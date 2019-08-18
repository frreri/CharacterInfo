from flask import Blueprint, render_template

misc = Blueprint("misc", __name__)


@misc.route("/operator", methods=["GET", "POST"])
def operator_search():
    return render_template("operator.html")
