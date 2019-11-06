import requests
from bs4 import BeautifulSoup


class Schedule:

    def __init__(self, url):
        self.url = url


    def get_soup(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        return soup


    def get_table(self):
        soup = self.get_soup()
        table = soup.find('table', {'id': 'games'})

        return table


    def parse_row(self, row):
        game = {}

        for tag in row:
            game[tag.attrs['data-stat']] = tag.text

        return game


    def parse_table(self):
        table = self.get_table()
        tr_rows = table.find_all('tr')
        td_rows = [row.findChildren(name = 'td') for row in tr_rows]

        games = []

        for td_row in td_rows:
            data = self.parse_row(td_row)

            if len(data) > 0:
                games.append(data)

        return games


    def clean_games(self):
        games = self.parse_table()
        # get team name and season from url

        target_fields = [
                'date_game',
                'opp_name',
                'pts',
                'opp_pts',
                'wins',
                'losses',
                'game_streak',
             ]
        
        cleaned_games = []

        games = games[0:1]
        
        for game in games:
            cleaned_game = {}

            for target_field in target_fields:
                cleaned_game[target_field] = game[target_field]

            cleaned_games.append(cleaned_game)
            print(cleaned_games) 


if __name__ == '__main__':

    team = 'WAS'
    season = '2010'

    test_url = "https://basketball-reference.com/teams/{}/{}_games.html".format(team, season)
    
    test_schedule = Schedule(test_url)
    test_schedule.clean_games()
