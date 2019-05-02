from wowapi import WowApi
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


def API_get_profile(region, realm, character):
    wowchar = api.get_character_profile(
        region,
        realm,
        character,
        fields="items,guild,titles,mounts,pets,statistics,quests",
    )
    wow_c = []
    pet_name = []
    pet_count = 0
    title_count = 0
    quest_count = 0
    for title in wowchar["titles"]:
        if "selected" in title:
            wow_c.append(title["name"] % (wowchar["name"]))
            title_count += 1
        else:
            pass
    if title_count < 1:
        wow_c.append(wowchar["name"])
    wow_c.append(classes[wowchar["class"] - 1])
    wow_c.append(races[wowchar["race"]])
    wow_c.append(genders[wowchar["gender"]])
    wow_c.append(wowchar["level"])
    wow_c.append(wowchar["items"]["averageItemLevelEquipped"])
    try:
        wow_c.append(wowchar["guild"]["name"])
    except:
        wow_c.append("Not in a guild")
    wow_c.append(wowchar["realm"])
    wow_c.append(wowchar["totalHonorableKills"])
    wow_c.append(wowchar["thumbnail"])
    wow_c.append(
        "https://render-eu.worldofwarcraft.com/character/"
        + wowchar["thumbnail"].replace("avatar", "main")
    )
    wow_c.append(wowchar["achievementPoints"])
    wow_c.append(wowchar["mounts"]["numCollected"])
    for pet in wowchar["pets"]["collected"]:
        if pet["name"] not in pet_name:
            pet_count += 1
            pet_name.append(pet["name"])
    wow_c.append(pet_count)
    wow_c.append(
        wowchar["statistics"]["subCategories"][0]["subCategories"][1]["statistics"][0][
            "quantity"
        ]
    )
    for _ in wowchar["quests"]:
        quest_count += 1
    wow_c.append(quest_count)
    wow_c.append(wowchar["name"])

    return wow_c
