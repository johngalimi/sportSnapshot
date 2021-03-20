SELECT league.league_abbr,
       game.game_season,
       game.game_date,
       team.team_abbr,
       opponent.team_abbr AS opponent_abbr,
       game.team_points,
       game.opponent_points
FROM tblGameRaw game
INNER JOIN tblTeam team ON game.team_id = team.id
INNER JOIN tblTeam opponent ON game.opponent_id = opponent.id
INNER JOIN tblLeague league ON team.league_id = league.id