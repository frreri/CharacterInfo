from flask import Blueprint, request, jsonify, abort, render_template
from webengine.apis import charAPI as myAPI
from webengine.mysql import SQLfetcher

apis = Blueprint('apis', __name__)

@apis.route('/server/api/roster', methods=['GET'])
def get_roster():
    api_roster = SQLfetcher.SQLfetchAll()
    return jsonify(api_roster)

@apis.route('/server/api/character', methods=['POST'])
def get_character():
    if not 'region' in request.json or not 'realm' in request.json or not 'character' in request.json:
        abort(400)
    api_region = request.json['region']
    api_realm = request.json['realm']
    api_character = request.json['character']

    if not all(c.isalpha() for c in api_character) or not api_realm.lower() in SQLfetcher.SQLfetchRealmLower() or not api_region.lower() in ['us','eu']:
        abort(400)

    try:
        api_profile = myAPI.API_get_profile(api_region,api_realm,api_character)
        api_response = {
            'title': api_profile[0],
            'class': api_profile[1],
            'race': api_profile[2],
            'gender': api_profile[3],
            'level': api_profile[4],
            'ilvl': api_profile[5],
            'guild': api_profile[6],
            'realm': api_profile[7],
            'hk': api_profile[8],
            'thumb': 'https://render-eu.worldofwarcraft.com/character/'+api_profile[9],
            'image': api_profile[10],
            'achievement': api_profile[11],
            'mounts': api_profile[12],
            'pets': api_profile[13],
            'exalted': api_profile[14],
            'quests': api_profile[15],
            'name': api_profile[16]
        }
        SQLfetcher.SQLinsert(api_profile, "API")
    except:
        api_response = {
            'error':'Character not found'
        }
    return jsonify(api_response), 200

@apis.route('/server/searches', methods=['GET'])
def get_searches():
    searchlist = SQLfetcher.SQLfetchSearch()
    return render_template('searchstat.html', data=searchlist)
