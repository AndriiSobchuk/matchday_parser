import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from LeaguesDirtionary import dict_leagues_scores


### Getting current date
match_day = datetime.now()
match_day = match_day.strftime("%Y-%m-%d")

### Matchday parsing (for https://fbref.com/*)
class LeaguesMatchday:

    parsed_list = [[] for _ in range(len(dict_leagues_scores.keys()))] # nested list to save matchday info for each league

    def __init__(self, dict_leagues):
        self.dict_leagues = dict_leagues

    def getDataFromValueURL(self):
        dict_counter = 0
        for key_name_of_country, url_of_league in  self.dict_leagues.items():
            league_name = url_of_league.split('/')[7].split('-Scores-and-Fixtures')[0]
            try:
                self.url = requests.get(url_of_league, timeout=5)
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
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

            #parsing data from url_of_league link
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
                        # rr = row.find_all('tr', class_='spacer partial_table result_all') --> separation of weeks
                        if tmp == 0 or counter <= 1:
                            tmp = wk
                            counter += 1
                        if int(tmp) == int(wk):
                            # print(wk, m_day, m_date, m_time, m_home, m_score, m_away)
                            #match = m_day + ' ' + m_date + ' ' + m_time + ' ' + m_home + ' ' + m_score + ' ' + m_away
                            #result_schedule += match + '\n'
                            self.parsed_list[dict_counter].append([key_name_of_country, league_name, wk, m_day, m_date, m_time, m_home, m_score, m_away])

            #verify if list with leagues matchday is empty
            if not any(self.parsed_list):
                print("No games scheduled for this day")

            dict_counter += 1 # move to the next league in the nested list

        return self.parsed_list

    def getList(self):
        for matchday in self.parsed_list:
            print(matchday)

    def getInfo(self):
        for item in self.dict_leagues.items():
            print(item)

    def getKeys(self):
        for key in self.dict_leagues.keys():
            print(key)

    def getValue(self):
        for value in self.dict_leagues.keys():
            print(value)

#asd = LeaguesMatchday(dict_leagues=dict_leagues_scores)

#asd.getInfo()
#asd.getDataFromValueURL()
#asd.getKeys()
#asd.getList()
