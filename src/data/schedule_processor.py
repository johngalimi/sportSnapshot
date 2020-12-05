import os
import json
import logging
import pandas as pd
import psycopg2 as db

from datetime import datetime
from psycopg2.extras import execute_values

import config
from seeder import Seeder


class ScheduleProcessor:
    _seeder = Seeder()


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

    # define processed game skeleton object
    GAME = {
        "game_date": None,
        "game_season": None,
        "team_id": None,
        "opponent_id": None,
        "team_points": None,
        "opponent_points": None,
        "is_team_home": None,
        "is_overtime": None,
    }

    def get_raw(self, sport, team, season):

        if not os.path.isfile(f"data/results/{sport}/{season}_{team}.json"):
            logging.warning(f"Raw crawl result not available")
            return {}

        with open(f"data/results/{sport}/{season}_{team}.json") as f:
            raw_data = json.load(f)

        return raw_data

    def get_league_from_sport(self, sport):
        league_lookup = {"basketball": "NBA", "hockey": "NHL"}
        return league_lookup.get(sport, None)

    def get_team_from_abbreviation(self, sport, team):
        return self.seeder.team_lookup[sport][team]

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

    def get_point_fields(self, sport, game_data):

        POINTS_TEAM, POINTS_OPPONENT = "team_points", "opponent_points"

        point_column_map = {
            "basketball": {POINTS_TEAM: "pts", POINTS_OPPONENT: "opp_pts"},
            "hockey": {POINTS_TEAM: "goals", POINTS_OPPONENT: "opp_goals"},
        }

        team_points = game_data[point_column_map[sport][POINTS_TEAM]]
        opponent_points = game_data[point_column_map[sport][POINTS_OPPONENT]]

        return (
            int(team_points) if team_points else 0,
            int(opponent_points) if opponent_points else 0,
        )

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

        # TODO -- process win streak

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

        (
            processed_game["team_points"],
            processed_game["opponent_points"],
        ) = self.get_point_fields(sport, game_record)

        uuid_component_time = int(
            datetime.combine(
                processed_game["game_date"], datetime.min.time()
            ).timestamp()
        )
        uuid_component_points = (
            processed_game["team_points"] + processed_game["opponent_points"]
        )

        processed_game["game_uuid"] = f"{uuid_component_time}-{uuid_component_points}"

        return processed_game

    def _process(self, sport, team, season):
        raw_data = self.get_raw(sport, team, season)
        processed_games = self.process_games(raw_data)

        return processed_games

    def get_raw_crawl_result(self, team_id, season):

        raw_crawl_file_path = f"data/results/{season}_{team_id}.json"

        if not os.path.isfile(raw_crawl_file_path):
            logging.warning(f"Raw crawl result not available")
            return {}

        with open(raw_crawl_file_path) as f:
            raw_data = json.load(f)

        return raw_data

    def process_raw_game(self, team_id, season, game_record):

        processed_game = self.GAME.copy()

        sport = self._seeder.league_map[self._seeder.team_map[team_id]["league_id"]]

        # get game date fields
        processed_game["game_date"] = self.get_game_date(
            sport, game_record["date_game"]
        )
        processed_game["game_season"] = season

        # get bool fields
        processed_game["is_team_home"] = self.get_is_team_home(
            game_record["game_location"]
        )
        processed_game["is_overtime"] = self.get_is_overtime(
            sport, game_record["overtimes"]
        )

        (
            processed_game["team_points"],
            processed_game["opponent_points"],
        ) = self.get_point_fields(sport, game_record)

        processed_game["team_id"] = team_id

        processed_game["opponent_id"] = self._seeder.normalized_team_name_map[
            game_record["opp_name"].replace(" ", "").lower()
        ]

        return processed_game

    def process(self, team_id, season):

        raw_crawl = self.get_raw_crawl_result(team_id, season)

        games = raw_crawl.get("games", [])

        processed_games = [
            self.process_raw_game(team_id, season, game) for game in games
        ]

        return processed_games

    def write_games_to_csv(self, games):
        # load into df to prepare for csv insert
        season_df = pd.DataFrame(games)

        # write to csv in "a" (append) mode
        # need to include headers only at the top when appending
        season_df.to_csv("data/results/processed_games.csv", mode="a", index=False)

    def write_games_to_db(self, games):
        connection = db.connect(
            database=config.DB_database,
            user=config.DB_user,
            password=config.DB_password,
            host=config.DB_host,
            port=config.DB_port,
        )

        cursor = connection.cursor()

        game_columns = games[0].keys()

        game_values = [[data_point for data_point in game.values()] for game in games]

        insert_tbl_game_raw = "INSERT INTO tblGameRaw ({}) VALUES %s".format(
            ",".join(game_columns)
        )

        execute_values(cursor, insert_tbl_game_raw, game_values)
        connection.commit()

        connection.close()
        cursor.close()


    def write_processed_games(self, processed_games):
        logging.warning(
            f"Writing processed games, expected row count: {len(processed_games)}"
        )

        self.write_games_to_csv(processed_games)

        self.write_games_to_db(processed_games)

if __name__ == "__main__":

    start_time = datetime.now()
    logging.warning(f"Processing started, current time: {start_time}")

    schedule_processor = ScheduleProcessor()

    schedule_processor._seeder.get_seasons(base_year=config.BASE_YEAR, years_back=config.YEARS_BACK)
    schedule_processor._seeder.construct_mappings()

    master_processed_games = []

    for team_id in schedule_processor._seeder.team_map:
        for season in schedule_processor._seeder.seasons:
            logging.warning(f"---> Started {team_id}.{season}")

            try:
                master_processed_games.extend(schedule_processor.process(team_id, season))
            except Exception as e:
                logging.warning(f"FAILED TO PROCESS, ERROR {e}")
                pass

            logging.warning(f"---> Finished {team_id}.{season}")

    schedule_processor.write_processed_games(master_processed_games)

    logging.warning(f"Processing complete, time elapsed: {datetime.now() - start_time}")
