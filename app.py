from flask import *
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__, static_url_path='/static')

# Configure db
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sql5665870"
)

#cur = cnx.cursor(dictionary=True)

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
            cur.execute("SELECT TITLE, RELEASE_DATE, CON_NAME, PUB_NAME FROM GAME JOIN CONSOLE"\
                        " ON GAME.CON_ID = CONSOLE.CON_ID JOIN PUBLISHER ON GAME.PUB_ID = PUBLISHER.PUB_ID" \
                            " WHERE TITLE LIKE %s", ('%' + title + '%',))
            games = cur.fetchall()
        finally:
            if cur:
                cur.close()
    return render_template('search.html', games=games)

@app.route('/add.html', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form["title"]
        publisher = request.form["publisher"]
        release_year = request.form["release_year"]
        console = request.form["console"]
        
        
        try:
            cur = cnx.cursor(dictionary=True)
            pub_id = get_pub_id(publisher)
            con_id = get_con_id(console)
            game_id = get_game_id() + 1
            cur.execute('INSERT INTO GAME VALUES (%s ,%s, %s, %s, %s)', (int(game_id), title, int(pub_id), int(release_year), int(con_id)))
            cnx.commit()
        except:
            cnx.rollback()
        finally:
            if cur: 
                cur.close()
                return redirect('/')
    return render_template('add.html')

# Get the console id from a value when inserting a game to the game table
def get_con_id(console):
    try:
        cur = cnx.cursor(dictionary=True)
        cur.execute('SELECT CON_ID FROM CONSOLE WHERE CON_NAME LIKE %s;', (console,))
        result = cur.fetchone()

        if result is not None:
            return result['CON_ID']  
        else:
            return None
    finally:
        if cur:
            cur.close()

def get_pub_id(publisher):
        try:
            cur = cnx.cursor(dictionary=True)
            cur.execute('SELECT PUB_ID FROM PUBLISHER WHERE PUB_NAME LIKE %s;', (publisher,))
            result = cur.fetchone()
            if result is not None:
                return result['PUB_ID']
            else: 
                return None
        finally: 
            if cur: 
                cur.close()

def get_game_id():
    try:
        cur = cnx.cursor(dictionary=True)
        cur.execute("SELECT MAX(GAME_ID) FROM GAME;")
        result = cur.fetchone()
        if result is not None:
            return result["MAX(GAME_ID)"]
        else: 
            return None
    finally:
        if cur:
            cur.close()


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
