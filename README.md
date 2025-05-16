YouTube Video Downloader
This is a serverless application built with the Serverless Framework, designed to download YouTube videos in various formats (mp4, webm, mkv, mp3) and quality levels (360p, 480p, 720p, 1080p, 4k). The application uses yt_dlp and pytube to download videos, stores the files in a LocalStack S3 bucket, and saves metadata in a PostgreSQL database. It runs on AWS Lambda (simulated locally with Serverless Offline and LocalStack) and provides a REST API endpoint for initiating downloads.
Features

Supported Formats: Download videos in mp4, webm, mkv, or audio-only mp3.
Supported Qualities: Select video quality from 360p, 480p, 720p, 1080p, or 4k (ignored for mp3).
Storage: Videos are uploaded to a LocalStack S3 bucket with URLs in the format s3://youtube-downloader-bucket/videos/<youtube_id>_<timestamp>.<format>.
Database: Metadata (YouTube ID, title, duration, resolution, S3 URL, format, quality) is stored in a PostgreSQL database.
API: REST endpoint (/download) accepts POST and GET requests with youtube_id, format, and quality parameters.
Local Development: Uses LocalStack for S3 and Serverless Offline for Lambda simulation.

Project Structure
youtube-downloader/
├── handler.py          # Main Lambda handler for the /download endpoint
├── utils/
│   ├── youtube.py      # Video download and metadata extraction logic
│   ├── s3_mock.py      # S3 upload logic for LocalStack
│   ├── db.py           # PostgreSQL database operations
├── schema.sql          # Database schema for the videos table
├── serverless.yml      # Serverless Framework configuration
├── requirements.txt    # Python dependencies
├── package.json        # Node.js dependencies for Serverless Framework
└── README.md           # Project documentation

Prerequisites

Docker: For running LocalStack.
Node.js: For Serverless Framework (npm).
Python 3.8+: For Lambda runtime and dependencies.
PostgreSQL: Local or hosted instance (e.g., Dockerized).
FFmpeg: Required for video/audio processing (/usr/bin/ffmpeg).
AWS CLI: For interacting with LocalStack (optional for verification).

Setup
1. Clone the Repository
git clone <repository_url>
cd youtube-downloader

2. Install Node.js Dependencies
Install Serverless Framework and plugins:
npm install

3. Install Python Dependencies
Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Ensure requirements.txt includes:
yt_dlp
pytube
boto3
psycopg2-binary
localstack

4. Install FFmpeg
Install FFmpeg on your system:

Ubuntu:sudo apt update
sudo apt install ffmpeg


macOS:brew install ffmpeg


Verify:ffmpeg -version



Ensure FFmpeg is accessible at /usr/bin/ffmpeg or update the ffmpeg_location in youtube.py if different.
5. Set Up LocalStack
Run LocalStack using Docker:
docker run -d -p 4566:4566 localstack/localstack

Verify LocalStack is running:
curl http://localhost:4566

6. Set Up PostgreSQL
Run a PostgreSQL instance (e.g., via Docker):
docker run -d -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=divyam -e POSTGRES_DB=aws_yt postgres

Create the videos table:
psql -h localhost -U postgres -d aws_yt -f schema.sql

The schema.sql defines:
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

7. Configure Environment Variables
The serverless.yml defines environment variables. Ensure they match your setup:
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
    DB_PORT: '5432'
    DB_NAME: aws_yt
    DB_USER: postgres
    DB_PASSWORD: divyam

Usage
Start the Application
Run Serverless Offline:
serverless offline

The API will be available at http://localhost:3000.
API Endpoint

Endpoint: /download
Methods: POST, GET
Parameters:
youtube_id (required): YouTube video ID (e.g., AR9wAiAniu0).
format (optional): File format (mp4, webm, mkv, mp3). Default: mp4.
quality (optional): Video quality (360p, 480p, 720p, 1080p, 4k). Default: 720p. Ignored for mp3.



Example Requests

POST (mp4, 720p):
curl -X POST http://localhost:3000/download -H "Content-Type: application/json" -d '{"youtube_id": "AR9wAiAniu0", "format": "mp4", "quality": "720p"}'


GET (webm, 1080p):
curl http://localhost:3000/download?youtube_id=AR9wAiAniu0&format=webm&quality=1080p


