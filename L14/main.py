import flask
import flask_session as session
import flask_socketio as io
from globals import *
from client import Client
from game import GameRoom


application = flask.Flask(__name__, template_folder = "./views", static_folder = "./resources")
application.config["SECRET_KEY"] = "MM"
application.config["SESSION_TYPE"] = "filesystem"
application.config["SESSION_FILE_DIR"] = "./sessions"
session.Session(application)
socketIO = io.SocketIO(application, manage_session = False)

#users = list()
#users.append(User("MM", "MM@mm.mm", "mmmm"))
#users.append(User("BP", "BP@bp.bp", "bp"))

#waiting_rooms = list()
#during_game_rooms = list()


@application.route("/")
def index():
	return flask.redirect("/pictures")



@application.route("/pictures")
def pictures():
	return flask.render_template("pictures.html")



@application.route("/snake")
def snake():
	return flask.render_template("snake.html")



@application.route("/album")
def album():
	return flask.render_template("album.html")



@application.route("/game")
def game():
	return flask.render_template("game.html")



@application.route("/register", methods = ["GET", "POST"])
def register():
	if flask.request.method == "GET":
		if "_profile" in flask.session:
			return flask.redirect("/profile")
		else:
			return flask.render_template("register.html")

	elif flask.request.method == "POST":
		username = flask.request.form["Username"]
		email = flask.request.form["Email"]
		password = flask.request.form["Password"]
		is_valid = True

		print(username)
		print(email)
		print(password)

		for client in clients.values():
			print(client.username)
			print(username)
			print(client.email)
			print(email)
			if client.username == username or client.email == email:
				return flask.redirect("/register")

		# todo: validation
		# todo: usernames and emails have to be unique

		if is_valid:
			client = Client()
			client.create(username, email, password)
			flask.session["_profile"] = True
			flask.session["_client"] = client.client

			return flask.redirect("/profile")

		return flask.redirect("/register")



@application.route("/login", methods = ["GET", "POST"])
def login():
	if flask.request.method == "GET":
		if "_profile" in flask.session:
			return flask.redirect("/profile")
		else:
			return flask.render_template("login.html")

	elif flask.request.method == "POST":
		username = flask.request.form["UsernameEmail"]
		email = flask.request.form["UsernameEmail"]
		password = flask.request.form["Password"]

		print(username)
		print(email)
		print(password)

		for client in clients.values():
			if client.username == username or client.email == email:
				if client.password == password:
					flask.session["_profile"] = True
					flask.session["_client"] = client.client

					return flask.redirect("/profile")

		return flask.redirect("/login")



@application.route("/profile")
def profile():
	if "_profile" in flask.session:
		client = clients[flask.session["_client"]]
		return flask.render_template("profile.html", username = client.username, email = client.email, wins = client.wins, draws = client.draws, losses = client.losses)
	else:
		return flask.redirect("/login")



@application.route("/room")
def room():
	if "_profile" in flask.session:
		client = clients[flask.session["_client"]]

		if client.game is None:
			return flask.render_template("game-room.html")
		else:
			return flask.redirect("/profile")
	else:
		return flask.redirect("/login")



@application.route("/logout")
def logout():
	connection = flask.session["_client"]
	room = clients[connection].game

	if room is not None:
		if room in waiting_rooms:
			waiting_rooms[room].leave(connection)
		elif room in during_game_rooms:
			during_game_rooms[room].leave(connection)

		print(F"Disconnection: {connection}")
		print(F"Room: {room}")

	flask.session.clear()
	return flask.redirect("/login")



@application.route("/debug")
def debug():
	print(flask.session)
	return flask.render_template("debug.html", clients = clients.values(), waiting_rooms = waiting_rooms.values(), during_game_rooms = during_game_rooms.values())



# todo: room page
# todo: find request

# {% if condition %}
# html
# {% else %}
# html
# {% endif %}

# {% for x in xxx %}
# html
# {% endfor %}

# {{ variable }}

# {% extends "page.html" %}
# html
# {% endblock %}

@socketIO.on(CONNECTION, namespace = "/game-room")
def connectionRoom(data):
	if "_profile" not in flask.session:
		return

	for game_room in waiting_rooms.values():
		game_room.join(flask.session["_client"])
		io.join_room(game_room.game)
		break
	else:
		game_room = GameRoom(flask.session["_client"])
		io.join_room(game_room.game)

	connection = flask.session["_client"]
	room = clients[connection].game
	print(F"Connection: {connection}")
	print(F"Room: {room}")



@socketIO.on(DISCONNECTION, namespace = "/game-room")
def disconnectionRoom():
	if "_profile" not in flask.session:
		return

	connection = flask.session["_client"]
	room = clients[connection].game

	if room in waiting_rooms:
		waiting_rooms[room].leave(connection)
		io.leave_room(room)
	elif room in during_game_rooms:
		during_game_rooms[room].leave(connection)
		io.leave_room(room)

	print(F"Disconnection: {connection}")
	print(F"Room: {room}")



if __name__ == "__main__":
	connection = sqlite3.connect("main.db")
	cursor = connection.cursor()
	cursor.execute(open("./queries/select-clients.sql").read())
	for value in cursor.fetchall():
		client = Client()
		client.restore(value[0])
		print(client)
	connection.commit()
	connection.close()

	application.debug = True
	socketIO.run(application)
	# application.run(debug = True)
