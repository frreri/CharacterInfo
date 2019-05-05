from wowapi import WowApi
from datetime import datetime
from config import APIconfig

api = WowApi(APIconfig.CLIENT_ID, APIconfig.CLIENT_SECRET)
races = {
    1: "Human",
    2: "Orc",
    3: "Dwarf",
    4: "Night Elf",
    5: "Undead",
    6: "Tauren",
    7: "Gnome",
    8: "Troll",
    9: "Goblin",
    10: "Blood Elf",
    11: "Draenei",
    22: "Worgen",
    24: "Pandaren Neutral",
    25: "Pandaren Alliance",
    26: "Pandaren Horde",
    27: "Nightborne",
    28: "Highmountain Tauren",
    29: "Void Elf",
    30: "Lightforged Draenei",
    34: "Dark Iron Dwarf",
    36: "Mag'har Orc",
    31: "Zandalari Troll",
    32: "Kul Tiran",
}
classes = [
    "Warrior",
    "Paladin",
    "Hunter",
    "Rogue",
    "Priest",
    "Death Knight",
    "Shaman",
    "Mage",
    "Warlock",
    "Monk",
    "Druid",
    "Demon Hunter",
]
genders = ["Male", "Female"]
professions = [
    "Alchemy",
    "Herbalism",
    "Mining",
    "Blacksmithing",
    "Engineering",
    "Skinning",
    "Jewelcrafting",
    "Enchanting",
    "Leatherworking",
    "Inscription",
    "Tailoring",
]
item_list = [
    "head",
    "neck",
    "shoulder",
    "back",
    "chest",
    "wrist",
    "hands",
    "waist",
    "legs",
    "feet",
    "finger1",
    "finger2",
    "trinket1",
    "trinket2",
]


def get_character(region, realm, character, gear=None):

    include_gear = gear
    wowchar = api.get_character_profile(
        region,
        realm,
        character,
        fields="items,guild,titles,mounts,pets,statistics,quests,professions",
    )

    wow_c = {}
    pet_name = []
    learned_professions = []
    pet_count = 0
    title_count = 0
    quest_count = 0

    def bonusadd(type, length):
        result = ""
        count = 0
        while count < length:
            result += ":" + str(wowchar["items"][type]["bonusLists"][count])
            count += 1
        return result[1:]

    def additems():
        for item in wowchar["items"]:
            if item in item_list:
                wow_c.update(
                    {
                        item: "https://www.wowhead.com/item="
                        + str(wowchar["items"][item]["id"])
                        + "&bonus="
                        + bonusadd(item, len(wowchar["items"][item]["bonusLists"]))
                    }
                )
            if "offHand" in wowchar["items"]:
                wow_c.update(
                    {
                        "mainhand": '<a href="'
                        + "https://www.wowhead.com/item="
                        + str(wowchar["items"]["mainHand"]["id"])
                        + "&bonus="
                        + bonusadd(
                            "mainHand", len(wowchar["items"]["mainHand"]["bonusLists"])
                        )
                        + '" target='
                        + '"_blank'
                        + '"><span class='
                        + '"hidden">Mainhand</span></a><br>'
                    }
                )
                wow_c.update(
                    {
                        "offhand": "https://www.wowhead.com/item="
                        + str(wowchar["items"]["offHand"]["id"])
                        + "&bonus="
                        + bonusadd(
                            "offHand", len(wowchar["items"]["offHand"]["bonusLists"])
                        )
                    }
                )
            elif "mainHand" in wowchar["items"]:
                wow_c.update(
                    {
                        "mainhand": '<br><br><a href="'
                        + "https://www.wowhead.com/item="
                        + str(wowchar["items"]["mainHand"]["id"])
                        + "&bonus="
                        + bonusadd(
                            "mainHand", len(wowchar["items"]["mainHand"]["bonusLists"])
                        )
                        + '" target='
                        + '"_blank'
                        + '"><span class='
                        + '"hidden">Mainhand</span></a><br>'
                    }
                )
                wow_c.update({"offhand": "Placeholder"})
            else:
                wow_c.update({"mainhand": "Placeholder"})
                wow_c.update({"offhand": "Placeholder"})

    for title in wowchar["titles"]:
        if "selected" in title:
            wow_c.update({"name_with_title": title["name"] % (wowchar["name"])})
            title_count += 1
        else:
            pass
    if title_count < 1:
        wow_c.update({"name_with_title": wowchar["name"]})
    wow_c.update({"class": classes[wowchar["class"] - 1]})
    wow_c.update({"race": races[wowchar["race"]]})
    wow_c.update({"gender": genders[wowchar["gender"]]})
    wow_c.update({"level": wowchar["level"]})
    wow_c.update({"ilvl": wowchar["items"]["averageItemLevelEquipped"]})
    try:
        wow_c.update({"guild": wowchar["guild"]["name"]})
    except:
        wow_c.update({"guild": "Not in a guild"})
    wow_c.update({"realm": wowchar["realm"]})
    wow_c.update({"hks": wowchar["totalHonorableKills"]})
    wow_c.update({"thumb": wowchar["thumbnail"]})
    wow_c.update(
        {
            "image": "https://render-eu.worldofwarcraft.com/character/"
            + wowchar["thumbnail"].replace("avatar", "main")
        }
    )
    wow_c.update({"achievement": wowchar["achievementPoints"]})
    wow_c.update({"mounts": wowchar["mounts"]["numCollected"]})
    for pet in wowchar["pets"]["collected"]:
        if pet["name"] not in pet_name:
            pet_count += 1
            pet_name.append(pet["name"])
    wow_c.update({"pets": pet_count})
    wow_c.update(
        {
            "exalted": wowchar["statistics"]["subCategories"][0]["subCategories"][1][
                "statistics"
            ][0]["quantity"]
        }
    )
    for _ in wowchar["quests"]:
        quest_count += 1
    wow_c.update({"quests": quest_count})
    wow_c.update({"name": wowchar["name"]})
    for item in wowchar["professions"]["primary"]:
        if item["name"] in professions:
            learned_professions.append(item["name"])
    try:
        wow_c.update({"profession1": learned_professions[0]})
    except:
        wow_c.update({"profession1": "No profession"})
    try:
        wow_c.update({"profession2": learned_professions[1]})
    except:
        wow_c.update({"profession2": "No profession"})

    if include_gear == "gear":
        additems()

    return wow_c


def get_token_gold():
    regions = {"eu": "dynamic-eu", "us": "dynamic-us", "kr": "dynamic-kr"}
    tokeninfo_dict = {}
    for key, val in regions.items():
        tokeninfo = api.get_token(key, val)
        gold_amount = "{:,}".format(int(tokeninfo["price"] / 10000))
        last_updated = datetime.fromtimestamp(
            tokeninfo["last_updated_timestamp"] / 1e3
        ).strftime("%Y-%m-%d, %H:%M")
        tokeninfo_dict.update({key: {"gold": gold_amount, "updated": last_updated}})
    return tokeninfo_dict
