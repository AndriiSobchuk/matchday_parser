from ClassMatchdayParser import LeaguesMatchday, dict_leagues_scores
import mysql.connector
from DB_connector import db_connect

class MatchdayDB:

    #initialize and create table if no exists
    def __init__(self):
        cursor = db_connect.cursor()
        cursor.execute("USE DB")
        cursor.execute('CREATE TABLE IF NOT EXISTS matchday(country text, league text, wk text, m_day text, m_date text, m_time text, m_home text, m_score text, m_away text, unique (m_date(255), m_home(255)));')

    #get output from Leagues matchday
    def printData(self):
        createLeaguesMatchday = LeaguesMatchday(dict_leagues=dict_leagues_scores)
        getListMatchday = createLeaguesMatchday.getDataFromValueURL()
        print(getListMatchday)

    #insert method
    def insertData(self):
        cursor = db_connect.cursor()
        cursor.execute("USE DB")
        callParserClass = LeaguesMatchday(dict_leagues=dict_leagues_scores)
        callDataFromValueURL = callParserClass.getDataFromValueURL()
        for country in callDataFromValueURL:
            for game in country:
                query_string = 'INSERT IGNORE INTO matchday VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
                cursor.execute(query_string, game)
        db_connect.commit()
        db_connect.close()

    # select method
    def get_data_from_db(self, data_value):
        db_connect.reconnect()
        cursor = db_connect.cursor()
        cursor.execute("USE DB")
        select_query = "SELECT wk, m_day, m_time, m_home, m_score, m_away FROM matchday WHERE m_date =%s"
        cursor.execute(select_query, [data_value])
        for cell in cursor.fetchall():
            print(*cell)
        db_connect.commit()
        db_connect.close()

    # update method


awd = MatchdayDB()
awd.insertData()
#awd = MatchdayDB('andr.db')
awd.get_data_from_db('2022-12-29')
