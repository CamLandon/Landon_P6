# D&D Kafka Event Tracker

The dnd_consumer.py script listens to the Kafka topic (dnd_events), processes incoming D&D game events, and updates real-time visualizations for tracked players. It categorizes events into dice rolls, encounters, and spell casts, maintaining a summary of each player's activity. The visualization refreshes every 5 messages, ensuring an up-to-date view of in-game events.

## 🚀 Features
- 🛠️ **Kafka-based event streaming**
- 🎲 **Tracks dice rolls, encounters, and spells**
- 📊 **Real-time visualization for players: Stravos and Wurs**
- ⚡ **Scalable for multiple players**

---

## 📥 Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/dnd-kafka-tracker.git
cd dnd-kafka-tracker
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Start Kafka Broker and Zookeeper**
Ensure Kafka and Zookeeper are running:
```sh
sh start-kafka.sh
```

### **4️⃣ Run the Producer**
This script simulates game events and sends them to Kafka:
```sh
python dnd_producer.py
```

### **5️⃣ Run the Consumer**
This script processes events and updates visualizations:
```sh
python dnd_consumer.py
```

---

## ⚙️ Configuration

Set up a `.env` file in the project root with your Kafka settings:
```sh
KAFKA_BROKER_ADDRESS=localhost:9092
DND_TOPIC=dnd_events
MESSAGE_INTERVAL_SECONDS=5
```
Alternatively, modify `utils_config.py` for custom configurations.

---

## 🎮 Usage

Once both **producer** and **consumer** are running:
- The **producer** generates and sends D&D game events.
- The **consumer** processes events and updates a **live visualization**.

Example Kafka event:
```json
{
    "player": "Stravos",
    "event_type": "dice_roll",
    "roll_result": 18
}
```

The visualization updates **every 5 messages** and displays **separate charts for Stravos and Wurs**.

---

## 🤝 Contributing

Contributions are welcome! To contribute:
1. **Fork** the repository.
2. **Create a new branch**: `git checkout -b feature-branch`.
3. **Make your changes and commit**: `git commit -m "Added new feature"`.
4. **Push and create a Pull Request**.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🏆 Acknowledgments
- **Apache Kafka** - For real-time event streaming.
- **Matplotlib** - For visualizing game events.
- **D&D Community** - For inspiring this project.

---

Happy adventuring and coding! 🎲🐉🚀

