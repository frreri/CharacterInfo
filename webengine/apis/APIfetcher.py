from wowapi import WowApi
from datetime import datetime
from config import APIconfig
api = WowApi(APIconfig.CLIENT_ID, APIconfig.CLIENT_SECRET)
races = {1 : "Human",2 : "Orc",3 : "Dwarf",4 : "Night Elf",5 : "Undead",6 : "Tauren",7 : "Gnome",8 : "Troll",9 : "Goblin",10 : "Blood Elf",11 : "Draenei",22 : "Worgen",
        24 : "Pandaren Neutral",25 : "Pandaren Alliance",26 : "Pandaren Horde",27 : "Nightborne",28 : "Highmountain Tauren",29 : "Void Elf",30 : "Lightforged Draenei",
        34 : "Dark Iron Dwarf",36 : "Mag'har Orc", 31 : "Zandalari Troll", 32 : "Kul Tiran"}
classes = ["Warrior","Paladin","Hunter","Rogue","Priest","Death Knight","Shaman","Mage","Warlock","Monk","Druid","Demon Hunter"]
genders = ["Male","Female"]

def APIfetchChar(realm,character):
    wowchar = api.get_character_profile('eu',realm, character, fields='items,guild,titles,mounts,pets,statistics,quests')
    def bonusadd(type,length):
        result=''
        count=0
        while count < length:
            result +=':'+str(wowchar['items'][type]['bonusLists'][count])
            count+=1
        return result[1:]
    wow_c = []
    pet_name = []
    pet_count = 0
    title_count = 0
    quest_count = 0
    for title in wowchar['titles']:
	    if 'selected' in title:
		    wow_c.append(title['name'] % (wowchar['name']))
		    title_count +=1
	    else:
		    pass
    if title_count < 1:
	    wow_c.append(wowchar['name'])
    wow_c.append(classes[wowchar['class']-1])
    wow_c.append(races[wowchar['race']])
    wow_c.append(genders[wowchar['gender']])
    wow_c.append(wowchar['level'])
    wow_c.append(wowchar['items']['averageItemLevelEquipped'])
    try:
        wow_c.append(wowchar['guild']['name'])
    except:
        wow_c.append('Not in a guild')
    wow_c.append(wowchar['realm'])
    wow_c.append(wowchar['totalHonorableKills'])
    wow_c.append(wowchar['thumbnail'])
    wow_c.append('https://render-eu.worldofwarcraft.com/character/'+wowchar['thumbnail'].replace('avatar','main'))
    wow_c.append(wowchar['achievementPoints'])
    wow_c.append(wowchar['mounts']['numCollected'])
    for pet in wowchar['pets']['collected']:
        if pet['name'] not in pet_name:
            pet_count+=1
            pet_name.append(pet['name'])
    wow_c.append(pet_count)
    #Below is factions at exalted
    wow_c.append(wowchar['statistics']['subCategories'][0]['subCategories'][1]['statistics'][0]['quantity'])
    for _ in wowchar['quests']:
	    quest_count +=1
    wow_c.append(quest_count)
    wow_c.append(wowchar['name'])
    # Below is gear
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['head']['id'])+'&bonus='+bonusadd('head',len(wowchar['items']['head']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['neck']['id'])+'&bonus='+bonusadd('neck',len(wowchar['items']['neck']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['shoulder']['id'])+'&bonus='+bonusadd('shoulder',len(wowchar['items']['shoulder']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['back']['id'])+'&bonus='+bonusadd('back',len(wowchar['items']['back']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['chest']['id'])+'&bonus='+bonusadd('chest',len(wowchar['items']['chest']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['wrist']['id'])+'&bonus='+bonusadd('wrist',len(wowchar['items']['wrist']['bonusLists'])))
    if 'offHand' in wowchar['items']:
        wow_c.append('<a href="'+'https://www.wowhead.com/item='+str(wowchar['items']['mainHand']['id'])+'&bonus='+bonusadd('mainHand',len(wowchar['items']['mainHand']['bonusLists']))+
            '" target='+'"_blank'+'"><span class='+'"hidden">Mainhand</span></a><br>')
        wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['offHand']['id'])+'&bonus='+bonusadd('offHand',len(wowchar['items']['offHand']['bonusLists'])))
    else:
        wow_c.append('<br><br><a href="'+'https://www.wowhead.com/item='+str(wowchar['items']['mainHand']['id'])+'&bonus='+bonusadd('mainHand',len(wowchar['items']['mainHand']['bonusLists']))+
            '" target='+'"_blank'+'"><span class='+'"hidden">Mainhand</span></a><br>')
        wow_c.append('Placeholder')
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['hands']['id'])+'&bonus='+bonusadd('hands',len(wowchar['items']['hands']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['waist']['id'])+'&bonus='+bonusadd('waist',len(wowchar['items']['waist']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['legs']['id'])+'&bonus='+bonusadd('legs',len(wowchar['items']['legs']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['feet']['id'])+'&bonus='+bonusadd('feet',len(wowchar['items']['feet']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['finger1']['id'])+'&bonus='+bonusadd('finger1',len(wowchar['items']['finger1']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['finger2']['id'])+'&bonus='+bonusadd('finger2',len(wowchar['items']['finger2']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['trinket1']['id'])+'&bonus='+bonusadd('trinket1',len(wowchar['items']['trinket1']['bonusLists'])))
    wow_c.append('https://www.wowhead.com/item='+str(wowchar['items']['trinket2']['id'])+'&bonus='+bonusadd('trinket2',len(wowchar['items']['trinket2']['bonusLists'])))

    return wow_c

def get_token_gold():
    regions = {'eu':'dynamic-eu','us':'dynamic-us','kr':'dynamic-kr'}
    tokeninfo_dict = {}
    for key, val in regions.items():
        tokeninfo = api.get_token(key, val)
        gold_amount = '{:,}'.format(int(tokeninfo['price']/10000))
        last_updated = datetime.fromtimestamp(tokeninfo['last_updated_timestamp']/1e3).strftime('%Y-%m-%d, %H:%M')
        tokeninfo_dict.update({key:{'gold':gold_amount, 'updated':last_updated}})
    return tokeninfo_dict