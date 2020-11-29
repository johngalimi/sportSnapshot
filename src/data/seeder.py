import psycopg2 as db


class Seeder:
    team_lookup = {"basketball": {}, "hockey": {}}

    TEAMS = {"basketball": {}, "hockey": {}}

    LEAGUES = {}

    def get_seasons(self, base_year, years_back):
        return [season for season in range(base_year - years_back, base_year)]

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
                league.sport_name
            FROM tblLeague league;
        """

        cursor.execute(select_leagues)

        for league in cursor:
            (_id, _abbr, _sport) = league
            self.LEAGUES[_id] = {
                "sport": _sport,
                "abbr": _abbr,
                "teams": {} 
            }

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
                league.sport_name
            FROM tblTeam team
            INNER JOIN tblLeague league
                ON team.league_id = league.id;
        """

        cursor.execute(select_teams)

        for team in cursor:
            (team_id, team_abbr, team_location, team_name, league_id, sport_name) = team
            
            self.TEAMS[sport_name][team_abbr] = {
                "id": team_id,
                "name": f"{team_location} {team_name}",
                "league_id": league_id
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
