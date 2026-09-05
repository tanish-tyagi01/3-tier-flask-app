from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.secret_key = "your-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/flask_app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)



    # The below code creates a relationship between both tables so that without any column of user in todo we can still get the data of user.
    todos = db.relationship(
        "Todo",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan" # It will delete relative tasks of an user if it get deleted.
    )


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("home"))
    return redirect(url_for("register"))


@app.route("/index")
@login_required
def home():
    todos = Todo.query.filter_by(user_id=session["user_id"]).order_by(Todo.id.desc()).all()
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
@login_required
def add_todo():
    task = request.form.get("task", "").strip()

    if task:
        todo = Todo(task=task, user_id=session["user_id"])
        db.session.add(todo)
        db.session.commit()
        flash("Task added successfully.", "success")

    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>", methods = ["POST"])
@login_required
def update_todo(todo_id):
    new_task = request.form.get("task", " ").strip()

    todo = Todo.query.filter_by(
        id = todo_id,
        user_id = session["user_id"]
    ).first()

    if todo and new_task:
        todo.task = new_task
        db.session.commit()
        flash("Message replace wit new message", "success")
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.filter_by(
        id=todo_id,
        user_id=session["user_id"]
    ).first()

    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash("Task deleted.", "success")

    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if password != confirm_password:
            flash("Both passwords do not match. Please try again.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("register"))

        new_user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        """It searches the User table for an user whose email matches the given email and .first() serches the first object and None if no one found"""
        user = User.query.filter_by(email=email).first()
          

        if user and user.password == password:
            session["user_id"] = user.id
            session["user_name"] = user.name
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("home"))

        flash("Invalid email or password.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)


print("Hello Tanish, you did great job")
