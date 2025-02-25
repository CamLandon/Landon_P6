# buzzline-05-landon

This project demonstrates a simple streaming analytics pipeline that processes JSON messages, stores them in a SQLite database, and provides real-time insights with a live-updating bar chart. The example is built to be easily extended to other databases or more advanced visualization tools.

After each message is inserted into the database, the consumer runs a SQL query to group the messages by category and cacluate the average sentiment. Then the results are used to update a bar chart, created by matplotlib, redrawing the chart with each update. 

In this project, a producer generates streaming messages while two consumer options are available:
1. **File-Based Consumer:** Reads messages from a dynamically updating file.
2. **Real-Time Visualization Consumer:** Processes messages from the live file, aggregates average sentiment scores by category in a SQLite database, and updates a bar chart (implemented in `consumer_landon.py`).

---

## VS Code Extensions

To enhance your development experience, consider installing these VS Code extensions:
- **Black Formatter** by Microsoft
- **Markdown All in One** by Yu Zhang
- **PowerShell** by Microsoft (for Windows)
- **Pylance** by Microsoft
- **Python** by Microsoft
- **Python Debugger** by Microsoft
- **Ruff** by Astral Software (Linter)
- **SQLite Viewer** by Florian Klampfer
- **WSL** by Microsoft (for Windows)

---

## Project Setup

### Prerequisites
- **Python 3.11** is required.
- For those who wish to experiment with the Kafka-based consumer (provided for comparison), ensure you have a running instance of Kafka and Zookeeper. However, the real-time file-based consumer does not depend on Kafka.

### Virtual Environment and Dependencies
1. Create and activate your virtual environment:
   - **Windows:**
     ```shell
     .venv\Scripts\activate
     ```
   
2. Install the required dependencies using `requirements.txt`:
   ```shell
   pip install -r requirements.txt
