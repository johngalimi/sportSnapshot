from constants import NBA_TEAMS, NHL_TEAMS


class Seeder:

    TEAMS = {"basketball": NBA_TEAMS, "hockey": NHL_TEAMS}

    def get_seasons(self, base_year, years_back):
        return [season for season in range(base_year - years_back, base_year)]

    def get_teams(self, sport):
        return self.TEAMS.get(sport, [])

    def construct_team_lookup(self, sport):
        teams = self.TEAMS.get(sport, None)

        if teams is None:
            return {}

        return {_abbr: f"{_location} {_name}" for _abbr, _location, _name in teams}