def api_to_db():
    try:
        import mysql.connector
        from wowapi import WowApi
        from config import APIconfig, MySQLconfig

        api = WowApi(APIconfig.CLIENT_ID, APIconfig.CLIENT_SECRET)
        cnx = mysql.connector.connect(
            host=MySQLconfig.MYSQL_HOST,
            user=MySQLconfig.MYSQL_USER,
            passwd=MySQLconfig.MYSQL_PASSWORD,
            database=MySQLconfig.MYSQL_DATABASE,
        )
        cursor = cnx.cursor()
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
        gmembers = api.get_guild_profile(
            "eu", "aggramar", "fury", locale="en_GB", fields="members"
        )
        cursor.execute("select name from wowcharacter;")
        results = cursor.fetchall()
        index_count = 0
        intruder_count = 0
        c_sql = []
        c_api = []
        for x in gmembers["members"]:
            character_check = gmembers["members"][index_count]["character"]["name"]
            c_api.append(character_check)
            index_count += 1
        for x in results:
            c_sql.append(x[0])
        for x in c_sql:
            if x not in c_api:
                print(
                    "\nMostly reliable sources told me",
                    x,
                    "overstayed his/her welcome in our table!",
                )
                sql = "delete from wowcharacter where name = %s;"
                val = (x,)
                cursor.execute(sql, val)
                cnx.commit()
                print(cursor.rowcount, "records deleted.")
                intruder_count += 1
        if intruder_count < 1:
            print(
                "\nCharacter names in our database are all on the guest list, no need to throw anyone out!"
            )
        index_count = 0
        for x in gmembers["members"]:
            wow_character = gmembers["members"][index_count]["character"]["name"]
            wow_realm = gmembers["members"][index_count]["character"]["realm"]
            try:
                wowcharacter = api.get_character_profile(
                    "eu", wow_realm, wow_character, fields="items,guild"
                )
                race_name = races[wowcharacter["race"]]
                class_name = classes[wowcharacter["class"] - 1]
                gender_name = genders[wowcharacter["gender"]]
                print(
                    "\nInserting:",
                    wowcharacter["name"],
                    class_name,
                    race_name,
                    gender_name,
                    wowcharacter["level"],
                    wowcharacter["items"]["averageItemLevelEquipped"],
                    wowcharacter["guild"]["name"],
                    wow_realm,
                    wowcharacter["totalHonorableKills"],
                    "into database.",
                )
                sql = """INSERT INTO wowcharacter (name, class, race, gender, lvl, avgeqilvl, guild, realm, hk, thumbnail)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s) ON DUPLICATE KEY UPDATE name = VALUES(name), class = VALUES(class), race = VALUES(race), gender = VALUES(gender),
                lvl = VALUES(lvl), avgeqilvl = VALUES(avgeqilvl), guild = VALUES(guild), realm = VALUES(realm), hk = VALUES(hk), thumbnail = VALUES(thumbnail);"""
                val = (
                    wowcharacter["name"],
                    class_name,
                    race_name,
                    gender_name,
                    wowcharacter["level"],
                    wowcharacter["items"]["averageItemLevelEquipped"],
                    wowcharacter["guild"]["name"],
                    wow_realm,
                    wowcharacter["totalHonorableKills"],
                    wowcharacter["thumbnail"],
                )
                cursor.execute(sql, val)
                cnx.commit()
                print(cursor.rowcount, "records inserted/updated.")
            except:
                print(
                    "\nCharacter",
                    wow_character,
                    "not found on",
                    wow_realm,
                    "in armory or not actually in guild!",
                )
            finally:
                index_count += 1
        print("\nDatabase updates complete!\n")
        cnx.close()
    except:
        print(
            "Something went wrong during update from API to database, API or database could be down..."
        )


def token_to_db():
    from datetime import datetime, date
    import mysql.connector
    from wowapi import WowApi
    from config import APIconfig, MySQLconfig

    sql_config = {
        "user": MySQLconfig.MYSQL_USER,
        "password": MySQLconfig.MYSQL_PASSWORD,
        "host": MySQLconfig.MYSQL_HOST,
        "database": MySQLconfig.MYSQL_DATABASE,
    }
    this_day = str(date.today())
    api = WowApi(APIconfig.CLIENT_ID, APIconfig.CLIENT_SECRET)
    regions = {"eu": "dynamic-eu", "us": "dynamic-us", "kr": "dynamic-kr"}
    tokeninfo_dict = {}
    for key, val in regions.items():
        tokeninfo = api.get_token_index(key, val)
        gold_amount = "{:,}".format(int(tokeninfo["price"] / 10000))
        gold_int = int(tokeninfo["price"] / 10000)
        last_updated = datetime.fromtimestamp(
            tokeninfo["last_updated_timestamp"] / 1e3
        ).strftime("%Y-%m-%d, %H:%M")
        tokeninfo_dict.update(
            {key: {"gold": gold_amount, "updated": last_updated, "gold_int": gold_int}}
        )

    cnx = mysql.connector.connect(**sql_config)
    cursor = cnx.cursor()
    for key in tokeninfo_dict:
        sql = """INSERT INTO currentgold (Region, Gold)
        VALUES(%s, %s) ON DUPLICATE KEY UPDATE Region = VALUES(Region), Gold = VALUES(Gold);"""
        val = (key, tokeninfo_dict[key]["gold"])
        cursor.execute(sql, val)
        cnx.commit()
    cnx.close()

    for region in ["eu", "us", "kr"]:
        cnx = mysql.connector.connect(**sql_config)
        cursor = cnx.cursor()
        sql = "select * from goldhistory where region = %s order by date desc;"
        val = (region,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        rowcount = cursor.rowcount
        cnx.close()
        if rowcount == 0:
            cnx = mysql.connector.connect(**sql_config)
            cursor = cnx.cursor()
            sql = """INSERT INTO goldhistory (Date, GoldHigh, Region, gold_int)
            VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE Date = VALUES(Date), GoldHigh = VALUES(GoldHigh), Region = VALUES(Region), gold_int = VALUES(gold_int);"""
            val = (
                this_day,
                tokeninfo_dict[region]["gold"],
                region,
                tokeninfo_dict[region]["gold_int"],
            )
            cursor.execute(sql, val)
            cnx.commit()
            cnx.close()
        else:
            result_date = result[0][0]
            result_gold_int = result[0][3]
            if (
                this_day > result_date
                or tokeninfo_dict[region]["gold_int"] > result_gold_int
            ):
                cnx = mysql.connector.connect(**sql_config)
                cursor = cnx.cursor()
                sql = """INSERT INTO goldhistory (Date, GoldHigh, Region, gold_int)
                VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE Date = VALUES(Date), GoldHigh = VALUES(GoldHigh), Region = VALUES(Region), gold_int = VALUES(gold_int);"""
                val = (
                    this_day,
                    tokeninfo_dict[region]["gold"],
                    region,
                    tokeninfo_dict[region]["gold_int"],
                )
                cursor.execute(sql, val)
                cnx.commit()
                cnx.close()
            else:
                pass
