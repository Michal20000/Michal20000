import flask
import flask_session as session
import flask_socketio as io
import threading


class User:
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password
		self.wins = 0
		self.draws = 0
		self.losses = 0


class GameRoom:
	def __init__(self):
		self.session_left = None
		self.session_right = None
		self.roomID = None
		self.thread = None

	def can_join(self):
		return self.session_right is None or self.session_left is None

	def join(self, session_user):
		if self.session_left is None:
			self.session_left = session_user["Username"]
			self.roomID = session_user["Username"]
		else:
			self.session_right = session_user["Username"]

	def run(self):
		self.thread = threading.Thread(target = self.game)
		self.thread.start()

	def game(self):
		print("thread runs!")
		during_game_rooms.remove(self)
		# todo: here is game
		# todo: initialization
		# todo: loop
		# todo: end game
		# todo: remove from during-game-rooms
		# todo: session-room
		# todo: it will check if session is leaving
		# todo: session direction will give you direction of move
		# todo: you need to emit game data to room
		# todo: objects
		# todo: client needs to read that

	def __repr__(self):
		return F"<GameRoom Left: {self.session_left}, Right: {self.session_right} RoomID: {self.roomID}>"


def insert(session_user):
	session_user["Wins"] = 0
	session_user["Draws"] = 0
	session_user["Losses"] = 0
	session_user["Room"] = None
	# todo: database insert


def update(session_user, wins = 0, draws = 0, losses = 0):
	session_user["Wins"] += wins
	session_user["Draws"] += draws
	session_user["Losses"] += losses
	# todo: database update


CONNECTION = "connect"
DISCONNECTION = "disconnect"

application = flask.Flask(__name__, template_folder = "./views", static_folder = "./resources")
application.config["SECRET_KEY"] = "MM"
application.config["SESSION_TYPE"] = "filesystem"
application.config["SESSION_FILE_DIR"] = "./sessions"
session.Session(application)
socketIO = io.SocketIO(application, manage_session = False)

users = list()
users.append(User("MM", "MM@mm.mm", "mmmm"))
users.append(User("BP", "BP@bp.bp", "bp"))

waiting_rooms = list()
during_game_rooms = list()


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
		if "Profile" in flask.session:
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

		# todo: database
		for user in users:
			if user.username == username or user.email == email:
				return flask.redirect("/register")

		# todo: validation

		if is_valid:
			# todo: database
			user = User(username, email, password)
			users.append(user)

			flask.session["Profile"] = True
			flask.session["Username"] = user.username
			flask.session["Email"] = user.email
			flask.session["Password"] = user.password
			flask.session["Wins"] = user.wins
			flask.session["Draws"] = user.draws
			flask.session["Losses"] = user.losses

			return flask.redirect("/profile")

		return flask.redirect("/register")


@application.route("/login", methods = ["GET", "POST"])
def login():
	if flask.request.method == "GET":
		if "Profile" in flask.session:
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

		for user in users:
			if user.username == username:
				if user.password == password:
					flask.session["Profile"] = True
					flask.session["Username"] = user.username
					flask.session["Email"] = user.email
					flask.session["Password"] = user.password
					flask.session["Wins"] = user.wins
					flask.session["Draws"] = user.draws
					flask.session["Losses"] = user.losses

					return flask.redirect("/profile")
		else:
			for user in users:
				if user.email == email:
					if user.password == password:
						flask.session["Profile"] = True
						flask.session["Username"] = user.username
						flask.session["Email"] = user.email
						flask.session["Password"] = user.password
						flask.session["Wins"] = user.wins
						flask.session["Draws"] = user.draws
						flask.session["Losses"] = user.losses

						return flask.redirect("/profile")

		return flask.redirect("/login")


@application.route("/profile")
def profile():
	if "Profile" in flask.session:
		return flask.render_template("profile.html")
	else:
		return flask.redirect("/login")


@application.route("/room")
def room():
	if "Profile" in flask.session:
		return flask.render_template("room.html")
	else:
		return flask.redirect("/login")


@application.route("/logout")
def logout():
	flask.session.clear()
	return flask.redirect("/login")


@application.route("/debug")
def debug():
	print(flask.session)
	return flask.render_template("debug.html", waiting_rooms = waiting_rooms, during_game_rooms = during_game_rooms)


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

@socketIO.on(CONNECTION, namespace = "/room")
def connectionRoom():
	for game_room in waiting_rooms:
		if game_room.can_join():
			game_room.join(flask.session)
			io.join_room(game_room.roomID)
			flask.session["RoomID"] = game_room.roomID
			waiting_rooms.remove(game_room)
			during_game_rooms.append(game_room)
			game_room.run()
			break
	else:
		game_room = GameRoom()
		game_room.join(flask.session)
		io.join_room(game_room.roomID)
		flask.session["RoomID"] = game_room.roomID
		waiting_rooms.append(game_room)

	connection_user = flask.session["Username"]
	room_user = flask.session["RoomID"]
	print(F"Connection: {connection_user}")
	print(F"Room: {room_user}")


@socketIO.on(DISCONNECTION, namespace = "/room")
def disconnectionRoom():
	connection_user = flask.session["Username"]
	room_user = flask.session["RoomID"]

	for game_room in waiting_rooms:
		if game_room.session_left == flask.session["Username"]:
			io.leave_room(flask.session["RoomID"])
			flask.session.pop("RoomID", None)
			waiting_rooms.remove(game_room)
			break
	# todo: if in during-game room sb leaves other player wins
	# todo: what if host creates room
	# todo: leave room
	# todo: create with the same name

	print(F"Disconnection: {connection_user}")
	print(F"Room: {room_user}")


if __name__ == "__main__":
	application.debug = True
	socketIO.run(application)
	# application.run(debug = True)
