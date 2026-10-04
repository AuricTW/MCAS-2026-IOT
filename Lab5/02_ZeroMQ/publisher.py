import time
import cv2
import zmq

PORT = 5555
WIDTH = 640
HEIGHT = 480
JPEG_QUALITY = 70


def main():
    context = zmq.Context()

    socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://*:{PORT}")

    print("=== ZeroMQ Publisher ===")
    print(f"Publishing on tcp://0.0.0.0:{PORT}")
    print("Opening camera...")

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Cannot open camera.")
        socket.close()
        context.term()
        return

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    # 給 Subscriber 一點連線時間
    time.sleep(1)

    print("Camera opened.")
    print("Sending frames... Press Ctrl+C to stop.")

    try:
        while True:
            ret, frame = camera.read()

            if not ret:
                print("ERROR: Failed to read camera frame.")
                break

            success, encoded = cv2.imencode(
                ".jpg",
                frame,
                [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY],
            )

            if not success:
                continue

            socket.send(encoded.tobytes())

            # 限制大約 15 FPS
            time.sleep(1 / 15)

    except KeyboardInterrupt:
        print("\nPublisher stopped.")

    finally:
        camera.release()
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
