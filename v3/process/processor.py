import json
import logging
import pandas as pd
from datetime import datetime


class Processor:

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
        with open(f"../crawl/raw_results/{sport}/{season}_{team}.json") as f:
            raw_data = json.load(f)

        return raw_data

    def get_league_from_sport(self, sport):
        league_lookup = {"basketball": "NBA", "hockey": "NHL"}
        return league_lookup.get(sport, None)

    def get_team_from_abbreviation(self, sport, team):
        team_lookup = {
            "basketball": {"CLE": "Cleveland Cavaliers", "LAL": "Los Angeles Lakers"},
            "hockey": {"WSH": "Washington Capitals", "STL": "St. Louis Blues"},
        }

        return team_lookup[sport][team]

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

        processed_games = [
            self.process_game(
                season_data["sport"], season_data["team"], season_data["season"], game
            )
            for game in season_data["games"]
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
        season_df.to_csv("games.csv", mode="a", index=False)


if __name__ == "__main__":
    start_time = datetime.now()
    logging.warning(f"Processing started, current time: {start_time}")

    processor = Processor()

    schedules_to_process = [
        ("basketball", "LAL", 2019),
        ("basketball", "CLE", 2011),
        ("hockey", "WSH", 2015),
        ("hockey", "STL", 2017),
    ]

    master_processed_games = []

    for sport, team, season in schedules_to_process:
        logging.warning(f"---> Started {sport}.{team}.{season}")

        games = processor.process(sport, team, season)
        master_processed_games.extend(games)

        logging.warning(f"---> Finished {sport}.{team}.{season}")

    processor.write_processed_games(master_processed_games)

    logging.warning(f"Processing complete, time elapsed: {datetime.now() - start_time}")