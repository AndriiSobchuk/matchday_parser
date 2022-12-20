import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3

### Getting current date
match_day = datetime.now()
match_day = match_day.strftime("%Y-%m-%d")

### Matchday parsing (for https://fbref.com/*)

class MatchdayParser:

    def __init__(self, url):
        def __init__(self, url):
            self.url = url
            try:
                self.url = requests.get(url, timeout=5)
                self.url = BeautifulSoup(self.url.text, "html.parser")
                self.url = self.url.find('table')
            except requests.exceptions.HTTPError as errHTTP:
                print("Http Error: ", errHTTP)
            except requests.exceptions.ConnectionError as errConnection:
                print("Error Connecting: ", errConnection)
            except requests.exceptions.Timeout as errTimeout:
                print("Timeout Error: ", errTimeout)
            except requests.exceptions.RequestException as err:
                print("Something went wrong with getting url value, please check: ", err)

    # print URL get result
    def get_url(self):
        print(self.url)

    # write data to DB from URL
    def get_schedule(self):
        #### DB CONNECTION ####
        db_connect = sqlite3.connect('prog66.db')
        cursor = db_connect.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS matchday(wk text, m_day text, m_date text, m_time text, m_home text, m_score text, m_away text, unique (m_date, m_home));')
        insert_query = 'INSERT OR IGNORE INTO matchday VALUES (?, ?, ?, ?, ?, ?, ?);'    #prevent adding duplicates

        ### INSERT INTO DB MATCHDAY DATA ###
        result_schedule = '\n'
        for i in self.url.find_all('tbody'):
            rows = i.find_all('tr')
            tmp = 0
            counter = 0
            for row in rows:
                wk = row.find_all('th', class_='right')[0].text
                m_day = row.find_all('td', class_='left')[0].text
                m_date = row.find_all('td', class_='left')[1].text
                m_time = row.find_all('td', class_='right')[0].text
                m_home = row.find_all('td', class_='right')[1].text
                m_score = row.find_all('td', class_='center')[0].text
                m_away = row.find_all('td', class_='left')[2].text
                # href = row.find_all('td', class_='left')[5].find('a', href=True)['href'] --> get link to match report
                if str(match_day) <= m_date:
                    # rr = row.find_all('tr', class_='spacer partial_table result_all') --> separation of weaks
                    if tmp == 0 or counter <= 1:
                        tmp = wk
                        counter += 1
                    if int(tmp) == int(wk):
                        # print(wk, m_day, m_date, m_time, m_home, m_score, m_away)
                        match = m_day + ' ' + m_date + ' ' + m_time + ' ' + m_home + ' ' + m_score + ' ' + m_away
                        cursor.execute(insert_query, (wk, m_day, m_date, m_time, m_home, m_score, m_away))
                        result_schedule += match + '\n'
        # verify update result
        if cursor.lastrowid == 0:
            print('No updates found')
        else:
            print('Schedule updated successfully')

        #### CLOSE CONNECTION TO DB ####
        db_connect.commit()
        db_connect.close()

    # read data from DB
    def get_data_from_db(self, data_value):
        conn_db = sqlite3.connect('prog66.db')
        cursor = conn_db.cursor()
        #qwe = "SELECT wk, m_day, m_time, m_home, m_score, m_away FROM matchday WHERE m_date =(?)"
        select_query = "SELECT wk, m_day, m_time, m_home, m_score, m_away FROM matchday WHERE m_date =(?)"
        cursor.execute(select_query, [data_value])
        for i in cursor.fetchall():
            print(*i)
        conn_db.commit()
        conn_db.close()

