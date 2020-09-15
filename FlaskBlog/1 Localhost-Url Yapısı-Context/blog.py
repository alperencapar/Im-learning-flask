#pip install flask
from flask import Flask,render_template     # render_template, bulunduğu klasörde, templates klasörü arıyor

app = Flask(__name__)   #


@app.route("/")          # * ben bu adrese gitmek istiyorum demek
def index():             # ! @app.route'un bir fonksiyona bağlanması gerekiyor
    # sayi = 10
    # sayi2 = 20


    article = dict()
    article["title"] = "Deneme"
    article["body"] = "Deneme 123"
    article["author"] = "Alperen"

    return render_template("index.html",article = article)  # ! sayi değişkenini number key(anahatarı) ile gönderdik. key ile html tarafında kullanabiliriz ! 


@app.route("/about")
def about():
    return "Hakkımda"


@app.route("/about/alp")
def alp():
    return "Alp Hakkında"


if __name__ == "__main__":      # *dışarıdan import edilip edilmediğini kontrol ediyoruz
    app.run(debug=True)






















