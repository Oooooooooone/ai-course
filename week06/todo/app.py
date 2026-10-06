import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from contextlib import closing

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with closing(get_db_connection()) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    with closing(get_db_connection()) as conn:
        todos = conn.execute('SELECT * FROM todos ORDER BY created_at DESC, id DESC').fetchall()
    error = request.args.get('error')
    return render_template('index.html', todos=todos, error=error)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    
    if not title or len(title) > 100:
        with closing(get_db_connection()) as conn:
            todos = conn.execute('SELECT * FROM todos ORDER BY created_at DESC, id DESC').fetchall()
        return render_template('index.html', todos=todos, error="제목은 1자 이상 100자 이하여야 합니다.")

    with closing(get_db_connection()) as conn:
        conn.execute(
            'INSERT INTO todos (title, completed, created_at) VALUES (?, ?, ?)',
            (title, False, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle(todo_id):
    with closing(get_db_connection()) as conn:
        todo = conn.execute('SELECT id, completed FROM todos WHERE id = ?', (todo_id,)).fetchone()
        if todo:
            new_completed = not todo['completed']
            conn.execute('UPDATE todos SET completed = ? WHERE id = ?', (new_completed, todo_id))
            conn.commit()
            return redirect(url_for('index'))
        else:
            return 'Not Found', 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)