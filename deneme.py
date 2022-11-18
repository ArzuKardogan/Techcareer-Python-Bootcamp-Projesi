from flask import Flask,render_template,flash,redirect,url_for,session,request,logging
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,IntegerField, validators
from passlib.hash import sha256_crypt
from functools import wraps
app = Flask(__name__)
app.secret_key="yemek"

class RegisterForm(Form):
    name=StringField("İsim Soyisim",validators=[validators.Length(min=6, max=30)])
    username = StringField("Kullanıcı adı",validators=[validators.Length(min=6, max=30)])
    email = StringField("E posta",validators=[validators.email(message="Geçerli bir email adresi giriniz")])
    password = PasswordField("Parola",validators=[
        validators.DataRequired("Lütfen bir parola belileyin"),
        validators.length(min=8),
        validators.EqualTo(fieldname="confirm",message="Parolanız Uyuşmuyor")        
    ])
    confirm=PasswordField("Parola Doğrula")

class LoginForm(Form):
    username=StringField("Kullanıcı adı")
    password=PasswordField("Parola")


class UpdateProfileForm(Form):
    name=StringField("İsim Soyisim",validators=[validators.Length(min=6, max=30)])
    username = StringField("Kullanıcı adı",validators=[validators.Length(min=6, max=30)])
    email = StringField("E posta",validators=[validators.email(message="Geçerli bir email adresi giriniz")])

class YemekTarifiForm(Form):
    tarifadi=StringField("Tarif Adı",validators=[validators.Length(min=6, max=30)])
    tarif = TextAreaField("Tarif",validators=[validators.Length(min=8)])
    tarifkategorisi = IntegerField("Tarif Kategorisi",validators=[validators.Length(min=8)])

class KategoriForum(Form):
    kategoriAdi=StringField("Kategori adı")

def login_required(f):
    @wraps(f)
    def decorator_function(*args,**kwargs):
        if "logged_in" in session:
            return f(*args,**kwargs)
        else:
            flash("Bu sayfayı görüntülemek için giriş yapmanız lazım...","danger")
            return redirect(url_for("login"))
    return decorator_function

#Db bağlantı konfigürasyonu başladı
app.config["MYSQL_HOST"] ="localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "blog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
#Db bağlantı konfigürasyonu bitti

@app.route("/")
def index():
   
    return render_template("index.html")

    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/yemektarifi/<string:id>")
def tarif(id):
    cursor=mysql.connection.cursor()
    sorgu="Select * from yemektarifi where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        tarif = cursor.fetchone()
        return render_template("tarif.html",tarif=tarif)
    else:
        return render_template("tarif.html")

@app.route("/kategoriler")
def kategoriler():
    cursor = mysql.connection.cursor()
    sorgu = "Select * from yemekkategori"
    result=cursor.execute(sorgu)
    if result >0:
        kategoriler=cursor.fetchall()
        return render_template("tarifler.html",kategoriler=kategoriler)
    else:
        return render_template("tarifler.html")


@app.route("/yemektarifleri/<string:id>")
def tarifler(id):
    cursor=mysql.connection.cursor()
    sorgu="Select * from yemektarifi where kategori_id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        tarifler = cursor.fetchall()
        return render_template("yemektarifi.html",tarifler=tarifler)
    else:
        return render_template("yemektarifi.html")

