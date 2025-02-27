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
import matplotlib.pyplot as plt
from collections import defaultdict, deque
from kafka import KafkaConsumer

# Import local config module
import utils.utils_config as config

#####################################
# Initialize Data Storage
#####################################

event_counts = {"dice_roll": 0, "encounter": 0, "spell_cast": 0}
recent_events = deque(maxlen=20)  # Store the last 20 events

MESSAGE_BATCH_SIZE = 5  # Update visualization every 5 messages
message_count = 0  # Track processed messages

#####################################
# Define Visualization Function
#####################################

def plot_event_summary():
    """Generate a simple bar chart summarizing all events."""
    plt.figure(figsize=(6, 4))
    plt.bar(event_counts.keys(), event_counts.values(), color=["blue", "red", "green"])
    plt.xlabel("Event Types")
    plt.ylabel("Total Count")
    plt.title("D&D Event Summary")
    plt.show()

#####################################
# Define Message Processing Function
#####################################

def process_message(message):
    """
    Process incoming Kafka messages based on event type.
    """
    global event_counts, recent_events

    event = message.value  # Already a dictionary
    event_type = event.get("event_type")
    player = event.get("player")

    if event_type in event_counts:
        event_counts[event_type] += 1

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
    global message_count
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
            message_count += 1

            if message_count % MESSAGE_BATCH_SIZE == 0:
                plot_event_summary()  # Update visualization every 5 messages

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
