import os
from flask import (
    redirect, render_template, request, send_from_directory, session)
from app import app
from repositories import books_repository
from repositories import users_repository
from services import source_service
from services import bibtex_service



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add(service = source_service):
    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        tag = request.form["tag"]
        title = request.form["title"]
        author = request.form["author"]
        publish_year = request.form["publish_year"]
        publisher = request.form["publisher"]
        service.insert_book(tag, title, author,
                                   publish_year, publisher, books_repository)

    return render_template("add.html")

@app.route("/list", methods=["GET"])
def list_sources():
    books = source_service.get_books(books_repository)
    return render_template("list.html", sources=books)

@app.route("/reset", methods=["GET"])
def empty_sources():
    source_service.delete_all_books(books_repository)
    return redirect("/")

@app.route("/reset_users", methods=["GET"])
def reset_users():
    users_repository.delete_all_users()
    return redirect("/")


@app.route("/bibtex", methods=["GET"])
def create_bibtex_file(service = bibtex_service):
    service.create_bibtex_file("references", books_repository)
    return render_template("bibtex.html")

@app.route("/download", methods=["GET"])
def download_bibtex_file():
    upload = os.path.join(app.root_path, "bibtex_files")
    return send_from_directory(upload, "references.bib")

@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        login_check = users_repository.login(username, password)
        if login_check is True:
            session["username"] = username
            return redirect("/")

    error = login_check
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/register", methods=["POST", "GET"])
def register():
    error = None

    if request.method == "GET":
        return render_template("register.html", error=error)

    if request.method == "POST":
        all_usernames = users_repository.get_all_usernames()
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if username in all_usernames:
            error = "Username has already been taken"
        elif password != password2:
            error = "Passwords do not match"
        else:
            users_repository.register(username, password)
            session["username"] = username
            return redirect("/")

    return render_template("register.html", error=error)
