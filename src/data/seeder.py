import psycopg2 as db
import config

class Seeder:
    def __init__(self):
        self.team_map = {}
        self.normalized_team_name_map = {}
        self.league_map = {}
        self.seasons = []

    # team_lookup = {"basketball": {}, "hockey": {}}

    # TEAMS = {"basketball": {}, "hockey": {}}

    # LEAGUES = {}

    # seasons = []
    # league_map = {}
    # team_map = {}

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

    def populate(self):
        connection = db.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="host.docker.internal",
            port="5432",
        )

        cursor = connection.cursor()

        select_leagues = """
            SELECT
                league.id,
                league.league_abbr,
                league.league_sport
            FROM tblLeague league;
        """

        cursor.execute(select_leagues)

        for league in cursor:
            (_id, _abbr, _sport) = league
            self.LEAGUES[_id] = {"sport": _sport, "abbr": _abbr, "teams": {}}

        select_teams = """
            SELECT
                team.id,
                team.team_abbr,
                league.id AS league_id
            FROM tblTeam team
            INNER JOIN tblLeague league
                ON team.league_id = league.id;
        """

        connection.close()
        cursor.close()

    def get_teams(self):
        connection = db.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="host.docker.internal",
            port="5432",
        )

        cursor = connection.cursor()

        select_teams = """
            SELECT
                team.id AS team_id,
                team.team_abbr,
                team.team_location,
                team.team_name,
                league.league_sport,
                team.league_id
            FROM tblTeam team
            INNER JOIN tblLeague league
                ON team.league_id = league.id;
        """

        cursor.execute(select_teams)

        for team in cursor:
            (
                team_id,
                team_abbr,
                team_location,
                team_name,
                league_sport,
                league_id,
            ) = team

            self.TEAMS[league_sport][team_abbr] = {
                "id": team_id,
                "name": f"{team_location} {team_name}",
                "league_id": league_id,
            }

        # team_list = [team for team in cursor]

        # team_dict = {
        #     _abbr: f"{_location} {_name}" for _abbr, _location, _name in team_list
        # }

        # self.team_lookup[sport].update(team_dict)

        connection.close()
        cursor.close()

        # return team_list

    def get_teams_by_sport(self, sport):

        connection = db.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="host.docker.internal",
            port="5432",
        )

        cursor = connection.cursor()

        select_teams_by_sport = """
            SELECT
                team_abbr,
                team_location,
                team_name
            FROM tblTeam
            WHERE league_id = {}
        """.format(
            {"basketball": 1, "hockey": 2}[sport]
        )

        cursor.execute(select_teams_by_sport)

        team_list = [team for team in cursor]

        team_dict = {
            _abbr: f"{_location} {_name}" for _abbr, _location, _name in team_list
        }

        self.team_lookup[sport].update(team_dict)

        connection.close()
        cursor.close()

        return team_list
