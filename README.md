# YouTube Video Downloader (Serverless)

This is a serverless Python application for downloading YouTube videos in various formats (MP4, WebM, MKV, MP3) and resolutions (360p to 4K). The app uses `yt_dlp` primarily and falls back to `pytube` in case of failure. Downloads are uploaded to a mock S3 bucket (via LocalStack), and metadata is saved in a PostgreSQL database.

## Features

- **Supported Formats**: mp4, webm, mkv, mp3
- **Supported Qualities**: 360p, 480p, 720p, 1080p, 4k (ignored for mp3)
- **Storage**: Uploads to mock S3 (`http://localhost:4566/youtube-downloader-bucket`)
- **Database**: Saves metadata to PostgreSQL (`videos` table)
- **API**: Exposes a REST endpoint `/download` (GET/POST)
- **Fallback Logic**: Automatically falls back to `pytube` if `yt_dlp` fails

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

- Python 3.8+
- Node.js & npm
- Docker
- FFmpeg (`/usr/bin/ffmpeg`)
- PostgreSQL
- AWS CLI (optional)

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone <repository_url>
cd youtube-downloader
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
docker run -d -p 4566:4566 localstack/localstack
```

### 6. Start PostgreSQL (Dockerized)

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

---

## Environment Variables

Configured in `serverless.yml`:

```yaml
S3_BUCKET_NAME: youtube-downloader-bucket
LOCALSTACK_ENDPOINT: http://localhost:4566
AWS_ACCESS_KEY_ID: test
AWS_SECRET_ACCESS_KEY: test
AWS_REGION: us-east-1
DB_HOST: localhost
DB_PORT: '5432'
DB_NAME: aws_yt
DB_USER: postgres
DB_PASSWORD: divyam
```

---

## Run Locally

```bash
serverless offline
```

API available at: `http://localhost:3000/download`

---

## API Reference

### POST /download

```bash
curl -X POST http://localhost:3000/download \
  -H "Content-Type: application/json" \
  -d '{"youtube_id": "AR9wAiAniu0", "format": "mp4", "quality": "720p"}'
```

### GET /download

```bash
curl "http://localhost:3000/download?youtube_id=AR9wAiAniu0&format=mp3"
```

---

## Example Output

```json
{
  "message": "Video processed successfully",
  "s3_url": "http://localhost:4566/youtube-downloader-bucket/videos/AR9wAiAniu0_<timestamp>.mp4",
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
