from flask import Flask, render_template,request,redirect,url_for,session
from database import get_connection
import mysql.connector
from config import my_key



app=Flask(__name__)

app.secret_key=my_key

@app.route("/home")
def home():
    try:
        conn=get_connection()
        conn.close()
        status="successfully connected to Database"
    except:
        status="Database error occured"
    if "username" in session:
        return render_template("home.html",info=status )
    else:
        return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():
    try:
        if request.method=="POST":
            name=request.form.get("name")
            username=request.form.get("username")
            email=request.form.get("email")
            password=request.form.get("password")
            
            conn=get_connection()
            cursor=conn.cursor()
            cursor.execute(
                "insert into users(name,username,email,password) values(%s,%s,%s,%s)",
                (name, username, email, password),
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            return redirect(url_for("login"))
    except mysql.connector.IntegrityError:
        return render_template("register.html",error="User already exists")

    return render_template("register.html",error="")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        identifier=request.form.get("identifier")
        password=int(request.form.get("password"))
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("select id from users where email=%s and password=%s",(identifier,password),)
        result=cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        
        if result:
            session["username"]=identifier
            return redirect(url_for("home"))
            

        return "login successfull"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    print("In logout")
    return redirect(url_for("login"))

        
if __name__ == "__main__":
    app.run(debug=True, port=5001, use_reloader=False)
