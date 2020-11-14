import json
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from base_crawler import BaseCrawler


class ScheduleCrawler(BaseCrawler):
    def construct_url(self, sport, team, season):
        return (
            f"https://www.{sport}-reference.com/teams/{team}/{str(season)}_games.html"
        )

    def get_game_table(self, soup):
        return soup.find("table", {"id": "games"})

    def parse_game_table(self, table):
        table_rows = table.find_all("tr")

        child_rows = [row.findChildren(name="td") for row in table_rows]

        processed_rows = []
        for row in child_rows:
            processed_row = self.parse_game(row)

            if processed_row:
                processed_rows.append(processed_row)

        return processed_rows

    def parse_game(self, row):
        return {tag.attrs["data-stat"]: tag.text for tag in row}

    def construct_schedule_json(self, sport, team, season, games):
        return {"sport": sport, "team": team, "season": season, "games": games}

    def write_raw_crawl_results(self, sport, season, team, schedule_data):
        with open(f"raw_results/{sport}/{season}_{team}.json", "w") as f:
            json.dump(schedule_data, f)

    def crawl(self, sport, team, season):
        schedule_url = self.construct_url(sport, team, season)

        blob = self.get_html(schedule_url)
        text = self.get_response_text(blob)
        soup = self.get_soup(text)

        raw_game_table = self.get_game_table(soup)

        parsed_games = self.parse_game_table(raw_game_table)

        schedule_dict = self.construct_schedule_json(sport, team, season, parsed_games)

        self.write_raw_crawl_results(sport, season, team, schedule_dict)


if __name__ == "__main__":

    start_time = datetime.now()
    logging.warning(f"Crawling started, current time: {start_time}")

    schedule_crawler = ScheduleCrawler()

    schedules_to_crawl = [
        ("basketball", "LAL", 2019),
        ("basketball", "CLE", 2011),
        ("hockey", "STL", 2017),
        ("hockey", "WSH", 2015),
    ]

    for sport, team, season in schedules_to_crawl:
        logging.warning(f"---> Started {sport}.{team}.{season}")

        schedule_crawler.crawl(sport, team, season)

        logging.warning(f"---> Finished {sport}.{team}.{season}")

    logging.warning(f"Crawling complete, time elapsed: {datetime.now() - start_time}")