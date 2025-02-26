"""
dnd_consumer.py

Consumes Dungeons & Dragons event messages from a Kafka topic, processes them, 
and prepares them for analysis.

Example JSON message received:
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
import time
from collections import defaultdict, deque
from kafka import KafkaConsumer

# Import local config module
import utils.utils_config as config

#####################################
# Initialize Data Storage
#####################################

# Store aggregated event data
dice_roll_counts = defaultdict(lambda: defaultdict(int))  # {dice_type: {roll_result: count}}
encounter_counts = defaultdict(int)  # {monster_type: count}
spell_cast_counts = defaultdict(int)  # {spell_name: count}
recent_events = deque(maxlen=20)  # Store the last 20 events

#####################################
# Define Message Processing Function
#####################################


def process_message(message):
    """
    Process incoming Kafka messages based on event type.
    """
    global dice_roll_counts, encounter_counts, spell_cast_counts, recent_events

    event = message.value  # Remove json.loads() since it's already a dictionary
    event_type = event.get("event_type")

    if event_type == "dice_roll":
        dice_type = event.get("dice_type")
        roll_result = event.get("roll_result")
        if dice_type in config.DICE_TYPES:
            dice_roll_counts[dice_type][roll_result] += 1  # ✅ Matches updated structure

    elif event_type == "encounter":
        monster_type = event.get("monster_type")
        if monster_type in config.MONSTERS:
            encounter_counts[monster_type] += 1  # ✅ Matches updated structure

    elif event_type == "spell_cast":
        spell_name = event.get("spell_name")
        if spell_name in config.SPELLS:
            spell_cast_counts[spell_name] += 1  # ✅ Matches updated structure

    # Store recent events
    recent_events.append(event)

    # Print the event for debugging
    print(f"✅ Processed Event: {event}")


#####################################
# Define Consumer Function
#####################################


def consume_events():
    """
    Kafka Consumer that continuously reads messages from the topic.
    """
    print("Starting D&D Kafka Consumer...")

    # Load Kafka configurations
    kafka_server = config.get_kafka_broker_address()
    topic = config.get_kafka_topic()

    # Initialize Kafka Consumer
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_server,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="dnd_consumer_group",
    )

    print(f"✅ Subscribed to Kafka topic: {topic}")

    try:
        for message in consumer:
            process_message(message)
            time.sleep(config.get_message_interval_seconds_as_int())  # Controlled processing interval

    except KeyboardInterrupt:
        print("⚠️ Consumer interrupted by user. Shutting down...")
    finally:
        consumer.close()
        print("🛑 Kafka Consumer closed.")


#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    consume_events()