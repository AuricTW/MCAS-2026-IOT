from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

images = [
    "images/pic1.jpg",
    "images/pic2.jpg",
    "images/pic3.jpg"
]

current_index = 0  # 全域索引

@app.route("/")
def index():
    global current_index
    img = images[current_index]
    return render_template("index.html", image=img, idx=current_index, total=len(images))

@app.route("/next")
def next_img():
    global current_index
    current_index += 1
    return redirect(url_for("index"))

@app.route("/prev")
def prev_img():
    global current_index
    current_index -= 1
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
