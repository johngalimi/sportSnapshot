import json
import requests
from bs4 import BeautifulSoup


class Crawler:
    def construct_url(self, sport, team, season):
        return (
            f"https://www.{sport}-reference.com/teams/{team}/{str(season)}_games.html"
        )

    def get_html(self, url):
        return requests.get(url)

    def get_response_text(self, response):
        return response.text

    def get_soup(self, response):
        return BeautifulSoup(response, features="html.parser")

    def get_table(self, soup):
        return soup.find("table", {"id": "games"})

    def parse_table(self, table):
        table_rows = table.find_all("tr")

        child_rows = [row.findChildren(name="td") for row in table_rows]

        processed_rows = []
        for row in child_rows:
            processed_row = self.parse_row(row)

            if processed_row:
                processed_rows.append(processed_row)

        return processed_rows

    def parse_row(self, row):
        return {tag.attrs["data-stat"]: tag.text for tag in row}

    def construct_json(self, sport, team, season, games):
        return {"sport": sport, "team": team, "season": season, "games": games}

    def crawl(self, sport, team, season):
        url = self.construct_url(sport, team, season)
        blob = self.get_html(url)
        text = self.get_response_text(blob)
        soup = self.get_soup(text)
        raw_table = self.get_table(soup)

        parsed_games = self.parse_table(raw_table)

        schedule_dict = self.construct_json(sport, team, season, parsed_games)

        with open(f"raw_results/{sport}/{season}_{team}.json", "w") as f:
            json.dump(schedule_dict, f)

        return schedule_dict


if __name__ == "__main__":
    crawler = Crawler()

    schedules_to_crawl = [
        ("basketball", "LAL", 2019),
        ("basketball", "CLE", 2011),
        ("hockey", "STL", 2017),
        ("hockey", "WSH", 2015),
    ]

    for sport, team, season in schedules_to_crawl:
        games = crawler.crawl(sport, team, season)
