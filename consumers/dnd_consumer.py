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

# Store aggregated event data per player
player_stats = defaultdict(lambda: {
    "dice_rolls": defaultdict(int),
    "encounters": defaultdict(int),
    "spells_cast": defaultdict(int),
})
recent_events = deque(maxlen=20)  # Store the last 20 events

#####################################
# Define Visualization Function
#####################################

def plot_player_statistics():
    """Generate a bar chart for each player's statistics."""
    for player, stats in player_stats.items():
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(f"Statistics for {player}")

        # Dice Rolls
        axs[0].bar(stats["dice_rolls"].keys(), stats["dice_rolls"].values())
        axs[0].set_title("Dice Rolls")
        axs[0].set_xlabel("Dice Type")
        axs[0].set_ylabel("Count")

        # Encounters
        axs[1].bar(stats["encounters"].keys(), stats["encounters"].values())
        axs[1].set_title("Encounters")
        axs[1].set_xlabel("Monster Type")
        axs[1].set_ylabel("Count")

        # Spells Cast
        axs[2].bar(stats["spells_cast"].keys(), stats["spells_cast"].values())
        axs[2].set_title("Spells Cast")
        axs[2].set_xlabel("Spell Name")
        axs[2].set_ylabel("Count")

        plt.show()

#####################################
# Define Message Processing Function
#####################################

def process_message(message):
    """
    Process incoming Kafka messages based on event type.
    """
    global player_stats, recent_events

    event = message.value  # Remove json.loads() since it's already a dictionary
    event_type = event.get("event_type")
    player = event.get("player")

    if event_type == "dice_roll":
        dice_type = event.get("dice_type")
        roll_result = event.get("roll_result")
        context = event.get("context")
        if dice_type in config.DICE_TYPES:
            player_stats[player]["dice_rolls"][dice_type] += 1
            print(f"🎲 {player} rolled a {roll_result} on a {dice_type} for a {context}.")

    elif event_type == "encounter":
        monster_type = event.get("monster_type")
        location = event.get("location")
        if monster_type in config.MONSTERS:
            player_stats[player]["encounters"][monster_type] += 1
            print(f"⚔️ {player} encountered a {monster_type} in the {location}!")

    elif event_type == "spell_cast":
        spell_name = event.get("spell_name")
        target = event.get("target")
        effect = event.get("effect")
        if spell_name in config.SPELLS:
            player_stats[player]["spells_cast"][spell_name] += 1
            if target == "enemy" and effect in ["damage", "debuff"]:
                print(f"✨ {player} cast {spell_name} on an enemy, causing {effect}.")
            elif target == "ally" and effect in ["heal", "buff"]:
                print(f"🛡️ {player} cast {spell_name} on an ally, providing {effect}.")
            elif target == "self" and effect in ["buff", "heal"]:
                print(f"🔮 {player} cast {spell_name} on themselves, gaining {effect}.")

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
            plot_player_statistics()  # Visualize after processing each message

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
