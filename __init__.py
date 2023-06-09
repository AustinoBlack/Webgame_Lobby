# Main app
# @Austin Black
from flask import Flask, url_for, render_template, redirect, request, jsonify
from Cogs import Generate_Code, Create_Lobby, Join_Lobby, Get_Players, Leave_Lobby, End_Game
import json

app = Flask(__name__)

@app.route("/")
def Landing_Page():
    '''renders the Landing.html template'''
    return render_template("Landing.html")


@app.route("/create_lobby")
def Create_Page():
    '''renders the Create.hmtl template'''
    return render_template("Create.html")


@app.route("/join_lobby")
def Join_Page():
    '''renders the Join.html template'''
    return render_template("Join.html")


@app.route("/", methods=['POST'])                                               #triggered by form on either create or join page
def Handle_Clicks():
    '''handles various button clicks throughout the website
       Leave -> returns the user to the landing page
       End Game -> calls End_Game() and returns the user to the landing page
       Leave Game -> calls Leave_Game() and returns the user to the landing page
       Create -> calls Generate_Code and Create_Lobby(), on success, redirects user to a newly created Lobby
       Join -> redirects user to the appropiate Lobby on success'''
    if request.method == 'POST':
        if request.form.get('return') == 'Leave':                               #if leave button is clicked
            return render_template("Landing.html")                              #go to Landing page

        elif request.form.get('end') == 'End Game':
            rmcode = request.form['roomcode']
            if End_Game(rmcode) == True:
                return redirect( url_for('Landing_Page') )

        elif request.form.get('leave') == 'Leave Game':
            playername = request.form['playername']
            if Leave_Lobby(playername) == True:
                return redirect( url_for('Landing_Page') )

        elif request.form.get('insert') == 'Create':                                        #if create button is clicked on create page
            rmcode = Generate_Code()                                                        #see Cogs
            hname = request.form['hostname']                                                #get hostname from form
            rmsize = request.form['roomsize']                                               #get roomsize from form
            if Create_Lobby( hname, rmcode, rmsize ) == True:                               #see Cogs
                return redirect( url_for('Lobby_Page', room_code=rmcode, playername=hname)) #go to correct lobby
            elif Create_Lobby( hname, rmcode, rmsize ) == "username":                       #refresh page with username taken msg
                return render_template('Create.html', flash_msg="username")
            elif Create_Lobby( hname, rmcode, rmsize ) == "roomcode":                       #refresh page with roomcode already generated msg
                return render_template('Create.html', flash_msg="roomcode")
            else:
                return render_template('Create.html', flash_msg="error")                    #refresh page with backup\undefined msg

        elif request.form.get('insert') == 'Join':                                          #if join button is clicked on join page
            rmcode = request.form['roomcode']                                               #get roomcode from form
            uname = request.form['username']                                                #get username from form
            if Join_Lobby( uname, rmcode ) == True:                                         #see Cogs
                return redirect( url_for('Lobby_Page', room_code=rmcode, playername=uname ))#go to correct lobby
            elif Join_Lobby( uname, rmcode ) == "username":                                 #refresh page with username taken msg
                return render_template('Join.html', flash_msg="username") 
            elif Join_Lobby( uname, rmcode ) == "room":                                     #refresh page with room does not exist msg
                return render_template('Join.html', flash_msg="room") 
            elif Join_Lobby( uname, rmcode ) == "full":                                     #refresh page with room is full msg
                return render_template('Join.html', flash_msg="full") 
            else:
                return render_template('Join.html', flash_msg="error")                      #refresh page with backup\undefined msg
    else:
        return render_template("Landing.html")                                              #if something goes horribly wrong, go back to Landing


@app.route("/Lobby/<room_code>/<playername>")
def Lobby_Page(room_code, playername):
    '''renders the Lobby.html template'''
    return render_template("Lobby.html", code=room_code, name=playername)


@app.route("/update_list/<room_code>", methods=['GET','POST'])
def update_list(room_code):
    '''checks and updates a list of players for a given roomcode'''
    rmcode = room_code
    plist = Get_Players( rmcode )
    return jsonify( plist )


if __name__ == "__main__":
    app.run( host='0.0.0.0', port=5000, debug=True )
