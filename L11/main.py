import flask

application = flask.Flask(__name__, template_folder = "./views", static_folder = "./resources")


@application.route("/")
def index():
    return flask.render_template("index.html")


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


if __name__ == "__main__":
    application.run()