@app.route("/user/<string:id>")
def users(id):
    cursor=mysql.connection.cursor()
    sorgu="Select * from user where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        user = cursor.fetchone()
        return render_template("user.html",user=user)
    else:
        return render_template("user.html")

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if(request.method=="POST" and form.validate()):
        name=form.name.data
        username=form.username.data
        email=form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()
        sorgu= "Insert into user(name,email,username,password) VALUES(%s,%s,%s,%s) "
        cursor.execute(sorgu,(name,email,username,password))
        mysql.connection.commit()
        cursor.close()
        flash("Başarıyla kayıt oldunuz...","success")
        return redirect(url_for("login"))

    else:
        return render_template("register.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if(request.method=="POST"):
        username=form.username.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        sorgu= "Select * from user where username = %s"
        result=cursor.execute(sorgu,(username,))

        if result>0:
            data=cursor.fetchone()
            real_passw=data["password"]
            if sha256_crypt.verify(password,real_passw):
                flash("Başarılı giriş yaptınız..","success")
                session["logged_in"] = True
                session["username"] = username
                """
                Yönetici girişi kontrolu
                if data["rol_id"]==2:
                    return redirect(url_for("admin"))
                else:
                    #session["id"] = data["id"]
                    return redirect(url_for("index"))"""
                return redirect(url_for("index"))     
            else:
                flash("Parolanızı yanlış girdiniz","danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı bulunmuyor...","danger")
            return redirect(url_for("login"))

    return render_template("login.html",form=form)



@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    sorgu= "Select * from yemektarifi where tarifi_yazan = %s"
    result = cursor.execute(sorgu,(session["username"],))
    if result>0:
        tarifler = cursor.fetchall()
        return render_template("dashboard.html",tarifler=tarifler)
    else:
        return render_template("dashboard.html")

@app.route("/kategoriduzenle")
@login_required
def dashboard2():
    cursor = mysql.connection.cursor()
    sorgu= "Select * from yemekkategori"
    result = cursor.execute(sorgu)
    if result>0:
        kategoriler = cursor.fetchall()
        return render_template("kategoriduzenle.html",kategoriler=kategoriler)
    else:
        return render_template("kategoriduzenle.html")

@app.route("/kategoriekle",methods=["GET","POST"])
@login_required
def kategoriekle():
    form=KategoriForum(request.form)
    if request.method=="POST" and form.validate:
        kategoriAdi = form.kategoriAdi.data
        cursor = mysql.connection.cursor()
        sorgu="Insert into yemekkategori (kategori_adi) VALUES(%s)"
        cursor.execute(sorgu,(kategoriAdi,))
        mysql.connection.commit()
        cursor.close()
        flash("Kategori Başarılı bir şekilde kaydedildi...","success")
        return redirect(url_for("dashboard"))
    return render_template("kategoriekle.html",form=form)

@app.route("/yemektarifiekle",methods=["GET","POST"])
@login_required
def yemektarifiekle():
    form=YemekTarifiForm(request.form)
    if request.method=="POST" and form.validate:
        tarifadi = form.tarifadi.data
        tarif = form.tarif.data
        tarifkategorisi = form.tarifkategorisi.data
        cursor = mysql.connection.cursor()
        sorgu="Insert into yemektarifi (yemek_adi,tarifi_yazan,tarif,kategori_id) VALUES(%s,%s,%s,%s)"
        cursor.execute(sorgu,(tarifadi,session["username"],tarif,tarifkategorisi))
        mysql.connection.commit()
        cursor.close()
        flash("Makele Başarılı bir şekilde kaydedildi...","success")
        return redirect(url_for("dashboard"))
    return render_template("yemektarifiekle.html",form=form)


@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor=mysql.connection.cursor()
    sorgu="Select * from yemektarifi where tarifi_yazan = %s and id = %s"
    result = cursor.execute(sorgu,(session["username"],id))
    if result > 0:
        sorgu2="Delete from yemektarifi where id = %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()

        return redirect(url_for("dashboard"))
    else:
        flash("Böyle bir yemek tarifi yok veya bu işlem için yetkiniz yok","danger")
        return redirect(url_for("dashboard"))

@app.route("/deletekategori/<string:id>")
@login_required
def deletekategori(id):
    cursor=mysql.connection.cursor()
    sorgu="Select * from yemekkategori where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        sorgu2="Delete from yemekkategori where id = %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()

        return redirect(url_for("dashboard2"))
    else:
        flash("Böyle bir yemek kategorisi yok veya bu işlem için yetkiniz yok","danger")
        return redirect(url_for("dashboard2"))

@app.route("/editprofile",methods=["GET","POST"])
@login_required
def editprofile():
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        sorgu = "Select * from user where  username = %s"
        result = cursor.execute(sorgu,(session["username"],))
        if result == 0:
            flash("Böyle bir user yok veya bu işlem için yetkiniz yok","danger")
            session.clear()
            return redirect(url_for("index"))
        else:
            user=cursor.fetchone()
            form =UpdateProfileForm()

            form.name.data = user["name"]
            form.email.data = user["email"]
            form.username.data = user["username"]
            return render_template("updateUser.html",form = form)
    else:
        form = UpdateProfileForm(request.form)
        newName=form.name.data
        newUserEmail = form.email.data
        newUserName=form.username.data
        sorgu2="Update user Set name = %s, email = %s, username = %s where username = %s"
        sorgu3="Update yemektarifi Set tarifi_yazan = %s where tarifi_yazan = %s"
        cursor= mysql.connection.cursor()
        cursor.execute(sorgu2,(newName,newUserEmail,newUserName,(session["username"])))
        mysql.connection.commit()
        cursor.execute(sorgu3,(newUserName,(session["username"])))
        mysql.connection.commit()
        flash("Kullanıcı profiliniz başarılı bir şekilde güncellendi","success")
        session.clear()
        return redirect(url_for("index"))



@app.route("/edit/<string:id>",methods=["GET","POST"])
@login_required
def edit(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        sorgu = "Select * from yemektarifi where id = %s and tarifi_yazan = %s "
        result = cursor.execute(sorgu,(id,session["username"]))
        if result == 0:
            flash("Böyle bir yemek tarifi yok veya bu işlem için yetkiniz yok","danger")
            session.clear()
            return redirect(url_for("index"))
        else:
            tarif=cursor.fetchone()
            form =YemekTarifiForm()

            form.tarifadi.data = tarif["yemek_adi"]
            form.tarif.data = tarif["tarif"]
            form.tarifkategorisi.data = tarif["kategori_id"]
        
            return render_template("update.html",form = form)
    else:
        form = YemekTarifiForm(request.form)
        newYemekAdi=form.tarifadi.data
        newYemekTarifi=form.tarif.data
        newKategori=form.tarifkategorisi.data
        sorgu2="Update yemektarifi Set yemek_adi = %s, tarif = %s, kategori_id = %s where id=%s"
        cursor= mysql.connection.cursor()
        cursor.execute(sorgu2,(newYemekAdi,newYemekTarifi,newKategori,id))
        mysql.connection.commit()
        flash("Tarif Başarılı bir şekilde güncellendi","success")
        return redirect(url_for("dashboard"))

@app.route("/editkategori/<string:id>",methods=["GET","POST"])
@login_required
def editkategori(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        sorgu = "Select * from yemekkategori where id = %s"
        result = cursor.execute(sorgu,(id,))
        if result == 0:
            flash("Böyle bir yemek kategorisi yok veya bu işlem için yetkiniz yok","danger")
            session.clear()
            return redirect(url_for("index"))
        else:
            kategori=cursor.fetchone()
            form =KategoriForum()

            form.kategoriAdi.data = kategori["kategori_adi"]
          
        
            return render_template("updatekategori.html",form = form)
    else:
        form = KategoriForum(request.form)
        newKategoriAdi=form.kategoriAdi.data
        sorgu2="Update yemekkategori Set kategori_adi = %s where id=%s"
        cursor= mysql.connection.cursor()
        cursor.execute(sorgu2,(newKategoriAdi,id))
        mysql.connection.commit()
        flash("Tarif Başarılı bir şekilde güncellendi","success")
        return redirect(url_for("dashboard2"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
@app.route("/search",methods=["GET","POST"])
def search():
    if request == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sorgu = "Select * from yemekkategori where kategori_adi like '%" + keyword + "%'"
        result = cursor.execute(sorgu)
        if result == 0:
            flash("Aradığınız kelimeyi içerene yemek kategorisi yok","warning")
            return redirect(url_for("tarifler"))
        else:
            kategoriler=cursor.fetchall()
            return render_template("tarifler.html",kategoriler=kategoriler)
if __name__ =="__main__":
    app.run(debug = True)