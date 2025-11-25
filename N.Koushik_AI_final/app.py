from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# -------- Task Model --------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    priority = db.Column(db.String(10), default="Medium")
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# ----------- Routes -----------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'priority': t.priority,
        'completed': t.completed
    } for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title', '')
    description = data.get('description', '')

    # 🧠 AI assist: detect priority keywords
    priority = "High" if any(word in title.lower() for word in ['urgent', 'important', 'today']) else "Medium"

    new_task = Task(title=title, description=description, priority=priority)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully!'})

@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
