from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ===== DATABASE SETUP =====
def init_db():
    conn = sqlite3.connect('visitors.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            visit_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ===== HOME PAGE =====
@app.route('/')
def home():
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM visitors')
    count = c.fetchone()[0]
    conn.close()

    return render_template("index.html", count=count)

# ===== ABOUT PAGE =====
@app.route('/about')
def about():
    return render_template("about.html")

# ===== CONTACT PAGE =====
@app.route('/contact')
def contact():
    return render_template("contact.html")

# ===== SIGN-IN PAGE =====
@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():

    if request.method == 'POST':
        name = request.form['name']

        conn = sqlite3.connect('visitors.db')
        c = conn.cursor()

        c.execute(
            "INSERT INTO visitors (name, visit_time) VALUES (?, ?)",
            (name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("signin.html")
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sign In</title>
        <style>
            body { background: #1a1a2e; color: #fff; font-family: Arial; text-align: center; padding: 50px; }
            h1 { color: #e94560; }
            .container { background: #16213e; padding: 40px; border-radius: 10px; max-width: 400px; margin: auto; }
            input, button { padding: 10px; font-size: 16px; border-radius: 5px; margin: 5px; }
            input { width: 80%; background: #2a2a4e; color: #fff; border: 1px solid #4fc3f7; }
            button { background: #e94560; color: #fff; border: none; cursor: pointer; }
            a { color: #4fc3f7; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Sign In</h1>
            <form method="POST">
                <input type="text" name="name" placeholder="Enter your name" required>
                <br>
                <button type="submit">Submit</button>
            </form>
            <p><a href="/">Home</a></p>
        </div>
    </body>
    </html>
    """

# ===== VISITORS LIST PAGE =====
@app.route("/visitors")
def visitors():

    conn = sqlite3.connect("visitors.db")

    c = conn.cursor()

    c.execute("SELECT * FROM visitors")

    visitors = c.fetchall()

    conn.close()

    return render_template(
        "visitors.html",
        visitors=visitors
    )
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Visitor List</title>
        <style>
            body { background: #1a1a2e; color: #fff; font-family: Arial; text-align: center; padding: 50px; }
            h1 { color: #e94560; }
            ul { list-style: none; padding: 0; }
            li { background: #16213e; padding: 10px; margin: 5px auto; border-radius: 5px; max-width: 400px; }
            a { color: #4fc3f7; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>Visitor List</h1>
        <ul>
    """
    for name, time in data:
        html += "<li><strong>" + name + "</strong> - " + time + "</li>"
    
    html += """
        </ul>
        <p><a href="/">Home</a></p>
    </body>
    </html>
    """
    return html

# ===== SEARCH PAGE =====
@app.route("/search", methods=["GET", "POST"])
def search():

    visitors = []

    if request.method == "POST":

        name = request.form["name"]

        conn = sqlite3.connect("visitors.db")

        c = conn.cursor()

        c.execute(
            "SELECT * FROM visitors WHERE name LIKE ?",
            ('%' + name + '%',)
        )

        visitors = c.fetchall()

        conn.close()

    return render_template(
        "search.html",
        visitors=visitors
    )
 
    # GET request - show search form
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search Visitors</title>
        <style>
            body { background: #1a1a2e; color: #fff; font-family: Arial; text-align: center; padding: 50px; }
            h1 { color: #e94560; }
            .container { background: #16213e; padding: 40px; border-radius: 10px; max-width: 400px; margin: auto; }
            input, button { padding: 10px; font-size: 16px; border-radius: 5px; margin: 5px; }
            input { width: 80%; background: #2a2a4e; color: #fff; border: 1px solid #4fc3f7; }
            button { background: #e94560; color: #fff; border: none; cursor: pointer; }
            a { color: #4fc3f7; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Search Visitors</h1>
            <form method="POST">
                <input type="text" name="search" placeholder="Enter a name to search" required>
                <br>
                <button type="submit">Search</button>
            </form>
            <p><a href="/">Home</a></p>
        </div>
    </body>
    </html>
    """
# ===== CUSTOM 404 PAGE =====

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
