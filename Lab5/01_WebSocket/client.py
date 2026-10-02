from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosed

PORT = 8765

server_ip = input("請輸入 Raspberry Pi IP：").strip()
uri = f"ws://{server_ip}:{PORT}"

try:
    with connect(uri, proxy=None) as websocket:
        print(f"Connected to {uri}")
        print("Commands: on / off / status / quit\n")

        while True:
            command = input("Command: ").strip().lower()

            if command == "quit":
                print("Connection closed.")
                break

            if not command:
                continue

            websocket.send(command)

            reply = websocket.recv()
            print(f"Server: {reply}")

except (OSError, TimeoutError) as error:
    print(f"Connection failed: {error}")

except ConnectionClosed:
    print("Connection to server was closed.")
