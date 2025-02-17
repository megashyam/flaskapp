from flask import Flask, render_template, request, redirect, url_for
import sqlite3,os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path=os.path.join(basedir,'users.db')

# SQLite setup function
def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT NOT NULL, 
                  password TEXT NOT NULL, 
                  firstname TEXT NOT NULL, 
                  lastname TEXT NOT NULL, 
                  email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect('/home/ubuntu/ec2FlaskApp/users.db')
        cursor = conn.cursor()

        # Check for the user in the database
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return f"Welcome {user[3]} {user[4]}, Email: {user[5]}"
        else:
            return "Login failed, please try again."
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        # Basic validation
        if not all([username, password, first_name, last_name, email]):
            return "All fields are required!", 400

        conn = None  # Initialize conn to None
        try:
            # Save to SQLite3 Database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
                (username, password, first_name, last_name, email)
            )
            conn.commit()
        except sqlite3.IntegrityError as e:
            return f"An error occurred: {str(e)}", 400
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}", 500
        finally:
            if conn:
                conn.close()  # Remove the trailing comma

        return render_template('success.html', first_name=first_name, last_name=last_name, email=email)

    return render_template('register.html')

@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return render_template('profile.html', user=user)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('Limerick-1.txt')
        return redirect(url_for('success'))
    return render_template('upload.html')

@app.route('/success')
def success():
    with open('Limerick-1.txt', 'r') as file:
        content = file.read()
        word_count = len(content.split())
    return render_template('success.html', first_name=first_name, last_name=last_name, email=email, word_count=word_count)


if __name__ == '__main__':
    app.run(debug=True)
