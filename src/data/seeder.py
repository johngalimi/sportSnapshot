import psycopg2 as db
import config


class Seeder:
    def __init__(self):
        self.league_map = {}
        self.team_map = {}
        self.normalized_team_name_map = {}
        self.seasons = []

    def get_seasons(self, base_year, years_back):
        self.seasons = [season for season in range(base_year - years_back, base_year)]

    def construct_mappings(self):

        connection = db.connect(
            database=config.DB_database,
            user=config.DB_user,
            password=config.DB_password,
            host=config.DB_host,
            port=config.DB_port,
        )

        cursor = connection.cursor()

        select_leagues = """
            SELECT
                league.id,
                league.league_sport
            FROM tblLeague league;
        """

        cursor.execute(select_leagues)

        for league in cursor:
            (league_id, league_sport) = league
            self.league_map[league_id] = league_sport

        select_teams = """
            SELECT
                team.id,
                team.team_abbr,
                team.league_id,
                team.team_location,
                team.team_name
            FROM tblTeam team;
        """

        cursor.execute(select_teams)

        for team in cursor:
            (team_id, team_abbr, league_id, team_location, team_name) = team
            self.team_map[team_id] = {"team_abbr": team_abbr, "league_id": league_id}

            lowercase_team_key = f"{team_location}{team_name}".replace(" ", "").lower()
            self.normalized_team_name_map[lowercase_team_key] = team_id

        connection.close()
        cursor.close()
