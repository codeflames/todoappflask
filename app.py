from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(125), nullable=False)
    complete = db.Column(db.Boolean)


@app.route("/")
def index():
    todo_list = Todo.query.all()
    return render_template("tasks.html", todos = todo_list)

@app.route("/completed")
def completed():
    todo_list = Todo.query.all()
    return render_template("completed.html", todos = todo_list)

@app.route("/addTask", methods = ["GET", "POST"])
def addTask():
    if request.method == "GET":
        return render_template("addTasks.html")
    else:
        todo = request.form.get("task")
        todo_item = Todo(title=todo, complete=False)
        db.session.add(todo_item)
        db.session.commit()
        return redirect("/")

@app.route("/complete<int:todo_id>")
def complete(todo_id):
    todo =Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect("/")

@app.route("/delete<int:todo_id>")
def delete(todo_id):
    todo =Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)