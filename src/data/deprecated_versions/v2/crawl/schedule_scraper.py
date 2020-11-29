import datetime
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
        soup = BeautifulSoup(page.content, "html.parser")

        return soup

    def get_table(self):
        soup = self.get_soup()
        table = soup.find("table", {"id": "games"})

        return table

    def parse_row(self, row):
        game = {}

        for tag in row:
            game[tag.attrs["data-stat"]] = tag.text

        return game

    def parse_table(self):
        table = self.get_table()

        tr_rows = table.find_all("tr")
        td_rows = [row.findChildren(name="td") for row in tr_rows]

        games = []

        for td_row in td_rows:
            data = self.parse_row(td_row)

            if len(data) > 0:
                games.append(data)

        return games

    def get_games(self):
        games = self.parse_table()

        # likely extract out to constant file
        target_fields = [
            "date_game",
            "opp_name",
            "pts",
            "opp_pts",
            "wins",
            "losses",
            "game_streak",
        ]

        extracted_games = []

        for game in games:
            extracted_game = {}

            for target_field in target_fields:
                extracted_game[target_field] = game[target_field]

            extracted_game["team"] = self.team
            extracted_game["season"] = self.season

            extracted_games.append(extracted_game)

        return extracted_games

    def clean_game(self, game):

        print(game)

        clean_game = {}

        dt_game_date = datetime.datetime.strptime(game["date_game"], "%a, %b %d, %Y")
        dt_game_date = dt_game_date.date()

        clean_game["scDate"] = dt_game_date

        numerical_cols = ["pts", "opp_pts", "wins", "losses"]

        for numerical_col in numerical_cols:
            raw_value = game[numerical_col]

            # major bandaid here
            if numerical_col == "opp_pts":
                numerical_col = "oppPts"

            col_name = "sc" + numerical_col[0].upper() + numerical_col[1:]

            clean_game[col_name] = int(raw_value)

        print(clean_game)

    def clean_games(self):

        games = self.get_games()

        test = games[0]

        self.clean_game(test)


if __name__ == "__main__":

    team = "LAL"
    season = "2007"

    test_schedule = Schedule(team, season)
    test_schedule.clean_games()