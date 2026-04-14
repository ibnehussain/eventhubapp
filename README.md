# Azure Event Hub IoT Demo

A simple Python demo that simulates IoT devices sending telemetry events to **Azure Event Hub** and receiving them in real time.

---

## Project Structure

```
eventhub/
├── sender.py      # Sends simulated IoT events to Event Hub
├── reciever.py    # Listens and receives events from Event Hub
├── .env           # Configuration (not committed to source control)
└── README.md
```

---

## Prerequisites

- Python 3.8+
- An **Azure Event Hub** namespace and event hub entity
- An **Azure Storage Account** with a blob container (used for checkpointing)

---

## Setup

### 1. Install dependencies

```bash
pip install azure-eventhub azure-eventhub-checkpointstoreblob-aio python-dotenv
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
EVENT_HUB_CONNECTION_STR=<Your Event Hub namespace connection string>
EVENT_HUB_NAME=<Your event hub entity name>
STORAGE_CONNECTION_STR=<Your Azure Storage account connection string>
BLOB_CONTAINER_NAME=<Your blob container name for checkpoints>
```

> **Note:** Never commit `.env` to source control. Add it to `.gitignore`.

---

## Usage

### Send IoT Events

```bash
python sender.py
```

Sends one batch of telemetry events — one per simulated device (`device-001`, `device-002`, `device-003`).

**Sample output:**
```
Queued: {'device_id': 'device-001', 'timestamp': '2026-04-14T14:18:22Z', 'temperature_celsius': 65.5, ...}
Queued: {'device_id': 'device-002', ...}
Queued: {'device_id': 'device-003', ...}

3 IoT events sent successfully.
```

### Receive Events

```bash
python reciever.py
```

Starts a listener that continuously receives and prints incoming events. Press **Ctrl+C** to stop.

---

## IoT Payload Schema

Each event is a JSON object with the following fields:

| Field | Type | Description |
|---|---|---|
| `device_id` | string | Simulated device identifier |
| `timestamp` | string | UTC timestamp (ISO 8601) |
| `temperature_celsius` | float | Temperature reading (20–85 °C) |
| `humidity_percent` | float | Humidity reading (30–90%) |
| `pressure_hpa` | float | Atmospheric pressure (950–1050 hPa) |
| `vibration_g` | float | Vibration (0–5 g) |
| `status` | string | Device status: `normal`, `warning`, or `critical` |

---

## Checkpointing Behavior

The receiver uses **Azure Blob Storage** for checkpointing:

| Scenario | Behavior |
|---|---|
| First run (no checkpoint) | Reads all events from the beginning (`-1`) |
| Subsequent runs | Resumes from the last processed event |

To receive only new events (skip history), change `starting_position="-1"` to `starting_position="@latest"` in `reciever.py`.
