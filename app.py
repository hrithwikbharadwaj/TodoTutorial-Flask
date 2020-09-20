
from flask import Flask, request, Response, render_template, redirect, url_for
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Todo(db.Model):
   id= db.Column(db.Integer, primary_key=True)
   title=db.Column(db.String(100))
   complete= db.Column(db.Boolean)

@app.route('/')
def index():
   todo_list= Todo.query.all()
   print(todo_list)
   return render_template('base.html',todos=todo_list)

@app.route('/add',methods=["POST"])
def add():
   name=request.form.get('title')
   new_todo= Todo(title=name,complete=False)
   db.session.add(new_todo)   
   db.session.commit()
   return redirect(url_for("index"))

## Dynamic Routing - We pass the todo id from jinja and then filter the row we want and mark the item as completed
@app.route('/update/<int:todo_id>')
def update(todo_id):
   todo=Todo.query.filter_by(id=todo_id).first()
   todo.complete= not todo.complete
   db.session.commit()
   return redirect(url_for("index")) 

## Dynamic Routing - We pass the todo id from jinja and then filter the row we want and delete the item
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
   todo=Todo.query.filter_by(id=todo_id).first()
   db.session.delete(todo)
   db.session.commit()
   return redirect(url_for("index")) 




if __name__ == "__main__":
   db.create_all()
   app.run(debug=True)



