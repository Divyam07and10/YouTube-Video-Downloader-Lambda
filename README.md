# YouTube Video Downloader (Serverless)

This is a serverless application built with the Serverless Framework, designed to download YouTube videos in various formats (mp4, webm, mkv, mp3) and quality levels (360p, 480p, 720p, 1080p, 4k). The application uses yt_dlp and pytube to download videos, stores the files in a LocalStack S3 bucket, and saves metadata in a PostgreSQL database. It runs on AWS Lambda (simulated locally with Serverless Offline and LocalStack) and provides a REST API endpoint for initiating downloads.

## Features

- **Supported Formats**: mp4, webm, mkv, mp3
- **Supported Qualities**: 360p, 480p, 720p, 1080p, 4k (ignored for mp3)
- **Storage**: Videos are uploaded to a LocalStack S3 bucket with URLs in the format s3://youtube-downloader-bucket/videos/<youtube_id>_<timestamp>.<format>.
- **Database**: Saves metadata(YouTube ID, title, duration, resolution, S3 URL, format, quality) to PostgreSQL (`videos` table)
- **API**: REST endpoint (/download) accepts POST and GET requests with youtube_id, format, and quality parameters.
- **Fallback Logic**: Automatically falls back to `pytube` if `yt_dlp` fails
- **Local Development**: Uses LocalStack for S3 and Serverless Offline for Lambda simulation.

---

## Project Structure

```
youtube-downloader/
├── handler.py            # Lambda handler
├── utils/
│   ├── youtube.py        # Downloading and metadata extraction
│   ├── s3_mock.py        # S3 file upload to LocalStack
│   ├── db.py             # PostgreSQL operations
├── settings.py           # Unused in current flow
├── serverless.yml        # Serverless Framework config
├── requirements.txt      # Python dependencies
├── db_setup.sql          # Schema for 'videos' table
└── README.md             # Project documentation
```

---

## Prerequisites

- Docker: For running LocalStack.
- Node.js: For Serverless Framework (npm).
- Python 3.8+: For Lambda runtime and dependencies.
- PostgreSQL: Local or hosted instance (e.g., Dockerized).
- FFmpeg: Required for video/audio processing (/usr/bin/ffmpeg).
- AWS CLI: For interacting with LocalStack (optional for verification).

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/Divyam07and10/YouTube-Video-Downloader-Lambda.git
cd YouTube-Video-Downloader-Lambda
```

### 2. Install Node Dependencies

```bash
npm install
```

### 3. Install Python Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Install FFmpeg

- **Ubuntu**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Verify**: `ffmpeg -version`

Make sure it's available at `/usr/bin/ffmpeg` or update `youtube.py`.

### 5. Start LocalStack

```bash
localstack start -d
```

### 6. Start PostgreSQL

```bash
docker run -d -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=divyam \
  -e POSTGRES_DB=aws_yt postgres
```

Create the `videos` table:

```bash
psql -h localhost -U postgres -d aws_yt -f db_setup.sql
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

## Configure Environment Variables

The serverless.yml defines environment variables. Ensure they match your setup:

```yaml
provider:
  name: aws
  runtime: python3.8
  environment:
    S3_BUCKET_NAME: youtube-downloader-bucket
    LOCALSTACK_ENDPOINT: http://localhost:4566
    AWS_ACCESS_KEY_ID: test
    AWS_SECRET_ACCESS_KEY: test
    AWS_REGION: us-east-1
    DB_HOST: localhost
    DB_PORT: <database username> (eg '5432')
    DB_NAME: <database name> (eg aws_yt)
    DB_USER: <database name> (eg postgres)
    DB_PASSWORD: <postgres database password> (eg password)
```

---

## Run Locally

```bash
serverless offline
```

API available at: `http://localhost:3000/dev/download`

---

## API Reference

Initiates the download of a YouTube video using the URL http://localhost:3000/download?youtube_id=<youtube_video_id>&format=<youtube_video_format>&quality=<youtube_video_quality>, stores it in the LocalStack S3 bucket, and saves metadata to the PostgreSQL database. The response includes an S3 URL in the format http://localhost:4566/youtube-downloader-bucket/videos/<youtube_id>_<timestamp>.<format>. Opening this URL in a browser or using a tool like curl will download the video or audio file stored in the LocalStack S3 bucket.

## Example URL
```bash
http://localhost:3000/download?youtube_id=AR9wAiAniu0&format=mp4&quality=720p
```

## Response Example
```json
{
  "message": "Video processed successfully",
  "s3_url": "http://localhost:4566/youtube-downloader-bucket/videos/AR9wAiAniu0_1631234567890.mp4",
  "metadata": {
    "youtube_id": "AR9wAiAniu0",
    "title": "Sample Video",
    "duration": 300,
    "resolution": "1280x720",
    "size_bytes": 10500000,
    "format": "mp4",
    "quality": "720p"
  }
}
```

## Additional API Releated Information

- The s3_url returned in the response can be accessed directly to download the video or audio file from the LocalStack S3 bucket.
- Supported formats: mp4, webm, mkv, mp3.
- Supported qualities: 360p, 480p, 720p, 1080p, 4k (ignored for mp3).

---

## Verification of Videos stored in the LocalStack mock S3 Bucket:

```bash
aws --endpoint-url=http://localhost:4566 s3 ls s3://youtube-downloader-bucket/videos/
```

---

## Notes

- If `yt_dlp` fails, `pytube` will be used automatically.
- mp3 ignores `quality`
- Files are deleted locally after upload to S3
- Use `aws --endpoint-url=http://localhost:4566 ...` to verify uploads
- Ensure the stream you request exists for the video

---

## License

MIT License
