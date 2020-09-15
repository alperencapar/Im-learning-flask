from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps

#https://wtforms.readthedocs.io/en/2.3.x/
#https://flask-wtf.readthedocs.io/en/stable/

#https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/
#https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/



#! Kullanıcı Giriş Decorator'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:   
            flash("Bu sayfayı görüntülemek için giriş yapın","info error")
            return redirect(url_for("login"))
    return decorated_function



#? WTF FORM KISMI

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

class LoginForm(Form):
    username = StringField("Kullanıcı Adı:")
    password = PasswordField("Parola")





app = Flask(__name__)
app.secret_key = "alpblog"      #message flashing özelliğini kullanabilmek için gerekli


#! mysql bağlantı ayarları
app.config["MYSQL_HOST"] = "localhost"              
app.config["MYSQL_USER"] = "root"                   
app.config["MYSQL_PASSWORD"] = ""                   
app.config["MYSQL_DB"] = "alpblog"                  
app.config["MYSQL_CURSORCLASS"] = "DictCursor"      

mysql = MySQL(app)

@app.route("/")
def index():

    cursor = mysql.connection.cursor()
    sorgu = "Select * From articles"
    result = cursor.execute(sorgu)

    if result ==0:
        flash("Henüz Herhangi Bir Makale Bulunmuyor","info alert")
    else:
        articles = cursor.fetchall()
        return render_template("index.html", articles = articles) 


@app.route("/about")
def about():
    return render_template("about.html") 


#!Makale Sayfası
@app.route("/articles")
def articles():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From articles"
    result = cursor.execute(sorgu)
    if result > 0:
        articles = cursor.fetchall()
        return render_template("articles.html",articles = articles)
    else:
        return render_template("articles.html")



#!Kayıt Olma
@app.route("/register",methods=["GET","POST"])
def register():

    form = RegisterForm(request.form)     
    if request.method == "POST" and form.validate():

        name = form.name.data
        username = form.username.data    
        email = form.email.data    
        password =  sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()

        sorgu = "Insert Into users(name,email,username,password) Values(%s,%s,%s,%s)"
        cursor.execute(sorgu,(name,email,username,password))

        mysql.connection.commit()
        cursor.close()    

        #!message flash işlemleri
        flash("Başarıyla Kayıt oldunuz","info success")

        return redirect(url_for("login"))   #index fonksiyonuna gönderme
    else:
        #get request
        return render_template("register.html", form=form)


#!Login işlemi

@app.route("/login", methods=["GET","POST"])
def login():
    
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data           #input üzerindeki kullanıcı adı bilgisi username değişkenine atanıyor
        password_entered = form.password.data   #input üzerindeki şifre bilgisi password_entered değişkenine atanıyor

        cursor = mysql.connection.cursor()      #mysql üzerinde işlem yapabilmek için cursor oluşturuluyor

        sorgu = "Select * FROM users where username = %s"       #kullanıcı adı sorgu yapısı hazırlandı
        result = cursor.execute(sorgu,(username,))              #kullanıcı adı sorgulaması yapılıp result değişkenine atandı
        if result > 0:  #kullanıcı adı sistemde bulunuyorsa
            data = cursor.fetchone()             #database'den gelen bilgi alındı
            real_password = data["password"]    #db'deki password bilgisi değişkene atandı
            if sha256_crypt.verify(password_entered,real_password): #girilen ile db'deki şifre karşılaştırılması yapılıyor
                flash("Giriş yapıldı","info success")

                #! session başlatma
                session["logged_in"] = True
                session["username"] = username
                 
                return redirect(url_for("index"))

            else:
                flash("Parola yanlış","error")
                return redirect(url_for("login"))

        else:   #kullanıcı adı sistemde bulunmuyorsa
            flash("Böyle bir kullanıcı adı bulunamadı","info error")
            return redirect(url_for("login"))

    return render_template("login.html", form = form)    


#!Detay Sayfası

@app.route("/article/<string:id>")
def article(id):
    cursor = mysql.connection.cursor()

    sorgu = "Select * From articles where id = %s"

    result = cursor.execute(sorgu,(id,))
    if result > 0:
        article = cursor.fetchone()
        return render_template("article.html",article = article)
    else:
        return render_template("article.html")



#!logout işlemi
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():

    cursor = mysql.connection.cursor()

    sorgu = "Select * From articles where author = %s"

    result = cursor.execute(sorgu,(session["username"],))
    
    if result > 0:
        articles = cursor.fetchall()
        return render_template("dashboard.html", articles = articles)
    else:
        return render_template("dashboard.html")


#! Makale Ekleme
@app.route("/addarticle", methods = ["GET","POST"])
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data

        cursor = mysql.connection.cursor()

        sorgu = "Insert Into articles(title,author,content) Values(%s,%s,%s)"

        cursor.execute(sorgu,(title,session["username"],content))
        mysql.connection.commit()
        cursor.close()
        flash("Makale Başarıyla Eklendi","info success")
        return redirect(url_for("dashboard"))

    return render_template("addarticle.html",form = form)


#! Makale Silme
@app.route('/delete/<string:id>')
@login_required
def delete(id):
    cursor = mysql.connection.cursor()

    sorgu = "Select * From articles where author = %s and id = %s"

    result = cursor.execute(sorgu,(session["username"],id))

    if result > 0:
        sorgu2 = "Delete from articles where id = %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        return redirect(url_for("dashboard"))
    else:
        flash("Makale Yok veya Silmeye Yetkiniz Yok","info error")
        return redirect(url_for("index"))


#! Makale Güncelleme
@app.route('/edit/<string:id>', methods = ["GET", "POST"])
@login_required
def update(id):
    if request.method == "GET":
        
        cursor = mysql.connection.cursor()

        sorgu = "Select * From articles where id = %s and author = %s"
        result = cursor.execute(sorgu,(id,session["username"]))

        if result == 0:
            flash("Böyle bir Makale Bulunmuyor veya Yetkiniz Yok", "info error")
            return redirect(url_for("index"))
        else:
            article = cursor.fetchone()
            form = ArticleForm()
            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html", form = form)
        
    else:
        #? Metod post
        form = ArticleForm(request.form)
        newTitle = form.title.data
        newContent = form.content.data

        sorgu2 = "Update articles Set title = %s, content = %s where id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sorgu2,(newTitle,newContent,id))
        mysql.connection.commit()

        flash("Makale GÜncellendi","info success")
        return redirect(url_for("dashboard"))


#! Makale Form

class ArticleForm(Form):    #(Form) inheritance
    title = StringField("Makale Başlığı",validators=[validators.Length(min=5)])
    content = TextAreaField("Makale içeriği", validators=[validators.Length(min=10)])


#! Makale Arama
@app.route("/search", methods =["GET","POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")
        
        cursor = mysql.connection.cursor()

        sorgu = "Select * From articles Where title Like '%" + keyword +"%'"

        result = cursor.execute(sorgu)

        if result == 0:
            flash("Böyle bir makale bulunamadı","info alert")
            return redirect(url_for("articles"))
        else:
            articles = cursor.fetchall()
            return render_template("articles.html", articles = articles)


if __name__ == "__main__":
    app.run(debug=True)