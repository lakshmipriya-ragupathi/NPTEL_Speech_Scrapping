
# NPTEL Data Downloader and Preprocessing Toolkit

This repository provides tools to download and preprocess NPTEL lecture content, including lecture audios and transcripts, and to create training datasets for further analysis or model training. The repository is organized into various scripts, each serving a specific purpose.

---

## **Installation Requirements**

Ensure you have the following Python libraries and system tools installed before using the scripts:

- **Python Libraries**:  
  - `selenium`  
  - `webdriver_manager`  
  - `requests`  
  - `pypdf2`  
  - `num2words`  
  - `mutagen`  
  - `pandas`
  - `wave`

- **System Tools**:  
  - `GNU Parallel`  
  - `ffmpeg`

Install missing Python libraries using pip:

```bash
pip install selenium webdriver_manager requests pypdf2 num2words mutagen pandas
```

---

## **Scripts and Usage**

### 1. **Download NPTEL Lecture Audios**  
Download lecture audio files in MP4 format using `download_audio.py`.

**Command**:  
```bash
python download_audio.py -o <OUTPUT_DIR> -i <COURSE_URL>
```

**Options**:  
- `-o, --output_dir` : Directory to save audio files.  
- `-i, --course_url` : URL of the NPTEL course.  

---

### 2. **Download NPTEL Lecture Transcripts**  
Download lecture notes in PDF format using `download_transcript.py`.

**Command**:  
```bash
python download_transcript.py -o <OUTPUT_DIR> -i <COURSE_URL>
```

**Options**:  
- `-o, --output_dir` : Directory to save transcript files.  
- `-i, --course_url` : URL of the NPTEL course.  

---

### 3. **Preprocess Audio Files**  
Convert downloaded `.mp4` files to `.wav` format using the provided bash script.

**Command**:  
```bash
bash preprocess_audio.sh <input_directory> <output_directory> <num_cpus>
```

**Requirements**:  
- `GNU Parallel`  
- `ffmpeg`

Crop the last 10 seconds of background music in the `.wav` files using `crop_audio.py`.

**Command**:  
```bash
python crop_audio.py -i <INPUT_DIR> -o <OUTPUT_DIR>
```

**Requirements**:  
- `wave`  

---

### 4. **Preprocess Transcripts**  
Extract text from PDFs, clean it (remove punctuation, lowercase, and convert numbers to text), and save as `.txt` files.

**Command**:  
```bash
python preprocess_transcript.py -inp <INPUT_FOLDER> -op <OUTPUT_FOLDER>
```

**Options**:  
- `-inp, --input_folder` : Path to input PDF folder.  
- `-op, --output_folder` : Path to save cleaned `.txt` files.  

---

### 5. **Create Training Manifest**  
Generate a manifest JSONL file for training models using `create_manifest.py`.

**Command**:  
```bash
python create_manifest.py -aud <AUDIO_FOLDER> -tran <TRANSCRIPTION_FOLDER> -op <OUTPUT_MANIFEST>
```

**Options**:  
- `-aud, --audio_folder` : Path to the folder containing audio files.  
- `-tran, --transcription_folder` : Path to the folder containing transcription files.  
- `-op, --output_manifest` : Path to save the manifest file.  

---

### 6. **Generate Dashboards and Statistics**  
Use `dashboard_preprocess.py` to process the training manifest and generate CSVs for analysis.

**Command**:  
```bash
python dashboard_preprocess.py -i <INPUT_PATH> -o <OUTPUT_FOLDER>
```

**Options**:  
- `-i, --input_path` : Path to the manifest JSONL file.  
- `-o, --output_folder` : Path to save the generated CSV files.  

---

## **Output Files**

1. **Audio Files**: `.mp3` upon downloading, `.wav` format in the specified output directory upon conversion from `.mp3` to `.wav` and `.wav` format in the specified output directory upon cropping.  
2. **Transcripts**: `.pdf` files upon downloading,and cleaned `.txt` files for each PDF.  
3. **Training Manifest**: JSONL file with audio-duration-text pairs.  
4. **Dashboard Data**:  
   - CSV with fields: `duration`, `text`, `word_count`, `char_count`, `duration_bin`, `audio_id`.  
   - Summary CSV with `total_hours`, `total_utterances`, `vocabulary_size`, and `alphabet_size`.  

---

## **Contributors**  
Feel free to contribute by raising issues or submitting pull requests.  
