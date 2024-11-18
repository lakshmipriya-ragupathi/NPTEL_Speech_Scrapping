import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class NPTELDownloader:
    """
    A class to download audio files from NPTEL video lectures.
    """

    def __init__(self, output_dir, course_url):
        """
        Initializes the downloader with the output directory and course URL.
        
        Args:
            output_dir (str): Directory where audio files will be saved.
            course_url (str): URL of the NPTEL course page.
        """
        self.output_dir = output_dir
        self.course_url = course_url
        self.driver = None
        self.video_links = []

    def setup_driver(self):
        """
        Initializes the Selenium WebDriver with necessary Chrome options.
        
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
        chrome_options.add_argument("--no-sandbox")  # Disable sandbox mode
        chrome_options.add_argument("--disable-dev-shm-usage")  # Address memory issues
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection as a bot
        
        # Setup the WebDriver using ChromeDriverManager
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def fetch_video_links(self):
        """
        Extracts video links from the NPTEL course page.

        """
        try:
            print("Fetching the video links, this may take a while....")
            # Open the NPTEL course page
            self.driver.get(self.course_url)
            time.sleep(10)  # Wait for the page to load

            # Navigate to the "About Course" section
            about_course = self.driver.find_element(By.XPATH, '/html/body/app-root/app-course-details/main/section/app-course-detail-ui/div/div[2]/span[2]')
            about_course.click()
            time.sleep(15)  # Wait for the section to load

            # Locate and click the download section
            transcripts = self.driver.find_element(By.CLASS_NAME, 'course-downloads')
            download_buttons = transcripts.find_elements(By.CLASS_NAME, 'assignments')

            for i, button in enumerate(download_buttons):
                if i == 3:  # Select the desired download button
                    button.click()
                    break
            time.sleep(5)  # Wait for the download section to load

            # Extract video links from the download section
            divisions = button.find_elements(By.CLASS_NAME, 'd-data')
            self.video_links = [data.find_element(By.TAG_NAME, 'a').get_attribute("href") for data in divisions]
            print("Finished fetching the video links...")

        except Exception as e:
            print(f"Error fetching video links: {e}")
        finally:
            if self.driver:
                self.driver.quit()  # Ensure WebDriver is closed

    @staticmethod
    def download_audio_from_url(url, output_audio_path):
        """
        Downloads the audio from a video URL and saves it as an MP3 file.
        
        Args:
            url (str): URL of the video.
            output_audio_path (str): Path where the audio file will be saved.
        """
        try:
            # Command to extract audio from the video URL
            command = [
                "ffmpeg",
                "-i", url,
                "-vn",  # Skip video
                "-acodec", "libmp3lame",  # Use MP3 audio codec
                "-ar", "44100",  # Set audio sampling rate
                output_audio_path
            ]
            subprocess.run(command, check=True)  # Execute the ffmpeg command
            print(f"Audio saved to {output_audio_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error during audio extraction: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def download_videos(self):
        """
        Downloads audio tracks for all extracted video links.

        """
        if not os.path.exists(self.output_dir):  # Ensure output directory exists
            os.makedirs(self.output_dir)
        
        print("Downloading the audio...")
        for idx, link in enumerate(self.video_links):  # Iterate through video links
            output_audio_path = os.path.join(self.output_dir, f"audio_{idx}.mp3")
            self.download_audio_from_url(link, output_audio_path)  # Download each audio file


if __name__ == "__main__":
    """
    Entry point of the script. Parses command-line arguments and starts the download process.
    
    """
    import argparse

    # Setup argument parser
    parser = argparse.ArgumentParser(description="NPTEL Video Downloader")
    parser.add_argument("-o", "--output_dir",required=True, help="Directory to save audio files")
    parser.add_argument("-i", "--course_url", required=True, help="NPTEL course URL")
    args = parser.parse_args()

    # Initialize and execute the downloader
    downloader = NPTELDownloader(output_dir=args.output_dir, course_url=args.course_url)
    downloader.setup_driver()
    downloader.fetch_video_links()
    downloader.download_videos()
    
