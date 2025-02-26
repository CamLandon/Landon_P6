"""
dnd_consumer.py

Consumes Dungeons & Dragons event messages from a Kafka topic, processes them, 
and generates real-time visualizations.

Visualization:
- A continuously updating line chart that displays both:
  1. Monster Encounter Trends
  2. Spell Usage Trends
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
# Define Continuous Visualization Function
#####################################


def plot_encounter_and_spell_trend():
    """
    Generates a continuously updating line chart for monster encounters and spell usage.
    """
    plt.ion()  # Enable interactive mode
    plt.clf()  # Clear previous plot

    plotted_something = False  # Track if anything was plotted

    # Plot monster encounters
    if encounter_counts:
        monsters = list(encounter_counts.keys())
        monster_frequencies = list(encounter_counts.values())
        if monsters:
            plt.plot(monsters, monster_frequencies, marker="o", linestyle="-", label="Monster Encounters", color="red")
            plotted_something = True

    # Plot spell usage
    if spell_cast_counts:
        spells = list(spell_cast_counts.keys())
        spell_frequencies = list(spell_cast_counts.values())
        if spells:
            plt.plot(spells, spell_frequencies, marker="o", linestyle="-", label="Spell Usage", color="blue")
            plotted_something = True

    plt.xlabel("Event Type")
    plt.ylabel("Frequency")
    plt.title("Monster Encounters & Spell Usage Trends")
    plt.xticks(rotation=45)

    if plotted_something:
        plt.legend()

    plt.grid()
    plt.draw()
    plt.pause(0.1)  # Allow real-time updating without blocking execution


#####################################
# Define Consumer Function
#####################################


def consume_events():
    """
    Kafka Consumer that continuously reads messages from the topic and updates visuals.
    """
    print("📊 Starting D&D Consumer with Real-Time Visualization...")

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
            if message_count % 2 == 0:
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
