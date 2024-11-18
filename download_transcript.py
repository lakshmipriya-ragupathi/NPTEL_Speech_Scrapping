import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class NPTELTranscriptsDownloader:
    """
    Class for downloading transcript files from NPTEL course pages.
    """

    def __init__(self, output_dir, course_url):
        """
        Initialize the downloader with the output directory and course URL.

        Args:
            output_dir (str): Directory where transcripts will be saved.
            course_url (str): URL of the NPTEL course.
        """
        self.output_dir = output_dir
        self.course_url = course_url
        self.driver = None
        self.transcripts_links = []

    def setup_driver(self):
        """
        Initialize the Chrome WebDriver with necessary options.

        Purpose:
            Prepares the Selenium WebDriver for scraping web pages.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Set up the driver using WebDriver Manager
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def fetch_transcripts_links(self):
        """
        Extract transcript links from the NPTEL course page.

        Purpose:
            Navigates the NPTEL course page, identifies the section with transcripts, 
            and collects their download links.

        Returns:
            Updates the `self.transcripts_links` list with the extracted links.
        """
        try:
            print("Fetching the audio links...")
            self.driver.get(self.course_url)
            time.sleep(10)

            # Navigate to the course content section
            about_course = self.driver.find_element(By.XPATH, '/html/body/app-root/app-course-details/main/section/app-course-detail-ui/div/div[2]/span[2]')
            about_course.click()
            time.sleep(15)

            # Locate and click the download button
            transcripts = self.driver.find_element(By.CLASS_NAME, 'course-downloads')
            download_buttons = transcripts.find_elements(By.CLASS_NAME, 'assignments')

            for i, button in enumerate(download_buttons):
                if i == 1:  # Select the specific button for transcripts
                    button.click()
                    break
            time.sleep(5)

            # Extract transcript links
            divisions = button.find_elements(By.CLASS_NAME, 'd-data')
            for data in divisions:
                opt = data.find_element(By.CSS_SELECTOR, "app-nptel-dropdown")
                opt.click()
                time.sleep(2)
                choose = data.find_element(By.CLASS_NAME, "pseudo-options")
                choose.click()
                time.sleep(2)
                link = data.find_element(By.TAG_NAME, 'a').get_attribute("href")
                self.transcripts_links.append(link)
                print("Fetching...")
            print("Finished fetching the links...")
        except Exception as e:
            print(f"Error fetching transcript links: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    @staticmethod
    def download_file(link, folder_path, file_prefix, idx):
        """
        Download a file from a link and save it to the specified folder.

        Args:
            link (str): The URL of the file to download.
            folder_path (str): Directory to save the downloaded file.
            file_prefix (str): Prefix for naming the downloaded file.
            idx (int): Index to uniquely identify the file.

        Returns:
            Saves the file in the specified folder.
        """
        try:
            if "drive.google.com" in link:
                file_id = link.split("/")[-2]
                download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                output_path = os.path.join(folder_path, f"{file_prefix}_{idx}.pdf")

                with requests.get(download_url, stream=True) as response:
                    if response.status_code == 200:
                        with open(output_path, "wb") as file:
                            for chunk in response.iter_content(chunk_size=8192):
                                file.write(chunk)
                        print(f"Downloaded: {output_path}")
                    else:
                        print(f"Failed to download {link}: HTTP {response.status_code}")
            else:
                print(f"Invalid Google Drive link: {link}")
        except Exception as e:
            print(f"Error downloading {link}: {e}")

    def download_transcripts(self):
        """
        Download all transcripts using the fetched links.

        Purpose:
            Iterates over the list of transcript links and downloads each file.

        Returns:
            Saves all downloaded files in the specified output directory.
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        print("Downloading the transcript files, this may take a while...")
        for idx, link in enumerate(self.transcripts_links):
            self.download_file(link, self.output_dir, file_prefix="transcript", idx=idx)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="NPTEL Transcripts Downloader")
    parser.add_argument("-o", "--output_dir", required=True, help="Directory to save transcript files")
    parser.add_argument("-i", "--course_url", required=True, help="NPTEL course URL")
    args = parser.parse_args()

    # Create the downloader instance and start the download process
    downloader = NPTELTranscriptsDownloader(output_dir=args.output_dir, course_url=args.course_url)
    downloader.setup_driver()
    downloader.fetch_transcripts_links()
    downloader.download_transcripts()

