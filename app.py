from flask import Flask, redirect, render_template, request, session
from flask_login import LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from functools import wraps


app = Flask(__name__)

app.secret_key = "user"

# DB接続
engine = create_engine('sqlite:///project.db', connect_args={'check_same_thread': False})

# Session作成
Session = sessionmaker(bind=engine)
db_session = Session()

# Base
Base = declarative_base()

# テーブルクラスを定義
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

class Record(Base):
    __tablename__ = 'record'
    id = Column( Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    started_at = Column(String(50), nullable=False)
    ended_at = Column(String(50), nullable=False)


Base.metadata.create_all(engine)

# flask_loginの初期化
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# @login_requiredデコレータの実装
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def index():  # put application's code here
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # forget any user_id
    session.clear()

    # POST
    if request.method == "POST":

        session.clear()

        username = request.form.get("username")

        # ユーザー名が送信されたことを確認
        if not username:
            return apology()

        # パスワードが送信されたことを確認
        if not request.form.get("password"):
            return apology()

        # ユーザー名をデータベースに問い合わせる
        rows = db_session.query(User.id, User.name, User.password).filter_by(name=username).all()

        # ユーザー名が存在し、パスワードが正しいことを確認する
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology()

        # ユーザーのログインを記録。sessionにユーザーのuser_idを入れる
        session["user_id"] = rows[0][0]

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
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

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
        duplication = db_session.query(User.name).filter_by(name=name).all()

        if len(duplication) > 0:
            return apology()

        # 入力されたものをdbに入れる
        user = User(name=name, password=generate_password_hash(request.form.get("password")))
        db_session.add(user)
        db_session.commit()
        # db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",name, generate_password_hash(request.form.get("password")))

        # ログインしているユーザーを記憶する
        rows = db_session.query(User.id, User.name, User.password).filter_by(name=name).all()
        # rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0][0]

        # リダイレクト
        return redirect("/")

    else:
        return render_template("register.html")


if __name__ == '__main__':
    app.run()
    
    
def apology(message):  #TODO:
    return "<a>apology</a>"