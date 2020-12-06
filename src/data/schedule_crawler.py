import os
import json
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from base_crawler import BaseCrawler
from seeder import Seeder
from config import BASE_YEAR, YEARS_BACK, SPORTS_TO_CRAWL


class ScheduleCrawler(BaseCrawler):
    _seeder = Seeder()

    def construct_schedule_url(self, team_id, season):

        league_sport = self._seeder.league_map[
            self._seeder.team_map[team_id]["league_id"]
        ]
        team_abbr = self._seeder.team_map[team_id]["team_abbr"]

        schedule_url = f"https://www.{league_sport}-reference.com/teams/{team_abbr}/{str(season)}_games.html"

        return schedule_url

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

    def crawl(self, team_id, season):

        schedule_url = self.construct_schedule_url(team_id, season)

        blob = self.get_html(schedule_url)
        text = self.get_response_text(blob)
        soup = self.get_soup(text)

        raw_game_table = self.get_game_table(soup)

        parsed_games = self.parse_game_table(raw_game_table)

        schedule_payload = {"team_id": team_id, "season": season, "games": parsed_games}

        results_directory = f"data/results"

        if not os.path.exists(results_directory):
            os.makedirs(results_directory)

        # file write not currently working for nonexistent jsons
        with open(f"{results_directory}/{season}_{team_id}.json", "w") as f:
            json.dump(schedule_payload, f)


if __name__ == "__main__":

    start_time = datetime.now()
    logging.warning(f"Crawling started, current time: {start_time}")

    schedule_crawler = ScheduleCrawler()

    schedule_crawler._seeder.get_seasons(base_year=BASE_YEAR, years_back=YEARS_BACK)
    schedule_crawler._seeder.construct_mappings()

    for team_id in schedule_crawler._seeder.team_map:
        for season in schedule_crawler._seeder.seasons:
            logging.warning(f"---> Started {team_id}.{season}")

            try:
                schedule_crawler.crawl(team_id, season)
            except Exception as e:
                logging.warning(f"FAILED TO CRAWL, ERROR {e}")
                pass

            logging.warning(f"---> Finished {team_id}.{season}")

    logging.warning(f"Crawling complete, time elapsed: {datetime.now() - start_time}")
