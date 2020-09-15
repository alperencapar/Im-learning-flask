from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

#https://wtforms.readthedocs.io/en/2.3.x/
#https://flask-wtf.readthedocs.io/en/stable/



#! kullanıcı kayıt formu

class RegisterForm(Form):
    name = StringField("Ad Soyad", validators=[validators.Length(min = 4,max = 25)])        #<input type="text">    4 karaterden küçük 25 karakterden büyük olamaz
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min = 5,max = 35)])       
    email = StringField("e-mail", validators=[validators.Email(message="Geçerli Email adresi girin")])  #pip install email_validator
    password = PasswordField("Parola:", validators=[
        validators.DataRequired(message="Parola Girin!"),
        validators.EqualTo(fieldname="confirm", message="Parola uyuşmuyor")
    ])
    confirm = PasswordField("Parolanızı Tekrar Giriniz")





app = Flask(__name__)


#flask-mysqldb bağlantısı

app.config["MYSQL_HOST"] = "localhost"              #db konumu
app.config["MYSQL_USER"] = "root"                   #db kullanıcı
app.config["MYSQL_PASSWORD"] = ""                   #db şifre
app.config["MYSQL_DB"] = "alpblog"                  #database adı
app.config["MYSQL_CURSORCLASS"] = "DictCursor"      #bilgilerin düzenli gelmesi

mysql = MySQL(app)

@app.route("/")
def index():

    articles = [
        {"id":1, "title":"Deneme1", "content": "içerik1"},
        {"id":2, "title":"Deneme2", "content":"içerik2"},
        {"id":3, "title":"Deneme3", "content":"içerik3"}
    ]


    return render_template("index.html", articles = articles) 





@app.route("/about")
def about():
    return render_template("about.html") 


@app.route("/articles")
def articles():
    return render_template("articles.html")



@app.route("/articles/<string:id>")  #altındaki fonksiyondan id parametresini alıyor
def detail(id):
    return "Article Id:" + id


if __name__ == "__main__":
    app.run(debug=True)