POST (mp3):
curl -X POST http://localhost:3000/download -H "Content-Type: application/json" -d '{"youtube_id": "AR9wAiAniu0", "format": "mp3"}'



Response
{
  "message": "Video processed successfully",
  "s3_url": "s3://youtube-downloader-bucket/videos/AR9wAiAniu0_<timestamp>.<format>",
  "metadata": {
    "youtube_id": "AR9wAiAniu0",
    "title": "<video_title>",
    "duration": 26,
    "resolution": "<width>x<height>" or "audio" (for mp3),
    "size_bytes": <file_size>,
    "format": "<format>",
    "quality": "<quality>" or null (for mp3)
  }
}

Verification

Check S3 Bucket:
aws --endpoint-url=http://localhost:4566 s3 ls s3://youtube-downloader-bucket/videos/

Download a file:
aws --endpoint-url=http://localhost:4566 s3 cp s3://youtube-downloader-bucket/videos/AR9wAiAniu0_<timestamp>.mp4 ./test.mp4


Check Database:
psql -h localhost -U postgres -d aws_yt
SELECT youtube_id, s3_url, format, quality, resolution FROM videos WHERE youtube_id = 'AR9wAiAniu0';



Testing
Test all combinations of formats and qualities:
# mp4 at 360p
curl -X POST http://localhost:3000/download -H "Content-Type: application/json" -d '{"youtube_id": "AR9wAiAniu0", "format": "mp4", "quality": "360p"}'

# webm at 4k
curl -X POST http://localhost:3000/download -H "Content-Type: application/json" -d '{"youtube_id": "AR9wAiAniu0", "format": "webm", "quality": "4k"}'

# mkv at 1080p
curl -X POST http://localhost:3000/download -H "Content-Type: application/json" -d '{"youtube_id": "AR9wAiAniu0", "format": "mkv", "quality": "1080p"}'

# mp3
curl -X POST http://localhost:3000/download -H "Content-Type: application/json" -d '{"youtube_id": "AR9wAiAniu0", "format": "mp3"}'

Error Cases

Invalid Format:
curl -X POST http://localhost:3000/download -H "Content-Type: application/json" -d '{"youtube_id": "AR9wAiAniu0", "format": "avi"}'

Response: {"error": "Invalid format. Allowed formats: ['mp4', 'webm', 'mkv', 'mp3']"}

Invalid Quality:
curl -X POST http://localhost:3000/download -H "Content-Type: application/json" -d '{"youtube_id": "AR9wAiAniu0", "format": "mp4", "quality": "144p"}'

Response: {"error": "Invalid quality. Allowed qualities: ['360p', '480p', '720p', '1080p', '4k']"}

Invalid YouTube ID:
curl -X POST http://localhost:3000/download -H "Content-Type: application/json" -d '{"youtube_id": "invalid_id", "format": "mp4"}'

Response: {"error": "Invalid YouTube video ID"}


Troubleshooting

Download Fails:

Check Serverless logs for yt_dlp or pytube errors.
Verify available streams: yt-dlp -F https://www.youtube.com/watch?v=AR9wAiAniu0.
Ensure FFmpeg is installed and accessible at /usr/bin/ffmpeg.


S3 Upload Fails:

Confirm LocalStack is running (curl http://localhost:4566).
Check S3_BUCKET_NAME and LOCALSTACK_ENDPOINT in serverless.yml.


Database Errors:

Verify PostgreSQL is running and credentials match serverless.yml.
Ensure the videos table exists (psql -f schema.sql).


Timeout Issues:

Increase timeout in serverless.yml (default: 300 seconds) for large videos.
Monitor request duration in logs.



Notes

Quality for mp3: Ignored, as mp3 is audio-only. Metadata sets quality to null.
Stream Availability: Not all videos support all qualities (e.g., 4k may not be available). The app selects the closest available resolution.
File Cleanup: Local files in /tmp are deleted after S3 upload to prevent storage issues.
Dependencies: Ensure ffmpeg supports required codecs (libx264, aac, libmp3lame, vp9, opus).

Contributing
Submit issues or pull requests to the repository. Ensure tests cover new formats or qualities.
License
MIT License. See LICENSE file for details.
