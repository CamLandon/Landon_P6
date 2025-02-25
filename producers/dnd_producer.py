"""
dnd_producer.py

Simulates Dungeons & Dragons game events and streams them as JSON messages to a Kafka topic.

Example JSON message:
{
    "timestamp": "2025-02-24T20:30:00Z",
    "player": "Stravos",
    "event_type": "dice_roll",
    "dice_type": "d20",
    "roll_result": 15,
    "context": "attack_roll"
}

Configuration is stored in utils/config.py and producer/config_producer.json.
"""

#####################################
# Import Modules
#####################################

import json
import os
import random
import sys
import time
from datetime import datetime

# Import Kafka
from kafka import KafkaProducer

# Import local modules
import utils.config as config

#####################################
# Define Event Generator
#####################################


def generate_dnd_event():
    """
    Generates a random D&D game event (dice roll, encounter, or spell cast).
    """

    event_type = random.choice(config.EVENT_TYPES)

    # Dice Roll Event
    if event_type == "dice_roll":
        dice_type = random.choice(config.DICE_TYPES)
        roll_result = random.randint(1, int(dice_type[1:]))  # Extract max roll from "d20"
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "player": random.choice(config.PLAYERS),
            "event_type": "dice_roll",
            "dice_type": dice_type,
            "roll_result": roll_res
