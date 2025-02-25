"""
file_consumer_case.py

Consume JSON messages from a live data file.
For each processed message, calculate a real-time SQL aggregation in a SQLite database
of average sentiment score by category and update a bar chart.
"""

#####################################
# Import Modules
#####################################

import json
import pathlib
import sys
import time
import sqlite3
import matplotlib.pyplot as plt

# Import from local modules
import utils.utils_config as config
from utils.utils_logger import logger
from .db_sqlite_case import init_db, insert_message

#####################################
# Function to process a single message
#####################################

def process_message(message: dict) -> dict:
    """
    Process and transform a single JSON message.
    Converts message fields to appropriate data types.
    
    Args:
        message (dict): The JSON message as a dictionary.
        
    Returns:
        dict: Processed message dictionary or None if error occurs.
    """
    try:
        processed_message = {
            "message": message.get("message"),
            "author": message.get("author"),
            "timestamp": message.get("timestamp"),
            "category": message.get("category"),
            "sentiment": float(message.get("sentiment", 0.0)),
            "keyword_mentioned": message.get("keyword_mentioned"),
            "message_length": int(message.get("message_length", 0)),
        }
        logger.info(f"Processed message: {processed_message}")
        return processed_message
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return None

#####################################
# Function to update the bar chart
#####################################

def update_chart(sqlite_path: pathlib.Path, ax) -> None:
    """
    Query the SQLite database to compute average sentiment by category,
    and update the bar chart accordingly.
    
    Args:
        sqlite_path (pathlib.Path): Path to the SQLite database file.
        ax: Matplotlib Axes object.
    """
    try:
        conn = sqlite3.connect(str(sqlite_path))
        cursor = conn.cursor()
        cursor.execute(
            "SELECT category, AVG(sentiment) as avg_sentiment FROM streamed_messages GROUP BY category"
        )
        results = cursor.fetchall()
        conn.close()

        categories = [row[0] for row in results]
        avg_sentiments = [row[1] for row in results]

        ax.clear()
        ax.bar(categories, avg_sentiments, color="skyblue")
        ax.set_xlabel("Category")
        ax.set_ylabel("Average Sentiment")
        ax.set_title("Real-Time Average Sentiment by Category")
        plt.draw()
        plt.pause(0.001)
    except Exception as e:
        logger.error(f"Error updating chart: {e}")

#####################################
# Consume Messages from Live Data File
#####################################

def consume_messages_from_file(live_data_path: pathlib.Path, sqlite_path: pathlib.Path, interval_secs: int, last_position: int, ax) -> None:
    """
    Consume new messages from a file, process them, insert into SQLite DB,
    and update the bar chart with the latest SQL aggregation.
    
    Args:
        live_data_path (pathlib.Path): Path to the live data file.
        sqlite_path (pathlib.Path): Path to the SQLite database file.
        interval_secs (int): Interval in seconds to check for new messages.
        last_position (int): Last read position in the file.
        ax: Matplotlib Axes object for the bar chart.
    """
    logger.info("Starting message consumption with real-time chart updates.")
    logger.info(f"Live data file: {live_data_path}")
    logger.info(f"SQLite DB path: {sqlite_path}")

    # Initialize the database
    init_db(sqlite_path)

    # Start reading from the beginning of the file
    last_position = 0

    while True:
        try:
            with open(live_data_path, "r") as file:
                file.seek(last_position)
                for line in file:
                    if line.strip():
                        try:
                            message = json.loads(line.strip())
                        except json.JSONDecodeError as e:
                            logger.error(f"JSON decode error: {e}")
                            continue

                        processed_message = process_message(message)
                        if processed_message:
                            insert_message(processed_message, sqlite_path)
                            # Update the bar chart after each message insertion
                            update_chart(sqlite_path, ax)

                # Update last_position to current file pointer location
                last_position = file.tell()
        except FileNotFoundError:
            logger.error(f"ERROR: Live data file not found at {live_data_path}.")
            sys.exit(10)
        except Exception as e:
            logger.error(f"ERROR: Error reading from live data file: {e}")
            sys.exit(11)

        time.sleep(interval_secs)

#####################################
# Define Main Function
#####################################

def main() -> None:
    """
    Main function to run the consumer process.
    Reads configuration, initializes the database and the live chart, and starts consumption.
    """
    logger.info("Starting Consumer with real-time SQL aggregation and chart updates.")
    try:
        interval_secs: int = config.get_message_interval_seconds_as_int()
        live_data_path: pathlib.Path = config.get_live_data_path()
        sqlite_path: pathlib.Path = config.get_sqlite_path()
        logger.info("Successfully read environment variables.")
    except Exception as e:
        logger.error(f"ERROR: Failed to read environment variables: {e}")
        sys.exit(1)

    logger.info("Deleting any prior database file for a fresh start.")
    if sqlite_path.exists():
        try:
            sqlite_path.unlink()
            logger.info("Deleted existing database file.")
        except Exception as e:
            logger.error(f"ERROR: Failed to delete DB file: {e}")
            sys.exit(2)

    # Set up matplotlib for real-time updating
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()

    try:
        consume_messages_from_file(live_data_path, sqlite_path, interval_secs, 0, ax)
    except KeyboardInterrupt:
        logger.warning("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"ERROR: Unexpected error: {e}")
    finally:
        logger.info("Consumer shutting down.")
        plt.ioff()
        plt.show()

#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()
