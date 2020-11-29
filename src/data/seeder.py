import psycopg2 as db


class Seeder:
    team_lookup = {"basketball": {}, "hockey": {}}

    def get_seasons(self, base_year, years_back):
        return [season for season in range(base_year - years_back, base_year)]

    def get_teams(self, sport):
        
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
        """.format({"basketball": 1, "hockey": 2}[sport])

        cursor.execute(select_teams_by_sport)

        team_list = [team for team in cursor]

        team_dict = {_abbr: f"{_location} {_name}" for _abbr, _location, _name in team_list}

        self.team_lookup[sport].update(team_dict)

        connection.close()
        cursor.close()

        return team_list
