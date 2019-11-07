import requests
from bs4 import BeautifulSoup


class Schedule:

    url_template = "https://basketball-reference.com/teams/{}/{}_games.html"

    def __init__(self, team, season):
        self.team = team
        self.season = season
        self.url = self.url_template.format(team, season)


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
        
        for game in games:
            cleaned_game = {}

            for target_field in target_fields:
                cleaned_game[target_field] = game[target_field]

            cleaned_game['team'] = self.team
            cleaned_game['season'] = self.season

            cleaned_games.append(cleaned_game)
        
        return cleaned_games 


if __name__ == '__main__':

    team = 'BOS'
    season = '2018'
    
    test_schedule = Schedule(team, season)
    test_schedule.clean_games()
