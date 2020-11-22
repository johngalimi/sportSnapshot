import os
import json
import logging
import pandas as pd
from datetime import datetime

from seeder import Seeder


class ScheduleProcessor:

    seeder = Seeder()

    # define processed game skeleton object
    PROCESSED_GAME = {
        "league_name": None,
        "season": None,
        "game_date": None,
        "is_team_home": None,
        "is_overtime": None,
        "team_name": None,
        "opponent_name": None,
        "team_points": None,
        "opponent_points": None,
    }

    def get_raw(self, sport, team, season):

        if not os.path.isfile(f"results/{sport}/{season}_{team}.json"):
            logging.warning(f"Raw crawl result not available")
            return {}

        with open(f"results/{sport}/{season}_{team}.json") as f:
            raw_data = json.load(f)

        return raw_data

    def get_league_from_sport(self, sport):
        league_lookup = {"basketball": "NBA", "hockey": "NHL"}
        return league_lookup.get(sport, None)

    def get_team_from_abbreviation(self, sport, team):

        # TODO -- this should happen once at instantiation of processor rather than on every individual result
        team_lookup = self.seeder.construct_team_lookup(sport)

        return team_lookup[team]

    def get_season_string(self, season):
        return f"{season-1}-{season-2000}"

    def get_is_team_home(self, location_column_value):
        return "@" not in location_column_value

    def get_is_overtime(self, sport, overtime_column_value):

        if sport == "basketball":
            return "OT" in overtime_column_value

        elif sport == "hockey":
            return any(
                ot_identifier in overtime_column_value for ot_identifier in ["OT", "SO"]
            )

    def get_game_date(self, sport, date_column_value):

        if sport == "basketball":

            raw_game_date = "".join(
                game_record[date_column_value].split(",")[1:]
            ).lstrip()

            return datetime.strptime(raw_game_date, "%b %d %Y").date()

        elif sport == "hockey":

            return datetime.strptime(date_column_value, "%Y-%m-%d").date()

    def get_game_date(self, sport, date_column_value):

        if sport == "basketball":

            raw_game_date = "".join(date_column_value.split(",")[1:]).lstrip()

            return datetime.strptime(raw_game_date, "%b %d %Y").date()

        elif sport == "hockey":

            return datetime.strptime(date_column_value, "%Y-%m-%d").date()

    def process_games(self, season_data):

        games = season_data.get("games", [])

        processed_games = [
            self.process_game(
                season_data["sport"], season_data["team"], season_data["season"], game
            )
            for game in games
        ]

        return processed_games

    def process_game(self, sport, team, season, game_record):

        # define processed game skeleton object
        processed_game = self.PROCESSED_GAME.copy()

        # get game date
        processed_game["game_date"] = self.get_game_date(
            sport, game_record["date_game"]
        )

        processed_game["is_team_home"] = self.get_is_team_home(
            game_record["game_location"]
        )
        processed_game["is_overtime"] = self.get_is_overtime(
            sport, game_record["overtimes"]
        )

        # getting team and opponent information
        processed_game["league_name"] = self.get_league_from_sport(sport)
        processed_game["season"] = self.get_season_string(season)
        processed_game["team_name"] = self.get_team_from_abbreviation(sport, team)
        processed_game["opponent_name"] = game_record["opp_name"]

        # we should just be inheriting from a base processor and delegating league-specific logic to child classes
        if sport == "basketball":
            processed_game["team_points"] = game_record["pts"]
            processed_game["opponent_points"] = game_record["opp_pts"]

        elif sport == "hockey":
            processed_game["team_points"] = game_record["goals"]
            processed_game["opponent_points"] = game_record["opp_goals"]

        return processed_game

    def process(self, sport, team, season):
        raw_data = self.get_raw(sport, team, season)
        processed_games = self.process_games(raw_data)

        return processed_games

    def write_processed_games(self, processed_games):
        season_df = pd.DataFrame(processed_games)

        # write to csv in "a" (append) mode
        # need to include headers only at the top when appending
        season_df.to_csv("results/processed_games.csv", mode="a", index=False)


if __name__ == "__main__":

    start_time = datetime.now()
    logging.warning(f"Processing started, current time: {start_time}")

    schedule_processor = ScheduleProcessor()

    seeder = Seeder()

    sports = ["hockey", "basketball"]
    seasons = seeder.get_seasons(base_year=2020, years_back=2)

    master_processed_games = []

    for sport in sports:
        teams = seeder.get_teams(sport)

        for team_metadata in teams:
            (team_abbr, team_location, team_name) = team_metadata

            for season in seasons:

                logging.warning(f"---> Started {sport}.{team_abbr}.{season}")

                master_processed_games.extend(
                    schedule_processor.process(sport, team_abbr, season)
                )

                logging.warning(f"---> Finished {sport}.{team_abbr}.{season}")

    schedule_processor.write_processed_games(master_processed_games)

    logging.warning(f"Processing complete, time elapsed: {datetime.now() - start_time}")
