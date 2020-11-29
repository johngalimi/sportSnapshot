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

        if not os.path.exists(f"data/results/{sport}"):
            os.makedirs(f"data/results/{sport}")

        # file write not currently working for nonexistent jsons
        with open(f"data/results/{sport}/{season}_{team}.json", "w") as f:
            json.dump(schedule_data, f)

    def crawl(self, sport, team, season, team_metadata):
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

    seeder = Seeder()

    seasons = seeder.get_seasons(base_year=BASE_YEAR, years_back=YEARS_BACK)

    seasons = seasons[0:2]

    # seeder.get_teams()

    print(seeder.TEAMS)

    seeder.populate()

    print(seeder.LEAGUES)

    for sport in SPORTS_TO_CRAWL:

        teams = seeder.get_teams_by_sport(sport)

        teams = teams[0:3]

        for team_metadata in teams:
            (team_abbr, team_location, team_name) = team_metadata

            for season in seasons:
                logging.warning(f"---> Started {sport}.{team_abbr}.{season}")

                try:
                    schedule_crawler.crawl(sport, team_abbr, season, team_metadata)

                except Exception as e:
                    logging.warning(f"FAILED TO CRAWL, ERROR {e}")
                    pass

                logging.warning(f"---> Finished {sport}.{team_abbr}.{season}")

    logging.warning(f"Crawling complete, time elapsed: {datetime.now() - start_time}")
