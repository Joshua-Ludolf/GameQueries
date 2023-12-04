from flask import *
import mysql.connector

app = Flask(__name__, static_url_path='/static')

# Configure db
cnx = mysql.connector.connect(
    host="sql5.freesqldatabase.com",
    user="sql5665870",
    password="H8plu1kJh2",
    database="sql5665870"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search.html', methods=['GET', 'POST'])
def search(): 
    games = None
   
    if request.method == "POST":
        title = request.form.get('title')
        try:
            cur = cnx.cursor(dictionary=True)
            # cur.execute("SELECT * FROM GAME WHERE TITLE = %s", [title])
            cur.execute("SELECT TITLE, RELEASE_DATE, CON_NAME, PUB_NAME FROM GAME JOIN CONSOLE"\
                        " ON GAME.CON_CODE = CONSOLE.CON_ID JOIN PUBLISHER ON GAME.PUB_ID = PUBLISHER.PUB_ID" \
                            " WHERE TITLE = %s", (title,))
            games = cur.fetchall()
        finally:
            if cur:
                cur.close()
    return render_template('search.html', games=games)

if __name__ == '__main__':
    app.run(host='localhost')
