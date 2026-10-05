import threading
import socket

import zmq
from flask import Flask, Response


ZMQ_PORT = 5555
WEB_PORT = 5000

app = Flask(__name__)

latest_frame = None
frame_number = 0
frame_condition = threading.Condition()


def get_local_ip(target_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect((target_ip, ZMQ_PORT))
        return sock.getsockname()[0]
    finally:
        sock.close()


def receive_frames(publisher_ip):
    global latest_frame, frame_number

    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    address = f"tcp://{publisher_ip}:{ZMQ_PORT}"
    subscriber.connect(address)

    print("=== ZeroMQ Subscriber ===")
    print(f"Connected to publisher: {address}")
    print("Receiving frames...")

    try:
        while True:
            data = subscriber.recv()

            with frame_condition:
                latest_frame = data
                frame_number += 1
                frame_condition.notify_all()

    except KeyboardInterrupt:
        pass

    finally:
        subscriber.close()
        context.term()


def generate_frames():
    last_frame_number = -1

    while True:
        with frame_condition:
            frame_condition.wait_for(
                lambda: (
                    latest_frame is not None
                    and frame_number != last_frame_number
                )
            )

            frame = latest_frame
            last_frame_number = frame_number

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame
            + b"\r\n"
        )


@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ZeroMQ Video</title>
    </head>
    <body>
        <h2>ZeroMQ Video - Raspberry Pi</h2>
        <img src="/video_feed" width="640">
    </body>
    </html>
    """


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


def main():
    publisher_ip = input(
        "請輸入 Publisher 筆電 IP："
    ).strip()

    pi_ip = get_local_ip(publisher_ip)

    receiver_thread = threading.Thread(
        target=receive_frames,
        args=(publisher_ip,),
        daemon=True,
    )

    receiver_thread.start()

    print()
    print("=== Browser Viewer ===")
    print(f"請在瀏覽器開啟：http://{pi_ip}:{WEB_PORT}")
    print("Press Ctrl+C to stop.")
    print()

    app.run(
        host="0.0.0.0",
        port=WEB_PORT,
        debug=False,
        threaded=True,
        use_reloader=False,
    )


if __name__ == "__main__":
    main()
