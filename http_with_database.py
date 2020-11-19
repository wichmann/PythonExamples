
"""
Einfache Veranstaltungsverwaltung mit eigenem Web-Server und SQLite-Datenbank.
"""

import sqlite3
import webbrowser
from datetime import datetime

from flask import Flask
from flask import request


DB_FILENAME = 'datenbank.db'


# initialisiere HTTP-Server
app = Flask(__name__)

# initialisiere Datenbank im selben Thread wie HTTP-Server
conn = sqlite3.connect(DB_FILENAME, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS veranstaltungen (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, place TEXT, date DATE)""")
cursor.execute("""INSERT INTO veranstaltungen VALUES (NULL, 'Konzert', 'Bühne 1', '2018-01-05')""")
cursor.execute("""INSERT INTO veranstaltungen VALUES (NULL, 'Weinprobe', 'Wein Müller GmbH', '2018-08-12')""")
cursor.execute("""INSERT INTO veranstaltungen VALUES (NULL, 'Infoveranstaltung', 'Stadthaus', '2018-07-22')""")
conn.commit()

# erzeuge Vorlage für alle Seiten
html_template = """<html>
                     <head><title>{title}</title></head>
                     <style>
                       div a {{
                           background-color: #4CAF50;
                           border: 2px solid #aaaaaa;
                           color: white;
                           padding: 10px 32px;
                           text-align: center;
                           text-decoration: none;
                           display: inline-block;
                           font-size: 14px;
                       }}
                       div {{
                           background-color: #aaaaaa;
                           padding: 5px 5px;
                       }}
                     </style>
                     <body>
                       <div> Menü <a href="list">list</a><a href="add">add</a><a href="clear">clear</a></div>
                       <h1>{heading}</h1>
                       {content}
                     </body>
                   </html>"""


@app.route('/')
def info():
    text = 'VerAnDB - Veranstaltungsdatenbank!'
    content = '<p>Mögliche Funktionen:</p><ul><li>/list</li><li>/add</li></ul>'
    return html_template.format(title=text, heading=text, content=content)


@app.route('/list')
def list():
    title = 'Liste aller Veranstaltungen'
    heading = 'Liste aller Veranstaltungen'
    content = ''
    event_template = '<p>{name} am Ort {place} am {date}</p>'
    # hole alle Veranstaltungen aus der Datenbank
    cursor = conn.cursor()
    cursor.execute('SELECT name, place, date FROM veranstaltungen')
    for row in cursor.fetchall():
        # erzeuge HTML-Elemente für jede Veranstaltung aus der Datenbank
        name, place, date = row
        content += event_template.format(name=name, place=place, date=date)
    return html_template.format(title=title, heading=heading, content=content)


@app.route('/add', methods=['GET', 'POST'])
def add():
    title = 'Veranstaltung hinzufügen'
    heading = 'Veranstaltung hinzufügen'
    content = """<form action="/add" method="POST">
                   <p>Name: <input type="text" name="name" /></p>
                   <p>Ort: <input type="text" name="place" /></p>
                   <p>Datum (z.B. 2018-02-24): <input type="date" name="date" /></p>
                   <input type="submit" value="Absenden" />
                 </form>"""
    if request.method == 'POST':
        # hole Parameter aus POST-Request und schreibe Veranstaltung in Datenbank
        name = request.form.get('name')
        place = request.form.get('place')
        try:
            date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        except ValueError:
            date = datetime.now()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO veranstaltungen VALUES (NULL, ?, ?, ?)',
                       (name, place, date.date().isoformat()))
        conn.commit()
    return html_template.format(title=title, heading=heading, content=content)


@app.route('/clear')
def clear():
    title = 'Datenbank gelöscht'
    heading = 'Datenbank gelöscht'
    content = 'Alle Veranstaltungen wurden aus der Datenbank gelöscht.'
    cursor = conn.cursor()
    cursor.execute('DELETE FROM veranstaltungen')
    conn.commit()
    return html_template.format(title=title, heading=heading, content=content)


if __name__ == '__main__':
    webbrowser.open_new_tab('http://localhost:5000')
    app.run(host= '0.0.0.0', debug=True)
