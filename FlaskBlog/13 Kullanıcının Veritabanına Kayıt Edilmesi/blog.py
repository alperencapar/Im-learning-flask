from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

#https://wtforms.readthedocs.io/en/2.3.x/
#https://flask-wtf.readthedocs.io/en/stable/

#https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/

#! kullanıcı kayıt formu

class RegisterForm(Form):
    name = StringField("Ad Soyad", validators=[validators.Length(min = 4,max = 25)])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min = 5,max = 35)])       
    email = StringField("e-mail", validators=[validators.Email(message="Geçerli Email adresi girin")])  
    password = PasswordField("Parola:", validators=[
        validators.DataRequired(message="Parola Girin!"),
        validators.EqualTo(fieldname="confirm", message="Parola uyuşmuyor")
    ])
    confirm = PasswordField("Parolanızı Tekrar Giriniz")



app = Flask(__name__)




app.config["MYSQL_HOST"] = "localhost"              
app.config["MYSQL_USER"] = "root"                   
app.config["MYSQL_PASSWORD"] = ""                   
app.config["MYSQL_DB"] = "alpblog"                  
app.config["MYSQL_CURSORCLASS"] = "DictCursor"      

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


@app.route("/articles/<string:id>")  
def detail(id):
    return "Article Id:" + id



#!Kayıt Olma

@app.route("/register",methods=["GET","POST"])
def register():

    form = RegisterForm(request.form)   #kullanıcı kayıt formundan(class RegisterForm) obje oluşturuldu, post request yapıldığında verileri almamız için request.form yazıldı  
    if request.method == "POST" and form.validate():    #post metodu yapılıyorsa ve formlar gereken şartları karşılıyorsa

        name = form.name.data   #formdaki isim bilgisi değişkene atanıyor
        username = form.username.data    #formdaki kullanıcı adı bilgisi değişkene atanıyor
        email = form.email.data    #formdaki email bilgisi değişkene atanıyor
        password =  sha256_crypt.encrypt(form.password.data)    #formdaki şifre bilgisi, sha256 ile şifrelenip bir değişkene atanıyor

        cursor = mysql.connection.cursor()  #db'de işlem yapabilmek için cursor oluşturuldu

        sorgu = "Insert Into users(name,email,username,password) Values(%s,%s,%s,%s)"   #sorgu yapısı hazırlandı
        cursor.execute(sorgu,(name,email,username,password))    #sorgu yapıldı

        mysql.connection.commit()
        cursor.close()    

        return redirect(url_for("index"))   #index fonksiyonuna gönderme
    else:
        #get request
        return render_template("register.html", form=form)





if __name__ == "__main__":
    app.run(debug=True)