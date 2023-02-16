from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL    # TODO: cs50の部分書き換える
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import os


app = Flask(__name__)

db = SQL("sqlite:///project.db")    # TODO: cs50書き換え

""" 記事参考
# Engine作成
Engine = create_engine(
    "postgresql://postgres:postgres@sqlalchemy-db:5432/sqlalchemy",
    encoding="utf-8",
    echo=False
)

# Session作成
session = sessionmaker(
    autocommit=False,
    
)
"""

""" youtube参考
database_file = os.path.join(os.path.abspath(os.getcwd()), 'project.db')

# engineをセット
engine = create_engine('sqlite:///' + database_file,
                       convert_unicode=True, echo=True)
# session: dbとのつながりを確立してから切断するまでの一連の流れ。dbとpyを接続する
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False
        bind=engine
    )
)

# ベースとなるDBを作成（動画12:45）
Base = declarative_base()
Base.query = db_session.query_property()

# データベースを初期化する。matadata: データベースの情報を保持しているオブジェクト。
Base.metadata.create_all(bind=engine)
"""


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/login", methods=["GET", "POST"])
def login():

    # forget any user_id
    session.clear()

    # POST
    if request.method == "POST":

        username = request.form.get("username")

        # ユーザー名が送信されたことを確認
        if not username:
            return apology()

        # パスワードが送信されたことを確認
        if not request.form.get("password"):
            return apology()

        # ユーザー名をデータベースに問い合わせる
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # ユーザー名が存在し、パスワードが正しいことを確認する
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology()

        # ユーザーのログインを記録。sessionにユーザーのuser_idを格納
        session["user_id"] = rows[0]["id"]

        # homeページにリダイレクト
        return redirect("/")

    # GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # ログイン画面へリダイレクト
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # POST
    if request.method == "POST":

        # usernameが送信されたか
        if not request.form.get("username"):
            return apology()

        # パスワードが送信されたか
        elif not request.form.get("password"):
            return apology()

        # パスワードが一致するか
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology()

        # usernameがすでに使われていないか
        name = request.form.get("username")
        duplication = (db.execute(
            "SELECT username from users where username = ? LIMIT 1", name))
        if len(duplication) > 0:
            return apology("username is not available", 400)

        # 入力されたものをdbに入れる
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   name, generate_password_hash(request.form.get("password")))

        # ログインしているユーザーを記憶する
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # リダイレクト
        return redirect("/")

    else:
        return render_template("register.html")


if __name__ == '__main__':
    app.run()
    
    
def apology():  #TODO:
    return