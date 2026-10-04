from websockets.sync.server import serve
from websockets.exceptions import ConnectionClosed

HOST = "0.0.0.0"
PORT = 8765

device_state = "OFF"


def handle_client(websocket):
    global device_state

    client_address = websocket.remote_address

    if client_address:
        print(f"[CONNECTED] {client_address[0]}:{client_address[1]}")
    else:
        print("[CONNECTED] Client connected")

    try:
        for message in websocket:
            command = message.strip().lower()

            print(f"[RECEIVED] {command}")

            if command == "on":
                device_state = "ON"
                reply = "OK: Device ON"

            elif command == "off":
                device_state = "OFF"
                reply = "OK: Device OFF"

            elif command == "status":
                reply = f"STATUS: Device {device_state}"

            else:
                reply = "ERROR: Use on, off, or status"

            websocket.send(reply)
            print(f"[SENT] {reply}")

    except ConnectionClosed:
        pass

    finally:
        print("[DISCONNECTED] Client disconnected")


if __name__ == "__main__":
    print("=== WebSocket Server ===")
    print(f"Listening on ws://{HOST}:{PORT}")
    print("Waiting for client...\n")

    with serve(handle_client, HOST, PORT) as server:
        server.serve_forever()
