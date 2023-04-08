# Main app
# @Austin Black

from flask import Flask, url_for, render_template, redirect, request
import random
import string
import psycopg2

app = Flask(__name__)

@app.route("/")
def Landing_Page():
    return render_template("Landing.html")

@app.route("/create_lobby")
def Create_Page():
    return render_template("Create.html")

@app.route("/join_lobby")
def Join_Page():
    return render_template("Join.html")

@app.route("/Lobby/<room_code>")
def Lobby_Page(room_code):
    return render_template("Lobby.html", code=room_code)

def Generate_Code():
    return ''.join( random.choice( string.ascii_uppercase + string.digits ) for i in range(4) )

@app.route("/", methods=['POST']) #triggered by form on create page
def Create_Lobby():
    if request.method == 'POST':
        if request.form.get('return') == 'Leave':
            return render_template("Landing.html")
        elif request.form.get('insert') == 'Create': #database stuff
            rmcode = Generate_Code()
            return redirect( url_for('Lobby_Page', room_code=rmcode))
    else:
        return "error"

@app.route("/") #triggered by from on join page
def Join_Lobby():
    ... #insert data into database, redirect to lobby with url

if __name__ == "__main__":
    app.run( host='0.0.0.0', port=5000, debug=True )
