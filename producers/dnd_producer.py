"""
dnd_producer.py

Simulates Dungeons & Dragons game events and streams them as JSON messages to a Kafka topic.

Example message:
{
    "timestamp": "2025-02-24T20:30:00Z",
    "player": "Stravos",
    "event_type": "dice_roll",
    "dice_type": "d20",
    "roll_result": 15,
    "context": "attack_roll"
}

Configuration is stored in utils.utils_config.py.
"""

#####################################
# Import Modules
#####################################

import json
import random
import sys
import time
from datetime import datetime

# Import Kafka
from kafka import KafkaProducer

# Import local config module
import utils.utils_config as config

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
            "roll_result": roll_result,  # ✅ Fixed the typo here
            "context": random.choice(["attack_roll", "saving_throw", "skill_check"]),
        }

    # Encounter Event
    elif event_type == "encounter":
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "player": random.choice(config.PLAYERS),
            "event_type": "encounter",
            "monster_type": random.choice(config.MONSTERS),
            "location": random.choice(["forest", "dungeon", "cave", "village"]),
            "initiative_order": random.randint(1, 20),
        }

    # Spell Cast Event
    elif event_type == "spell_cast":
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "player": random.choice(config.PLAYERS),
            "event_type": "spell_cast",
            "spell_name": random.choice(config.SPELLS),
            "target": random.choice(["enemy", "self", "ally"]),
            "effect": random.choice(["damage", "heal", "buff", "debuff"]),
        }


#####################################
# Define Main Producer Function
#####################################


def main():
    print("Starting D&D Kafka Producer...")

    # Load Kafka Configurations
    kafka_server = config.get_kafka_broker_address()  # ✅ Updated to match utils_config.py
    topic = config.get_kafka_topic()  # Now retrieves "dnd_events"
    event_frequency = config.get_message_interval_seconds_as_int()  # ✅ Updated

    # Initialize Kafka Producer
    try:
        producer = KafkaProducer(
            bootstrap_servers=kafka_server,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        )
        print(f"✅ Connected to Kafka broker at {kafka_server}")
    except Exception as e:
        print(f"❌ Error: Unable to connect to Kafka - {e}")
        sys.exit(1)

    print(f"🎲 Producing D&D events to topic '{topic}' every {event_frequency} seconds.")

    try:
        while True:
            event = generate_dnd_event()  # ✅ Now included in the main loop
            print(f"🔹 Generated Event: {event}")

            # Send event to Kafka
            producer.send(topic, value=event)
            print(f"✅ Sent event to Kafka topic '{topic}'")

            time.sleep(event_frequency)  # ✅ Controlled event frequency

    except KeyboardInterrupt:
        print("⚠️ Producer interrupted by user. Shutting down...")
    finally:
        producer.close()
        print("🛑 Kafka Producer closed.")


#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()
