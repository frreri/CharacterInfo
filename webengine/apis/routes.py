from flask import Blueprint, request, jsonify, abort, render_template
from webengine.apis import wowdata as myAPI
from webengine.mysql import SQLfetcher

apis = Blueprint("apis", __name__)


@apis.route("/server/api/roster", methods=["GET"])
def get_roster():
    api_roster = SQLfetcher.SQLfetchAll("all")
    return jsonify(api_roster)


@apis.route("/server/api/character", methods=["POST"])
def get_wow_character():
    if (
        not "region" in request.json
        or not "realm" in request.json
        or not "character" in request.json
    ):
        abort(400)
    api_region = request.json["region"]
    api_realm = request.json["realm"]
    api_character = request.json["character"]

    if (
        not all(c.isalpha() for c in api_character)
        or not api_realm.lower() in SQLfetcher.SQLfetchRealmLower()
        or not api_region.lower() in ["us", "eu"]
    ):
        abort(400)

    try:
        api_profile = myAPI.get_character(api_region, api_realm, api_character)
        SQLfetcher.SQLinsert(api_profile, "API")
    except:
        api_profile = {"error": "Character not found"}
    return jsonify(api_profile), 200


@apis.route("/server/searches", methods=["GET"])
def get_searches():
    searchlist = SQLfetcher.SQLfetchSearch()
    return render_template("searchstat.html", data=searchlist)
