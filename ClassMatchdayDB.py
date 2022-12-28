from ClassMatchdayParser import LeaguesMatchday, dict_leagues_scores
import sqlite3

class MatchdayDB:

    #initialize and create table if no exists
    def __init__(self, DB_name):
        self.DB_name = sqlite3.connect(DB_name)
        self.cursor = self.DB_name.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS matchday(country text, league text, wk text, m_day text, m_date text, m_time text, m_home text, m_score text, m_away text, unique (m_date, m_home));')
        #or add here try / catch ?

    #get output from Leagues matchday
    def printData(self):
        createLeaguesMatchday = LeaguesMatchday(dict_leagues=dict_leagues_scores)
        getListMatchday = createLeaguesMatchday.getDataFromValueURL()
        print(getListMatchday)

    #insert method
    def insertData(self):
        callParserClass = LeaguesMatchday(dict_leagues=dict_leagues_scores)
        callDataFromValueURL = callParserClass.getDataFromValueURL()
        for country in callDataFromValueURL:
            for game in country:
                query_string = 'INSERT OR IGNORE INTO matchday VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'
                self.cursor.execute(query_string, game)
        self.DB_name.commit()
        self.DB_name.close()

    # select method
    def get_data_from_db(self, data_value):
        self.DB_name = sqlite3.connect('andr.db')
        self.cursor = self.DB_name.cursor()
        select_query = "SELECT wk, m_day, m_time, m_home, m_score, m_away FROM matchday WHERE m_date =(?)"
        self.cursor.execute(select_query, [data_value])
        for cell in self.cursor.fetchall():
            print(*cell)
        self.DB_name.commit()
        self.DB_name.close()

    # update method


awd = MatchdayDB('andr.db')
awd.insertData()
#awd = MatchdayDB('andr.db')
awd.get_data_from_db('2022-12-29')