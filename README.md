# YouTube Video Downloader Lambda

This is a serverless application built with the Serverless Framework using AWS Lambda. It is designed to download YouTube videos in various formats (mp4, webm, mkv, mp3) and quality levels (360p, 480p, 720p, 1080p, 4k). The application uses yt_dlp with pytube as a fallback to ensure reliable downloads. Downloaded files are uploaded to an S3 bucket, and video metadata (such as title, duration, views, and upload date) is stored in a PostgreSQL database.

## 🎯 Objectives

* Accept a YouTube video URL via an API endpoint.
* Download the video using `pytube` or `yt_dlp`.
* Upload the video file to an S3 bucket.
* Extract and save metadata (title, duration, resolution, etc.).
* Store the metadata in a PostgreSQL database.
* Deploy using Serverless Framework v3.
  
## Features

* **Supported Formats**: mp4, webm, mkv, mp3
* **Supported Qualities**: 360p, 480p, 720p, 1080p, 4k (ignored for mp3)
* **Storage**: Videos are uploaded to S3 bucket
* **Database**: Saves metadata(YouTube ID, title, duration, resolution, S3 URL, format, quality) to PostgreSQL (`videos` table)
* **API**: REST endpoint (/download) accepts POST and GET requests with youtube\_id, format, and quality parameters.
* **Fallback Logic**: Automatically falls back to `pytube` if `yt_dlp` fails

---

## 📁 Project Structure

```
youtube-downloader/
├── core/
│   └── config.py                    # Configuration and environment setup
├── db/
│   ├── connection.py                # PostgreSQL connection setup
│   ├── save_metadata.py             # Logic to save metadata into DB
│   └── table_script.sql             # SQL schema for videos table
├── handler.py                       # Lambda function handler
├── package.json                     # Node.js dependencies for Serverless Framework
├── package-lock.json                # Lock file for npm dependencies
├── README.md                        # Project documentation
├── requirements.txt                 # Python dependencies
├── serverless.yml                   # Serverless Framework configuration
├── aws/                             # Virtual Environment
├── .env                             # Environment Variables File       
├── services/
│   ├── metadata.py                  # Service to extract and handle video metadata
│   ├── pytube.py                    # Fallback download logic using pytube
│   ├── youtube.py                   # Unified service to handle download flow
│   └── yt_dlp.py                    # Primary download logic using yt_dlp
└── utils/
    ├── bucket.py                    # S3 bucket-related utility function which ensure bucket exists
    ├── helpers.py                   # General-purpose helper utilities
    ├── pytube_utils.py              # pytube-specific utilities
    ├── s3_client.py                 # Initializes and handles S3 client
    ├── s3.py                        # S3 upload logic
    ├── validators.py                # Validations logic
    └── yt_dlp_utils.py              # yt_dlp-specific utilities
```

---

## Prerequisites

* Docker: For running LocalStack and PostgreSQL containers.
* Node.js: For Serverless Framework (npm).
* Python 3.8: For Lambda runtime and dependencies.
* PostgreSQL: Local or hosted instance (e.g., Dockerized).
* ffmpeg: Required for video/audio processing (/usr/bin/ffmpeg).
* AWS CLI: For interacting with LocalStack (optional for verification).
* LocalStack: For simulating AWS cloud services locally.
* Serverless Framework Offline Plugin: For running and testing Lambda functions locally (`serverless offline`).

---

## 🧪 Development Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/Divyam07and10/YouTube-Video-Downloader-Lambda.git
cd YouTube-Video-Downloader-Lambda
```

### 2. Install Dependencies

```bash
npm install
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install FFmpeg

* Ubuntu: `sudo apt install ffmpeg`
* macOS: `brew install ffmpeg`
* Verify: `ffmpeg -version`

### 4. Start LocalStack

```bash
localstack start -d
```

### 5. Start PostgreSQL Locally

```bash
docker run -d -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=divyam \
  -e POSTGRES_DB=aws_yt postgres
```

Create the table:

```bash
psql -h localhost -U postgres -d aws_yt -f db/table_script.sql
```

The schema.sql defines:

```sql
CREATE TABLE videos (
    id UUID PRIMARY KEY,
    youtube_id TEXT NOT NULL,
    title TEXT,
    duration INTEGER,
    resolution TEXT,
    s3_url TEXT NOT NULL,
    format TEXT,
    quality TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 6. Configure Environment Variables

```bash
S3_BUCKET_NAME=your-bucket-name
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key-id                             #For local simulation 'test' is used here
AWS_SECRET_ACCESS_KEY=your-secret-access-key                     #For local simulation 'test' is used here
IS_DEVELOPMENT=False                                             # If False, uploads videos to LocalStack S3 bucket for local simulation of s3 buket; if true, uploads to AWS S3 bucket
DB_HOST=localhost
DB_PORT=5432
DB_NAME=aws_yt
DB_USER=<database_username>
DB_PASSWORD=<database_password>
```

---

### 7. Run Locally

```bash
serverless offline
```

Access API at:

```
http://localhost:3000/dev/download
```

---

## 🚀 Deployment to AWS

Update credentials and region in your AWS CLI or CI/CD pipeline, then deploy:

```bash
serverless deploy
```
