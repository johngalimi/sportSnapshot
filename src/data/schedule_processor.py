import os
import json
import logging
import pandas as pd
import psycopg2 as db

from datetime import datetime
from psycopg2.extras import execute_values

from seeder import Seeder
from config import BASE_YEAR, YEARS_BACK, SPORTS_TO_CRAWL


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

        uuid_component_time = int(datetime.combine(processed_game['game_date'], datetime.min.time()).timestamp())
        uuid_component_points = processed_game['team_points'] + processed_game['opponent_points']

        processed_game['game_uuid'] = f"{uuid_component_time}-{uuid_component_points}"

        return processed_game

    def process(self, sport, team, season):
        raw_data = self.get_raw(sport, team, season)
        processed_games = self.process_games(raw_data)

        return processed_games

    def write_games_to_csv(self, games):
        # load into df to prepare for csv insert
        season_df = pd.DataFrame(games)

        # write to csv in "a" (append) mode
        # need to include headers only at the top when appending
        season_df.to_csv("data/results/processed_games.csv", mode="a", index=False)

    def write_games_to_db(self, games):
        connection = db.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="host.docker.internal",
            port="5432",
        )

        cursor = connection.cursor()

        create_tbl_game = """
            DROP TABLE IF EXISTS tblGame;
            CREATE TABLE tblGame (
                id serial PRIMARY KEY,
                league_name VARCHAR(3) NOT NULL,
                season VARCHAR(8) NOT NULL,
                game_date DATE NOT NULL,
                is_team_home BOOLEAN NOT NULL,
                is_overtime BOOLEAN NOT NULL,
                team_name VARCHAR(50) NOT NULL,
                opponent_name VARCHAR(50) NOT NULL,
                team_points INT NOT NULL,
                opponent_points INT NOT NULL,
                game_uuid VARCHAR (25) NOT NULL
            );
        """

        cursor.execute(create_tbl_game)
        connection.commit()

        game_columns = games[0].keys()

        game_values = [
            [data_point for data_point in game.values()]
            for game in games
        ]

        insert_tbl_game = "INSERT INTO tblGame ({}) VALUES %s".format(
            ",".join(game_columns)
        )

        execute_values(cursor, insert_tbl_game, game_values)
        connection.commit()

        connection.close()
        cursor.close()

    def write_processed_games(self, processed_games):
        logging.warning(
            f"Writing processed games, expected row count: {len(processed_games)}"
        )

        self.write_games_to_csv(processed_games)

        # self.write_games_to_db(processed_games)

if __name__ == "__main__":

    start_time = datetime.now()
    logging.warning(f"Processing started, current time: {start_time}")

    schedule_processor = ScheduleProcessor()

    seeder = Seeder()

    seasons = seeder.get_seasons(base_year=BASE_YEAR, years_back=YEARS_BACK)

    seasons = seasons[0:2]

    master_processed_games = []

    for sport in SPORTS_TO_CRAWL:
        teams = seeder.get_teams(sport)

        teams = teams[0:3]

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
