# Main app
# @Austin Black
from flask import Flask, url_for, render_template, redirect, request, jsonify
from Cogs import Generate_Code, Create_Lobby, Join_Lobby, Get_Players
import json

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


@app.route("/", methods=['POST'])                                               #triggered by form on either create or join page
def Handle_Clicks():
    if request.method == 'POST':
        if request.form.get('return') == 'Leave':                               #if leave button is clicked
            return render_template("Landing.html")                              #go to Landing page

        elif request.form.get('insert') == 'Create':                            #if create button is clicked on create page
            rmcode = Generate_Code()                                            #see Cogs
            hname = request.form['hostname']                                    #get hostname from form
            rmsize = request.form['roomsize']                                   #get roomsize from form
            if Create_Lobby( hname, rmcode, rmsize ):                           #see Cogs
                return redirect( url_for('Lobby_Page', room_code=rmcode))       #go to correct lobby
            elif Create_Lobby( hname, rmcode, rmsize ) == "username":           #refresh page with username taken msg
                return redirect( url_for('Create_Page', flash_msg="username"))
            elif Create_Lobby( hname, rmcode, rmsize ) == "roomcode":           #refresh page with roomcode already generated msg
                return redirect( url_for('Create_Page', flash_msg="roomcode"))
            else:
                return redirect( url_for('Create_Page', flash_msg="error"))     #refresh page with backup\undefined msg

        elif request.form.get('insert') == 'Join':                              #if join button is clicked on join page
            rmcode = request.form['roomcode']                                   #get roomcode from form
            uname = request.form['username']                                    #get username from form
            if Join_Lobby( uname, rmcode ):                                     #see Cogs
                return redirect( url_for('Lobby_Page', room_code=rmcode))       #go to correct lobby
            elif Join_Lobby( uname, rmcode ) == "username":                     #refresh page with username taken msg
                return redirect( url_for('Join_Page', flash_msg="username"))
            elif Join_Lobby( uname, rmcode ) == "room":                         #refresh page with room does not exist msg
                return redirect( url_for('Join_Page', flash_msg="roomcode")
            elif Join_Lobby( uname, rmcode ) == "full":                         #refresh page with room is full msg
                return redirect( url_for('Join_Page', flash_msg="full"))
            else:
                return redirect( url_for('Join_Page', flash_msg="error"))       #refresh page with backup\undefined msg
    else:
        return render_template("Landing.html")                                  #if something goes horribly wrong, go back to Landing


@app.route("/Lobby/<room_code>")
def Lobby_Page(room_code):
    return render_template("Lobby.html", code=room_code)


@app.route("/update_list/<room_code>", methods=['GET','POST'])
def update_list(room_code):
    rmcode = room_code
    plist = Get_Players( rmcode )
    return jsonify( plist )


if __name__ == "__main__":
    app.run( host='0.0.0.0', port=5000, debug=True )
