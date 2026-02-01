#!/usr/bin/env python3
"""
YouTube Transcript Fetcher
Fetches transcripts for YouTube videos and stores them in PostgreSQL database.
"""

import json
import psycopg2
from youtube_transcript_api import YouTubeTranscriptApi


def load_video_ids(json_file='video_ids.json'):
    """Load video IDs from JSON file."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data['video_ids']


def create_database_table(cursor):
    """Create the transcripts table if it doesn't exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transcripts (
            id SERIAL PRIMARY KEY,
            video_id VARCHAR(20) UNIQUE NOT NULL,
            transcript TEXT NOT NULL
        )
    """)


def fetch_transcript(video_id):
    """Fetch transcript for a given video ID."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        # Combine all text segments into a single transcript
        transcript = ' '.join([entry['text'] for entry in transcript_list])
        return transcript
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
        return None


def store_transcript(cursor, video_id, transcript):
    """Store transcript in database."""
    try:
        cursor.execute(
            "INSERT INTO transcripts (video_id, transcript) VALUES (%s, %s) ON CONFLICT (video_id) DO NOTHING",
            (video_id, transcript)
        )
        return True
    except Exception as e:
        print(f"Error storing transcript for {video_id}: {e}")
        return False


def main():
    """Main function to orchestrate transcript fetching and storage."""
    # Database connection parameters
    # These should be configured in environment variables or a config file
    # For simplicity, using defaults that work with local PostgreSQL
    db_params = {
        'dbname': 'youtube_transcripts',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': '5432'
    }
    
    print("Starting YouTube Transcript Fetcher...")
    
    # Load video IDs
    print("Loading video IDs from JSON file...")
    video_ids = load_video_ids()
    print(f"Found {len(video_ids)} video IDs")
    
    # Connect to database
    print("Connecting to database...")
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        print("Connected successfully")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        print("Please ensure PostgreSQL is running and the database exists")
        return
    
    try:
        # Create table
        print("Creating table if it doesn't exist...")
        create_database_table(cursor)
        conn.commit()
        
        # Process each video
        successful = 0
        failed = 0
        
        for video_id in video_ids:
            print(f"\nProcessing video: {video_id}")
            
            # Fetch transcript
            transcript = fetch_transcript(video_id)
            
            if transcript:
                # Store in database
                if store_transcript(cursor, video_id, transcript):
                    conn.commit()
                    print(f"✓ Successfully stored transcript for {video_id}")
                    successful += 1
                else:
                    failed += 1
            else:
                failed += 1
        
        print(f"\n{'='*50}")
        print(f"Processing complete!")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"{'='*50}")
        
    finally:
        cursor.close()
        conn.close()
        print("\nDatabase connection closed")


if __name__ == '__main__':
    main()
