from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

db.create_all()


@app.get("/")
def redirection():
    return redirect(url_for("home"))


@app.get("/posts")
def home():
    posts = db.session.query(Post).all()
    return render_template("base.html", posts=posts)


@app.post("/posts/create")
def create():
    title = request.form.get("title")
    content = request.form.get("content")
    new_post = Post(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/posts/<int:post_id>")
def detail(post_id):
    post = db.session.query(Post).filter(Post.id == post_id).first()
    return render_template("detail.html", post=post)


@app.get("/posts/<int:post_id>/edit")
def edit(post_id):
    post = db.session.query(Post).filter(Post.id == post_id).first()
    return render_template("update.html", post=post)


@app.post("/posts/<int:post_id>/update")
def update(post_id):
    post = db.session.query(Post).filter(Post.id == post_id).first()
    db.session.delete(post)
    title = request.form.get("title")
    content = request.form.get("content")
    new_post = Post(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for("detail"))


@app.get("/posts/<int:post_id>/delete")
def delete(post_id):
    post = db.session.query(Post).filter(Post.id == post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("home"))
