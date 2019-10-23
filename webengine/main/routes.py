from flask import Blueprint, render_template
from webengine.mysql import SQLfetcher
from webengine.apis import wowdata

main = Blueprint("main", __name__)


css_wow_class = {
    "Death Knight": "death-knight",
    "Demon Hunter": "demon-hunter",
    "Druid": "druid",
    "Hunter": "hunter",
    "Mage": "mage",
    "Monk": "monk",
    "Paladin": "paladin",
    "Priest": "priest",
    "Rogue": "rogue",
    "Shaman": "shaman",
    "Warlock": "warlock",
    "Warrior": "warrior",
}
thumb = "https://render-eu.worldofwarcraft.com/character/"
no_thumb = "/static/images/frericon.png"


@main.route("/", methods=["GET"])
@main.route("/lookup", methods=["GET"])
def char_lookup():
    realmlist = SQLfetcher.SQLfetchRealm()
    return render_template("lookup.html", realm_data=realmlist)


@main.route("/lookup/<wowrealm>/<wowcharacter>", methods=["GET"])
def char_search(wowrealm, wowcharacter):
    realmlist = SQLfetcher.SQLfetchRealm()
    realmlist_l = SQLfetcher.SQLfetchRealmLower()
    if (
        all(c.isalpha() for c in wowcharacter)
        and len(wowcharacter) < 13
        and len(wowcharacter) > 1
        and wowrealm in realmlist_l
    ):
        try:
            char_profile = wowdata.get_character("eu", wowrealm, wowcharacter, "gear")
            SQLfetcher.SQLinsert(char_profile, "WEB")
            return render_template(
                "lookup.html",
                char_data=char_profile,
                realm_data=realmlist,
                color_class=css_wow_class,
            )
        except:
            return render_template(
                "lookup.html", realm_data=realmlist, err_msg="Character not found!"
            )
    else:
        return render_template(
            "lookup.html", realm_data=realmlist, err_msg="Invalid input!"
        )


@main.route("/toplist", methods=["GET"])
def output():
    thumbnail = []
    g_char = SQLfetcher.SQLfetch()
    count = 0
    for x in g_char:
        if x[3] == "none":
            thumbnail.append(no_thumb)
        else:
            thumbnail.append(thumb + x[3])
        count += 1
    return render_template(
        "toplist.html", rank_list=g_char, thumb=thumbnail, title="Toplist"
    )


@main.route("/roster", methods=["GET"])
def roster_list():
    g_roster = SQLfetcher.SQLfetchAll()
    return render_template(
        "roster.html", data=g_roster, color_class=css_wow_class, title="Roster"
    )


@main.route("/token", methods=["GET"])
def get_token_info():
    token_info = SQLfetcher.SQLtokenFetchCurrent()
    token_history = SQLfetcher.SQLtokenFetchHistory()
    return render_template(
        "gold_token.html", data=token_info, data1=token_history, title="Token"
    )
