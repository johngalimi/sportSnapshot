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
        
        for i, game in enumerate(games):
            print(' ')
            print(i)
            print(game)


if __name__ == '__main__':
    test_url = 'https://basketball-reference.com/teams/BOS/2017_games.html'

    test_schedule = Schedule(test_url)
    test_schedule.clean_games()
