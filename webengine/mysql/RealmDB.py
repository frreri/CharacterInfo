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
realms = api.get_realm_status("eu")
for realm_n in realms["realms"]:
    print("Inserting:", realm_n["name"], "into database!")
    sql = """INSERT INTO realms (name)
    VALUES (%s) ON DUPLICATE KEY UPDATE name = VALUES(name);"""
    val = (realm_n["name"],)
    cursor.execute(sql, val)
    cnx.commit()
    print(cursor.rowcount, "records inserted/updated.")
cnx.close()
