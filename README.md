# D&D Kafka Event Tracker

The dnd_consumer.py script listens to the Kafka topic (dnd_events), processes incoming D&D game events, and updates real-time visualizations for tracked players. It categorizes events into dice rolls, encounters, and spell casts, maintaining a summary of each player's activity. The visualization refreshes every 5 messages, ensuring an up-to-date view of in-game events.

🚀 Features

🛠️ Kafka-based event streaming

🎲 Tracks dice rolls, encounters, and spells

📊 Real-time visualization for Stravos and Wurs

⚡ Scalable for multiple players

📥 Installation

1️⃣ Clone the Repository

git clone https://github.com/your-username/dnd-kafka-tracker.git
cd dnd-kafka-tracker

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Start Kafka Broker and Zookeeper

Ensure Kafka and Zookeeper are running:

sh start-kafka.sh

4️⃣ Run the Producer

This script simulates game events and sends them to Kafka:

python dnd_producer.py

5️⃣ Run the Consumer

This script processes events and updates visualizations:

python dnd_consumer.py

⚙️ Configuration

Set up a .env file in the project root with your Kafka settings:

KAFKA_BROKER_ADDRESS=localhost:9092
DND_TOPIC=dnd_events
MESSAGE_INTERVAL_SECONDS=5

Alternatively, modify utils_config.py for custom configurations.

🎮 Usage

Once both producer and consumer are running:

The producer generates and sends D&D game events.

The consumer processes events and updates a live visualization.

Example Kafka event:

{
    "player": "Stravos",
    "event_type": "dice_roll",
    "roll_result": 18
}

The visualization updates every 5 messages and displays separate charts for Stravos and Wurs.

🔍 Insights Gained from This Project

1️⃣ Understanding Real-Time Data Streaming with Kafka

Learned how to produce, consume, and process streaming data using Kafka.

Saw how Kafka topics facilitate real-time event-driven applications.

2️⃣ Event Tracking for D&D Gameplay

Gained insights into how often players roll dice, encounter monsters, and cast spells.

Identified player-specific trends, such as which character casts the most spells or rolls the highest numbers.

3️⃣ Live Data Visualization

Implemented dynamic Matplotlib visualizations that refresh without requiring manual intervention.

Discovered how separating data per player improves readability and analysis.

4️⃣ Scalability & Flexibility

Designed a system that can easily extend to more players, new event types, or additional data sources.

Proved Kafka's ability to handle continuous event ingestion for gaming analytics.

🚀 Key Takeaway:

This project demonstrates the power of Kafka for real-time event processing and how it can be used to track and analyze gameplay data dynamically. It also highlights the benefits of live visualization for better decision-making and in-game insights.

Happy adventuring and coding! 🎲🐉🚀