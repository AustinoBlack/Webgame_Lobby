# functions and their appropiate imports that do the heavy lifting for init. Thus Cogs
import random
import string
import psycopg2
from flask import redirect, url_for

def Generate_Code():
    return ''.join( random.choice( string.ascii_uppercase + string.digits ) for i in range(4) )


def Create_Lobby( hostname, roomcode, roomsize ):
    with psycopg2.connect( database="webgame", user="austinoblack", password="(AUS.Data.1998)", host="localhost" ) as conn:
        with conn.cursor() as cur:
            # check for duplicate usernames
            cur.execute("SELECT * FROM player WHERE username = %s", (hostname, ) )
            if cur.fetchone() is not None:
                print("username taken")
                return "username"
            # check for duplicate roomcodes
            cur.execute("SELECT roomcode FROM lobby WHERE roomcode = %s", (roomcode, ) )
            if cur.fetchone() is not None:
                print("lobbycode already generated... uh oh. I promise this doesn't happen very often")
                return "roomcode"
            # coast is clear, do the thing(s)
            else:
                cur.execute("INSERT INTO player (username) VALUES (%s)", (hostname, ) )
                cur.execute("INSERT INTO lobby (roomcode, roomsize) VALUES (%s, %s)", (roomcode, roomsize) )
                cur.execute("INSERT INTO hosts (username, roomcode) VALUES (%s, %s)", (hostname, roomcode) )
                conn.commit()
                return True
    conn.close()
    return False


def Join_Lobby( username, roomcode ):
    with psycopg2.connect( database="webgame", user="austinoblack", password="(AUS.Data.1998)", host="localhost" ) as conn:
        with conn.cursor() as cur:
            # check for duplicate usernames
            cur.execute("SELECT * FROM player WHERE username = %s", (username, ) )
            if cur.fetchone() is not None:
                print("username taken")
                return "username"
            # check if the given roomcode exists            
            cur.execute("SELECT roomcode FROM lobby WHERE roomcode = %s", (roomcode, ) )
            if cur.fetchone() is None:
                print("lobby doesn't exist!")
                return "room"
            # check if the lobby is full
            cur.execute("SELECT roomsize FROM lobby WHERE roomcode = %s", (roomcode, ) )
            size = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM ( SELECT username FROM hosts WHERE roomcode = %s UNION SELECT username FROM joins WHERE roomcode = %s ) as count", (roomcode, roomcode ) )
            occupency = cur.fetchone()[0]
            if occupency >= size: #check if lobby is full
                print("Lobby " + roomcode + " is full")
                return "full"
            # coast is clear, do the thing(s)
            else:
                cur.execute("INSERT INTO player (username) VALUES (%s)", (username, ) )
                cur.execute("INSERT INTO joins (username, roomcode) VALUES (%s, %s)", (username, roomcode) )
                conn.commit()
                return True
    conn.close()
    return False


def Get_Players( roomcode ):
    with psycopg2.connect( database="webgame", user="austinoblack", password="(AUS.Data.1998)", host="localhost" ) as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT username FROM hosts WHERE roomcode = %s 
                           UNION 
                           SELECT username FROM joins WHERE roomcode = %s''', (roomcode, roomcode) )
            List = [r[0] for r in cur.fetchall()]
    conn.close()
    return List


def Leave_Lobby(username):
	with psycopg2.connect( database="webgame", user="austinoblack", password="(AUS.Data.1998)", host="localhost" ) as conn:
		with conn.cursor() as cur:
            print( "Player: " + username + " left" )
			cur.execute("DELETE FROM player WHERE username = %s", (username,)	)
			cur.execute("DELETE FROM joins WHERE username = %s", (username,)	)
			conn.commit()
	conn.close()
	return True


def End_Game(roomcode):
	with psycopg2.connect( database="webgame", user="austinoblack", password="(AUS.Data.1998)", host="localhost" ) as conn:
		with conn.cursor() as cur:
            print( "deleting Lobby: " + roomcode )
			cur.execute("DELETE FROM player USING joins WHERE joins.username = player.username AND joins.roomcode = %s", (roomcode,)	)
			cur.execute("DELETE FROM player USING hosts WHERE hosts.username = player.username AND hosts.roomcode = %s", (roomcode,)	)
			cur.execute("DELETE FROM lobby WHERE roomcode = %s", (roomcode,)	)
			conn.commit()
	conn.close()
	return True

