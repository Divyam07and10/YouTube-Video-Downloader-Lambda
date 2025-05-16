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