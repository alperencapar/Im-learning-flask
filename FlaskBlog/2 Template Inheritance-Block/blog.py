from flask import Flask,render_template     # render_template, bulunduğu klasörde, templates klasörü arıyor

app = Flask(__name__)   #


@app.route("/")          # * ben bu adrese gitmek istiyorum demek
def index():             # ! @app.route'un bir fonksiyona bağlanması gerekiyor
    
    return render_template("index.html")  # ! index.html yazıyoruz. index.html, layout.html'den kalıtım(inherit) yapıyor ! 


@app.route("/about")
def about():
    return "Hakkımda"



if __name__ == "__main__":      # *dışarıdan import edilip edilmediğini kontrol ediyoruz
    app.run(debug=True)






















