# functions and their appropiate imports that do the heavy lifting for init. Thus Cogs
import random
import string
import psycopg2
from flask import redirect, url_for

def Generate_Code():
    return ''.join( random.choice( string.ascii_uppercase + string.digits ) for i in range(4) )


def Create_Lobby( hostname, roomcode ):
    with psycopg2.connect( database="webgame", user="austinoblack", password="(AUS.Data.1998)", host="localhost" ) as conn:
        with conn.cursor() as cur:
            # check for duplicate usernames
            cur.execute("SELECT * FROM player WHERE username = %s", (hostname, ) )
            if cur.fetchone() is not None:
                print("username taken")
                return redirect( url_for('Create_Page') )
            # check for duplicate roomcodes
            cur.execute("SELECT roomcode FROM lobby WHERE roomcode = %s", (roomcode, ) )
            if cur.fetchone() is not None:
                print("lobbycode already generated... uh oh. I promise this doesn't happen very often")
                return redirect( url_for('Create_Page') )
            # coast is clear, do the thing(s)
            else:
                cur.execute("INSERT INTO player (username) VALUES (%s)", (hostname, ) )
                cur.execute("INSERT INTO lobby (roomcode) VALUES (%s)", (roomcode, ) )
                cur.execute("INSERT INTO hosts (username, roomcode) VALUES (%s, %s)", (hostname, roomcode) )
                conn.commit()
    conn.close()


def Join_Lobby( username, roomcode ):
    with psycopg2.connect( database="webgame", user="austinoblack", password="(AUS.Data.1998)", host="localhost" ) as conn:
        with conn.cursor() as cur:
            # check for duplicate usernames
            cur.execute("SELECT * FROM player WHERE username = %s", (username, ) )
            if cur.fetchone() is not None:
                print("username taken")
                return redirect( url_for('Join_Page') )
            # check if the given roomcode exists            
            cur.execute("SELECT roomcode FROM lobby WHERE roomcode = %s", (roomcode, ) )
            if cur.fetchone() is None:
                print("lobby doesn't exist!")
                return redirect( url_for('Join_Page') )
            # coast is clear, do the thing(s)
            else:
                cur.execute("INSERT INTO player (username) VALUES (%s)", (username, ) )
                cur.execute("INSERT INTO joins (username, roomcode) VALUES (%s, %s)", (username, roomcode) )
                conn.commit()
    conn.close()
