"""
dnd_visualization.py

Reads processed D&D event data from the consumer and generates real-time visualizations.

Visualization Types:
- Dice Roll Distribution: Bar Chart
- Encounter Frequency: Line Chart
- Spell Usage: Bar Chart

"""

#####################################
# Import Modules
#####################################

import json
import time
import matplotlib.pyplot as plt
from collections import defaultdict, deque
from kafka import KafkaConsumer
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
    Process incoming Kafka messages and update visualization data.
    """
    global dice_roll_counts, encounter_counts, spell_cast_counts, recent_events

    event = message.value  # Message is already a dictionary
    event_type = event.get("event_type")

    if event_type == "dice_roll":
        dice_type = event.get("dice_type")
        roll_result = event.get("roll_result")
        dice_roll_counts[dice_type][roll_result] += 1

    elif event_type == "encounter":
        monster_type = event.get("monster_type")
        encounter_counts[monster_type] += 1

    elif event_type == "spell_cast":
        spell_name = event.get("spell_name")
        spell_cast_counts[spell_name] += 1

    # Store recent events
    recent_events.append(event)

#####################################
# Define Visualization Functions
#####################################


def plot_dice_roll_distribution():
    """
    Generates a bar chart showing dice roll distributions.
    """
    plt.figure(figsize=(8, 5))
    for dice_type, rolls in dice_roll_counts.items():
        rolls_sorted = sorted(rolls.items())  # Sort by roll result
        roll_values = [r[0] for r in rolls_sorted]
        roll_counts = [r[1] for r in rolls_sorted]
        plt.bar(roll_values, roll_counts, label=dice_type)

    plt.xlabel("Dice Roll Result")
    plt.ylabel("Frequency")
    plt.title("Dice Roll Distribution")
    plt.legend()
    plt.show()


def plot_encounter_trend():
    """
    Generates a line chart showing how often each monster type appears.
    """
    plt.figure(figsize=(8, 5))
    monster_names = list(encounter_counts.keys())
    encounter_frequencies = list(encounter_counts.values())

    plt.plot(monster_names, encounter_frequencies, marker="o", linestyle="-")

    plt.xlabel("Monster Type")
    plt.ylabel("Encounter Frequency")
    plt.title("Encounter Trends")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()


def plot_spell_usage():
    """
    Generates a bar chart showing spell usage counts.
    """
    plt.figure(figsize=(8, 5))
    spell_names = list(spell_cast_counts.keys())
    spell_frequencies = list(spell_cast_counts.values())

    plt.bar(spell_names, spell_frequencies, color="purple")

    plt.xlabel("Spell Name")
    plt.ylabel("Usage Count")
    plt.title("Spell Usage Frequency")
    plt.xticks(rotation=45)
    plt.show()


#####################################
# Define Consumer Function
#####################################


def consume_events():
    """
    Kafka Consumer that continuously reads messages from the topic and updates visuals.
    """
    print("📊 Starting D&D Visualization Consumer...")

    kafka_server = config.get_kafka_broker_address()
    topic = config.get_kafka_topic()

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_server,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="dnd_visualization_group",
    )

    print(f"✅ Subscribed to Kafka topic: {topic}")

    try:
        for message in consumer:
            process_message(message)
            time.sleep(config.get_message_interval_seconds_as_int())  # Controlled processing interval

    except KeyboardInterrupt:
        print("⚠️ Visualization Consumer interrupted by user. Shutting down...")
    finally:
        consumer.close()
        print("🛑 Kafka Visualization Consumer closed.")


#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    consume_events()
