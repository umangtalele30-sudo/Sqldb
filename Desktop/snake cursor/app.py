from flask import Flask, render_template, jsonify
import pyautogui
import threading
import time
import math

pyautogui.FAILSAFE = True

app = Flask(__name__)

running = False
movement_thread = None


def snake_movement():
    global running

    screen_width, screen_height = pyautogui.size()

    amplitude = 200
    wave_length = 500
    center_y = screen_height // 2

    while running:

        # LEFT → RIGHT
        for x in range(0, screen_width, 5):

            if not running:
                return

            y = center_y + int(
                amplitude * math.sin(
                    x / wave_length * 2 * math.pi
                )
            )

            # Smaller duration = faster
            pyautogui.moveTo(
                x,
                y,
                duration=0.01
            )

        # RIGHT → LEFT
        for x in range(screen_width - 1, 0, -5):

            if not running:
                return

            y = center_y + int(
                amplitude * math.sin(
                    x / wave_length * 2 * math.pi
                )
            )

            pyautogui.moveTo(
                x,
                y,
                duration=0.50
            )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start")
def start():

    global running, movement_thread

    if not running:

        running = True

        movement_thread = threading.Thread(
            target=snake_movement,
            daemon=True
        )

        movement_thread.start()

    return jsonify({
        "status": "started"
    })


@app.route("/stop")
def stop():

    global running

    running = False

    # Immediately stop any current PyAutoGUI movement
    pyautogui.moveTo(
        pyautogui.position().x,
        pyautogui.position().y,
        duration=0
    )

    return jsonify({
        "status": "stopped"
    })


if __name__ == "__main__":
    app.run(
        debug=False,
        threaded=True
    )