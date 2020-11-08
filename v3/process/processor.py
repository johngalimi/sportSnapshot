import json
import pandas as pd
from datetime import datetime


class Processor:
    def get_raw(self, sport, team, season):
        with open(f"../crawl/raw_results/{sport}/{season}_{team}.json") as f:
            raw_data = json.load(f)

        return raw_data

    def get_league_from_sport(self, sport):
        league_lookup = {"basketball": "NBA", "hockey": "NHL"}
        return league_lookup.get(sport, None)

    def get_season_string(self, season):
        return f"{season-1}-{season-2000}"

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
        processed_game = {
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

        # we should just be inheriting from a base processor and delegating league-specific logic to child classes
        if sport == "basketball":

            # parsing game date
            raw_game_date = "".join(game_record["date_game"].split(",")[1:]).lstrip()

            processed_game["game_date"] = datetime.strptime(
                raw_game_date, "%b %d %Y"
            ).date()

            # processing bit columns
            processed_game["is_team_home"] = "@" not in game_record["game_location"]
            processed_game["is_overtime"] = "OT" in game_record["overtimes"]

            # getting team and opponent information
            processed_game["league_name"] = self.get_league_from_sport(sport)
            processed_game["season"] = self.get_season_string(season)
            processed_game["team_name"] = team
            processed_game["opponent_name"] = game_record["opp_name"]
            processed_game["team_points"] = game_record["pts"]
            processed_game["opponent_points"] = game_record["opp_pts"]

        elif sport == "hockey":

            # parsing game date
            processed_game["game_date"] = datetime.strptime(
                game_record["date_game"], "%Y-%m-%d"
            ).date()

            # processing bit columns
            processed_game["is_team_home"] = "@" not in game_record["game_location"]

            processed_game["is_overtime"] = any(
                ot_identifier in game_record["overtimes"]
                for ot_identifier in ["OT", "SO"]
            )

            # getting team and opponent information
            processed_game["league_name"] = self.get_league_from_sport(sport)
            processed_game["season"] = self.get_season_string(season)
            processed_game["team_name"] = team
            processed_game["opponent_name"] = game_record["opp_name"]
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
        season_df.to_csv("games.csv", mode="a", index=False, header=False)


if __name__ == "__main__":
    processor = Processor()

    schedules_to_process = [
        ("basketball", "LAL", 2019),
        ("basketball", "CLE", 2011),
        ("hockey", "WSH", 2015),
        ("hockey", "STL", 2017),
    ]

    for sport, team, season in schedules_to_process:
        games = processor.process(sport, team, season)
        processor.write_processed_games(games)