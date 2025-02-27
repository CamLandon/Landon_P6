"""
Config Utility
File: utils/utils_config.py

This script provides the configuration functions for the project. 

It centralizes the configuration management 
by loading environment variables from .env in the root project folder
and constructing file paths using pathlib. 

If you rename any variables in .env, remember to:
- recopy .env to .env.example (and hide the secrets)
- update the corresponding function in this module.
"""

#####################################
# Imports
#####################################

# import from Python Standard Library
import os
import pathlib

# import from external packages
from dotenv import load_dotenv

# import from local modules
from .utils_logger import logger

#####################################
# Load Environment Variables
#####################################

load_dotenv()

#####################################
# Getter Functions for .env Variables
#####################################

def get_zookeeper_address() -> str:
    """Fetch ZOOKEEPER_ADDRESS from environment or use default."""
    address = os.getenv("ZOOKEEPER_ADDRESS", "localhost:2181")
    logger.info(f"ZOOKEEPER_ADDRESS: {address}")
    return address


def get_kafka_broker_address() -> str:
    """Fetch KAFKA_BROKER_ADDRESS from environment or use default."""
    address = os.getenv("KAFKA_BROKER_ADDRESS", "localhost:9092")
    logger.info(f"KAFKA_BROKER_ADDRESS: {address}")
    return address


def get_kafka_topic() -> str:
    """Fetch DND_TOPIC from environment or use default."""
    topic = os.getenv("DND_TOPIC", "dnd_events")
    logger.info(f"DND_TOPIC: {topic}")
    return topic


def get_message_interval_seconds_as_int() -> int:
    """Fetch MESSAGE_INTERVAL_SECONDS from environment or use default."""
    interval = int(os.getenv("MESSAGE_INTERVAL_SECONDS", 2))
    logger.info(f"MESSAGE_INTERVAL_SECONDS: {interval}")
    return interval


def get_kafka_consumer_group_id() -> str:
    """Fetch BUZZ_CONSUMER_GROUP_ID from environment or use default."""
    group_id = os.getenv("BUZZ_CONSUMER_GROUP_ID", "buzz_group")
    logger.info(f"BUZZ_CONSUMER_GROUP_ID: {group_id}")
    return group_id


def get_base_data_path() -> pathlib.Path:
    """Fetch BASE_DATA_DIR from environment or use default."""
    project_root = pathlib.Path(__file__).parent.parent
    data_dir = project_root / os.getenv("BASE_DATA_DIR", "data")
    logger.info(f"BASE_DATA_DIR: {data_dir}")
    return data_dir

#####################################
# Defining EVENT_TYPES
#####################################

# Define valid event types
EVENT_TYPES = ["dice_roll", "encounter", "spell_cast"]

# Define valid dice types
DICE_TYPES = ["d4", "d6", "d8", "d10", "d12", "d20"]

# Define player names (Example list, update as needed)
PLAYERS = ["Stravos", "Ya", "Sylas", "Wurs"]

# Define monster types
MONSTERS = ["Goblin", "Orc", "Dragon", "Beholder"]

# Define spell names
SPELLS = ["Fireball", "Shield", "Magic Missile", "Cure Wounds"]

#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    # Test the configuration functions
    logger.info("Testing configuration.")
    try:
        get_zookeeper_address()
        get_kafka_broker_address()
        get_kafka_topic()
        get_message_interval_seconds_as_int()
        get_kafka_consumer_group_id()
        get_base_data_path()
        logger.info("SUCCESS: Configuration function tests complete.")
    except Exception as e:
        logger.error(f"ERROR: Configuration function test failed: {e}")