"""
dnd_consumer.py

Consumes Dungeons & Dragons event messages from a Kafka topic, processes them, 
and generates real-time visualizations.

Visualization Types:
- Spell Cast & Monster Encounters: Combined Line Chart
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

# Store aggregated event data
encounter_counts = defaultdict(int)  # {monster_type: count}
spell_cast_counts = defaultdict(int)  # {spell_name: count}
recent_events = deque(maxlen=20)  # Store the last 20 events

#####################################
# Define Message Processing Function
#####################################


def process_message(message):
    """
    Process incoming Kafka messages and update visualization data.
    """
    global encounter_counts, spell_cast_counts, recent_events

    event = message.value  # Kafka consumer already deserializes JSON
    event_type = event.get("event_type")

    if event_type == "encounter":
        monster_type = event.get("monster_type")
        encounter_counts[monster_type] += 1

    elif event_type == "spell_cast":
        spell_name = event.get("spell_name")
        spell_cast_counts[spell_name] += 1

    # Store recent events
    recent_events.append(event)


#####################################
# Define Combined Visualization Function
#####################################


def plot_encounter_and_spell_trend():
    """
    Generates a combined line chart showing monster encounters and spell usage.
    """
    plt.figure(figsize=(8, 5))

    # Plot monster encounters
    if encounter_counts:
        monsters = list(encounter_counts.keys())
        monster_frequencies = list(encounter_counts.values())
        plt.plot(monsters, monster_frequencies, marker="o", linestyle="-", label="Monster Encounters", color="red")

    # Plot spell usage
    if spell_cast_counts:
        spells = list(spell_cast_counts.keys())
        spell_frequencies = list(spell_cast_counts.values())
        plt.plot(spells, spell_frequencies, marker="o", linestyle="-", label="Spell Usage", color="blue")

    plt.xlabel("Event Type")
    plt.ylabel("Frequency")
    plt.title("Monster Encounters & Spell Usage Trends")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.show()


#####################################
# Define Consumer Function
#####################################


def consume_events():
    """
    Kafka Consumer that continuously reads messages from the topic and updates visuals.
    """
    print("📊 Starting D&D Consumer with Visualization...")

    kafka_server = config.get_kafka_broker_address()
    topic = config.get_kafka_topic()

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_server,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="dnd_consumer_group",
    )

    print(f"✅ Subscribed to Kafka topic: {topic}")

    message_count = 0  # Counter to track processed messages

    try:
        for message in consumer:
            process_message(message)
            message_count += 1
            time.sleep(config.get_message_interval_seconds_as_int())

            # Generate visualization every 2 messages
            if message_count % 1 == 0:
                print("📊 Updating visualization...")
                plot_encounter_and_spell_trend()

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
