# YouTube Transcript Fetcher

A simple Python script that fetches YouTube video transcripts and stores them in a PostgreSQL database.

## Features

- Reads YouTube video IDs from a JSON file
- Fetches transcripts using youtube-transcript-api
- Stores transcripts in a PostgreSQL database
- Simple command-line execution: `python fetch_transcripts.py`

## Prerequisites

- Python 3.6 or higher
- PostgreSQL database server

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database:**
   - Ensure PostgreSQL is running
   - Create a database named `youtube_transcripts`:
     ```sql
     CREATE DATABASE youtube_transcripts;
     ```
   - Configure database credentials (optional):
     - By default, the script uses: user=postgres, password=postgres, host=localhost, port=5432
     - You can override these using environment variables:
       ```bash
       export DB_NAME=youtube_transcripts
       export DB_USER=postgres
       export DB_PASSWORD=your_password
       export DB_HOST=localhost
       export DB_PORT=5432
       ```

3. **Configure video IDs:**
   - Edit `video_ids.json` and add the YouTube video IDs you want to fetch transcripts for:
     ```json
     {
       "video_ids": [
         "dQw4w9WgXcQ",
         "9bZkp7q19f0",
         "kJQP7kiw5Fk"
       ]
     }
     ```

## Usage

Simply run the script:

```bash
python fetch_transcripts.py
```

The script will:
1. Load video IDs from `video_ids.json`
2. Create the database table if it doesn't exist
3. Fetch transcripts for each video
4. Store them in the PostgreSQL database

## Database Schema

The script creates a table named `transcripts` with the following structure:

| Column     | Type         | Description                    |
|------------|--------------|--------------------------------|
| id         | SERIAL       | Primary key (auto-increment)   |
| video_id   | VARCHAR(20)  | YouTube video ID (unique)      |
| transcript | TEXT         | Video transcript content       |

## Notes

- Transcripts are fetched in English by default
- Duplicate video IDs are handled automatically (won't create duplicate entries)
- The script provides progress feedback during execution