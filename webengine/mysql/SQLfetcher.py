import mysql.connector
import datetime
from config import MySQLconfig

sql_config = {
    "user": MySQLconfig.MYSQL_USER,
    "password": MySQLconfig.MYSQL_PASSWORD,
    "host": MySQLconfig.MYSQL_HOST,
    "database": MySQLconfig.MYSQL_DATABASE,
}


def SQLfetch():
    cnx = mysql.connector.connect(**sql_config)
    cursor = cnx.cursor()
    sql = "select name,class,avgeqilvl,thumbnail from wowcharacter where lvl =120 order by avgeqilvl desc limit 10;"
    cursor.execute(sql)
    results = cursor.fetchall()
    cnx.close()
    return results


def SQLfetchAll(fetch_scope):
    class_to_fetch = fetch_scope
    cnx = mysql.connector.connect(**sql_config)
    cursor = cnx.cursor()
    if class_to_fetch == "all":
        sql = "select * from wowcharacter;"
    else:
        sql = "select * from wowcharacter where class = '{}';".format(class_to_fetch)
    cursor.execute(sql)
    results = cursor.fetchall()
    cnx.close()
    return results


def SQLfetchRealm():
    cnx = mysql.connector.connect(**sql_config)
    cursor = cnx.cursor()
    sql = "select name from realms;"
    cursor.execute(sql)
    results = cursor.fetchall()
    r_list = []
    for x in results:
        r_list.append(x[0])
    cnx.close()
    return r_list


def SQLfetchRealmLower():
    cnx = mysql.connector.connect(**sql_config)
    cursor = cnx.cursor()
    sql = "select name from realms;"
    cursor.execute(sql)
    results = cursor.fetchall()
    r_listL = []
    for x in results:
        r_listL.append(x[0].lower())
    cnx.close()
    return r_listL


def SQLinsert(search_result, source):
    cnx = mysql.connector.connect(**sql_config)
    cursor = cnx.cursor()
    sql = """INSERT INTO searches (data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, submission_date, source)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE data1 = VALUES(data1), data2 = VALUES(data2), data3 = VALUES(data3), data4 = VALUES(data4),
    data5 = VALUES(data5), data6 = VALUES(data6), data7 = VALUES(data7), data8 = VALUES(data8), data9 = VALUES(data9), data10 = VALUES(data10),
    submission_date = VALUES(submission_date), source = VALUES(source);"""
    val = (
        search_result["name"],
        search_result["class"],
        search_result["race"],
        search_result["gender"],
        search_result["level"],
        search_result["ilvl"],
        search_result["guild"],
        search_result["realm"],
        search_result["hks"],
        search_result["name_with_title"],
        datetime.datetime.now(),
        source,
    )
    cursor.execute(sql, val)
    cnx.commit()
    cnx.close()


def SQLtokenFetchCurrent():
    cnx = mysql.connector.connect(**sql_config)
    cursor = cnx.cursor()
    sql = "select * from currentgold;"
    cursor.execute(sql)
    results = cursor.fetchall()
    cnx.close()
    return results


def SQLtokenFetchHistory():
    cnx = mysql.connector.connect(**sql_config)
    cursor = cnx.cursor()
    sql = "select * from goldhistory order by date desc, region asc;"
    cursor.execute(sql)
    results = cursor.fetchall()
    cnx.close()
    return results


def SQLtokenFetchMonthHigh():
    results = {}
    for region in ["eu", "kr", "us"]:
        cnx = mysql.connector.connect(**sql_config)
        cursor = cnx.cursor()
        the_month = str(datetime.date.today())[:8] + "00"
        sql = "select * from goldhistory where date > '{}' and region = '{}' order by gold_int desc;".format(
            the_month, region
        )
        cursor.execute(sql)
        sql_result = cursor.fetchall()
        results.update({region: {"gold": sql_result[0][1], "date": sql_result[0][0]}})
        cnx.close()
    return results


def SQLfetchSearch():
    cnx = mysql.connector.connect(**sql_config)
    cursor = cnx.cursor()
    sql = "select * from searches;"
    cursor.execute(sql)
    results = cursor.fetchall()
    cnx.close()
    return results
