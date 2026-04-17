from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Task
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey_change_in_production'
# SQLite database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure tables are created
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        
        if not title:
            flash('Title is required!', 'error')
        else:
            new_task = Task(title=title, description=description, status=status)
            db.session.add(new_task)
            db.session.commit()
            flash('Task successfully added!', 'success')
            return redirect(url_for('index'))
            
    return render_template('create.html')

@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    task = Task.query.get_or_404(id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        
        if not title:
            flash('Title is required!', 'error')
        else:
            task.title = title
            task.description = description
            task.status = status
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('index'))
            
    return render_template('update.html', task=task)

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
