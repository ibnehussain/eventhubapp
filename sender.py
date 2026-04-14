import asyncio
import os
import json
import random
import time
from dotenv import load_dotenv
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

load_dotenv()

CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
EVENTHUB_NAME = os.getenv("EVENT_HUB_NAME")

DEVICES = ["device-001", "device-002", "device-003"]


def generate_iot_payload(device_id: str) -> dict:
    return {
        "device_id": device_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "temperature_celsius": round(random.uniform(20.0, 85.0), 2),
        "humidity_percent": round(random.uniform(30.0, 90.0), 2),
        "pressure_hpa": round(random.uniform(950.0, 1050.0), 2),
        "vibration_g": round(random.uniform(0.0, 5.0), 3),
        "status": random.choice(["normal", "warning", "critical"]),
    }


async def send_events():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        eventhub_name=EVENTHUB_NAME,
    )

    async with producer:
        event_data_batch = await producer.create_batch()

        for device_id in DEVICES:
            payload = generate_iot_payload(device_id)
            event_data_batch.add(EventData(json.dumps(payload)))
            print(f"Queued: {payload}")

        await producer.send_batch(event_data_batch)
        print(f"\n{len(DEVICES)} IoT events sent successfully.")


if __name__ == "__main__":
    asyncio.run(send_events())
