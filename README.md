# GUI-SDE

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Kafka](https://img.shields.io/badge/Dependency-Kafka-orange.svg)](https://kafka.apache.org/)
[![Flink](https://img.shields.io/badge/Dependency-Flink-yellow.svg)](https://flink.apache.org/)
[![License](https://img.shields.io/badge/License-STELAR-green.svg)](#-license)

---

A **Graphical User Interface (GUI)** for the **Synopsis Data Engine (SDE)**, integrated into the **STELAR KLMS** under the **“Utilities”** tab.

This tool allows users to easily interact with the SDE for:
- 📂 Loading data from the **Data Catalog**
- 🧮 Creating and maintaining **synopses**
- 🔍 Querying **synopses** and viewing estimation results

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-org>/gui-sde.git
   cd gui-sde

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🧩 Prerequisites

Before running the GUI, ensure the following services are available.

### ✅ Kafka Topics (on sde.stelar.gr/kafka)

---
| Topic Name	| Purpose |
| --------------| ----------- |
| data	| For data ingestion |
| request | For sending requests to the SDE (e.g., creating or querying synopses) |
| estimation | For receiving estimation results from the SDE |
| logging | For reading logs from the SDE |
---

### ✅ Flink Cluster

Ensure the SDE is running on a Flink cluster.
For STELAR, go to [sde.stelar.gr/flink](http://sde.stelar.gr/flink) and:
1. Submit the Flink job for the SDE./
2. Specify custom kafka topic names, or use the default ones.
3. Set the parallelism to at least 2.

More instructions can be found at [https://sdeaas.github.io/](https://sdeaas.github.io/).

## 🚀 Running the GUI
Start the gui with:
```bash
python src/main.py
```
Once launched, the application will open, providing a user-friendly interface to:
- Load data from the Data Catalog
  - Data can be sent to the SDE from Catalog to SDE using 'Send Data' in the sidebar.
- Create and maintain synopses in the SDE
- Query the synopses and view estimation results

If run from STELAR KLMS, the uri with credentials is passed. If testing locally, a login url can be entered in ../txt_files/local_url.txt.

## Project Structure
```graphql
gui-sde/
- txt_files/ # Folder with text files, for instance 'dataset.txt', which contains SDE-approved datasets
- requirements.txt # Python dependencies
- src/ # Source code
    - messages/ # Kafka message formats
    - utils/ # Utility functions
    - weatherData/ # Mapping locations to coordinates
    - main.py # Main application file
- README.md # This file
- Dockerfile # Docker configuration for integration in KLMS
```