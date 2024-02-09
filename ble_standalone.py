import asyncio, logging
from ble_serial.bluetooth.ble_interface import BLE_interface

loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

def receive_callback(value: bytes):
    print("Received:", value)

async def hello_sender(ble: BLE_interface):
    while True:
        await asyncio.sleep(3.0)
        print("Sending...")
        ble.queue_send(b"Hello world\n")

async def main():

    await ble.connect(DEVICE, "public", 10.0)
    await ble.setup_chars(WRITE_UUID, READ_UUID, "rw")

    await asyncio.gather(ble.send_loop(), hello_sender(ble))

async def cleanup():
    await ble.disconnect()

ADAPTER = "hci0"
SERVICE_UUID = "0000abf0-0000-1000-8000-00805f9b34fb"
WRITE_UUID = "0000abf1-0000-1000-8000-00805f9b34fb"
READ_UUID = "0000abf2-0000-1000-8000-00805f9b34fb"

# DEVICE = "2200187C-B468-7F8B-0F47-ECAF760BFF8F" # for glutamine
DEVICE = "9CEDCDA1-2F20-A3CA-A05E-0A9344C53CB1" # for isoleucine

ble = BLE_interface(ADAPTER, SERVICE_UUID)
ble.set_receiver(receive_callback)

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.run_until_complete(cleanup())
    finally:
        pass
