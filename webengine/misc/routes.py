from flask import Blueprint, render_template, request
from webengine.misc import msisdn

misc = Blueprint("misc", __name__)


@misc.route("/operator", methods=["GET", "POST"])
def operator_search():
    if request.method == "POST":
        if request.form["number"].isnumeric():
            the_operator = msisdn.op_search(request.form["number"])
            return render_template("operator.html", data=the_operator)
        else:
            return render_template("operator.html", data="Endast siffror tack!")

    return render_template("operator.html")


@misc.route("/tetris", methods=["GET"])
def tetris_game():
    return render_template("tetris_game.html", title="Tetris Game")
