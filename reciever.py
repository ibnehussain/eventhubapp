import asyncio
import os
from dotenv import load_dotenv
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

load_dotenv()

CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
EVENTHUB_NAME = os.getenv("EVENT_HUB_NAME")
STORAGE_CONNECTION_STR = os.getenv("STORAGE_CONNECTION_STR")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")


async def on_event(partition_context, event):
    print(f"Received event from partition {partition_context.partition_id}: {event.body_as_str()}")
    await partition_context.update_checkpoint(event)


async def receive_events():
    checkpoint_store = BlobCheckpointStore.from_connection_string(
        STORAGE_CONNECTION_STR, BLOB_CONTAINER_NAME
    )

    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group="$Default",
        eventhub_name=EVENTHUB_NAME,
        checkpoint_store=checkpoint_store,
    )

    async with client:
        print("Listening for events. Press Ctrl+C to stop.")
        await client.receive(
            on_event=on_event,
            starting_position="-1",  # "-1" reads from the beginning of the partition
        )


if __name__ == "__main__":
    asyncio.run(receive_events())
