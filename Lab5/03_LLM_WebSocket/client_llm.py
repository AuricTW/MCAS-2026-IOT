from getpass import getpass

from google import genai
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosed


MODEL = "gemini-3.5-flash-lite"
PORT = 8765

SYSTEM_INSTRUCTION = """
You are a device command classifier.

Convert the user's natural-language request into exactly one command:

on
off
status
unknown

Rules:
- Turn on, start, activate, enable -> on
- Turn off, stop, deactivate, disable -> off
- Ask about current state -> status
- If the request is unrelated or unclear -> unknown

Return only the command.
Do not explain.
"""


def ask_llm(client, user_text):
    interaction = client.interactions.create(
        model=MODEL,
        system_instruction=SYSTEM_INSTRUCTION,
        input=user_text,
    )

    command = interaction.output_text.strip().lower()

    if command not in {"on", "off", "status", "unknown"}:
        return "unknown"

    return command


def main():
    print("=== LLM + WebSocket Client ===")

    api_key = getpass("請輸入 Gemini API Key：").strip()

    if not api_key:
        print("ERROR: API Key 不可為空")
        return

    server_ip = input("請輸入 Raspberry Pi IP：").strip()
    uri = f"ws://{server_ip}:{PORT}"

    client = genai.Client(api_key=api_key)

    try:
        with connect(uri, proxy=None) as websocket:
            print(f"\nConnected to {uri}")
            print("輸入自然語言控制設備")
            print("輸入 quit 結束\n")

            while True:
                user_text = input("You: ").strip()

                if user_text.lower() == "quit":
                    print("Connection closed.")
                    break

                if not user_text:
                    continue

                try:
                    command = ask_llm(client, user_text)

                except Exception as error:
                    print(f"LLM API ERROR: {error}")
                    continue

                print(f"LLM Command: {command}")

                if command == "unknown":
                    print("無法判斷控制指令，不傳送至 Raspberry Pi。\n")
                    continue

                websocket.send(command)

                reply = websocket.recv()
                print(f"Server: {reply}\n")

    except (OSError, TimeoutError) as error:
        print(f"Connection failed: {error}")

    except ConnectionClosed:
        print("Connection to server was closed.")


if __name__ == "__main__":
    main()
