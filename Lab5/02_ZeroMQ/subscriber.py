import cv2
import numpy as np
import zmq

PORT = 5555


def main():
    publisher_ip = input("請輸入 Publisher 筆電 IP：").strip()

    context = zmq.Context()

    socket = context.socket(zmq.SUB)

    # 訂閱全部訊息
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    address = f"tcp://{publisher_ip}:{PORT}"
    socket.connect(address)

    print("=== ZeroMQ Subscriber ===")
    print(f"Connected to publisher: {address}")
    print("Receiving frames...")
    print("Press Q to quit.")

    try:
        while True:
            data = socket.recv()

            frame_array = np.frombuffer(
                data,
                dtype=np.uint8,
            )

            frame = cv2.imdecode(
                frame_array,
                cv2.IMREAD_COLOR,
            )

            if frame is None:
                continue

            cv2.imshow(
                "ZeroMQ Video - Raspberry Pi",
                frame,
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nSubscriber stopped.")

    finally:
        cv2.destroyAllWindows()
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
