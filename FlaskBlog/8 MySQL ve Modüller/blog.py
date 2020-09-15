#pip install flask-mysqldb     - şuan için python 3.7 sürümünü destekliyor
#pip install flask-WTF      - form class'larını oluşturmak için kullanılacak
#pip install passlib    - kullanıcılar tablosuna ekleyeceğimiz parolayı şifreliyor

from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

#veritabanı adı: alpBlog
#veritabanı tablosu: users  - 5 sütün (id,name,email,username,password)(id primary key A_i: on)



app = Flask(__name__)


@app.route("/")
def index():

    #bir liste içerisinde 3 sözlük
    articles = [
        {"id":1, "title":"Deneme1", "content": "içerik1"},
        {"id":2, "title":"Deneme2", "content":"içerik2"},
        {"id":3, "title":"Deneme3", "content":"içerik3"}
    ]


    return render_template("index.html", articles = articles)    # numbers anahtar kelimesi ile numbers elemanlarını gönderiyoruz






@app.route("/about")
def about():
    return render_template("about.html") 


@app.route("/articles")
def articles():
    return render_template("articles.html")



@app.route("/articles/<string:id>")  #altındaki fonksiyondan id parametresini alıyor
def detail(id):
    return "Article Id:" + id
#http://127.0.0.1:5000/articles/1 adresine gittiğimizde     -- Article Id:1 -- yazısını görüyoruz


if __name__ == "__main__":
    app.run(debug=True)