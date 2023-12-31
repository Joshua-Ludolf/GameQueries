from flask import *
import mysql.connector

app = Flask(__name__, static_url_path='/static')

# Configure db
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jaguarJosh24!",
    database="gamestock"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search.html', methods=['GET', 'POST'])
def search():
    game = None
    if request.method == "POST":
        title = request.form.get('title')
        try:
            cur = cnx.cursor(dictionary=True)
            cur.execute("SELECT * FROM GAME WHERE TITLE = %s", (title,))
            game = cur.fetchone()
        finally:
            if cur:
                cur.close()
    return render_template('search.html', game=game)

if __name__ == '__main__':
    app.run(host='localhost')