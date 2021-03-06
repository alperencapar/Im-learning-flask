from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", islem = 1)    # index'e veri göndermesi yapıyoruz

@app.route("/about")
def about():
    return render_template("about.html") 

@app.route("/articles")
def articles():
    return render_template("articles.html")


if __name__ == "__main__":
    app.run(debug=True)