WITH season_records AS (
    SELECT
        league.league_abbr,
        team.team_abbr,
        game.game_season,
        SUM(CASE WHEN game.team_points > game.opponent_points THEN 1 ELSE 0 END) wins,
        SUM(CASE WHEN game.team_points < game.opponent_points AND game.is_overtime IS FALSE THEN 1 ELSE 0 END) losses,
        SUM(CASE WHEN game.team_points < game.opponent_points AND game.is_overtime IS TRUE THEN 1 ELSE 0 END) ot_losses
    FROM tblGameRaw game
    INNER JOIN tblTeam team
        ON game.team_id = team.id
    INNER JOIN tblLeague league
        ON team.league_id = league.id
    GROUP BY
        league.league_abbr,
        team.team_abbr,
        game.game_season
    ORDER BY
        league.league_abbr, team.team_abbr, game.game_season DESC
),

nhl_points AS (
    SELECT 
        season_records.game_season,
        season_records.team_abbr,
        ((2 * wins) + ot_losses) points
    FROM season_records
    WHERE 
        season_records.league_abbr = 'NHL'
)

-- TODO: cut by conference / division and add tiebreaker (OTW) in ranking calculation
SELECT 
    nhl_points.game_season,
    nhl_points.team_abbr,
    nhl_points.points,
    ROW_NUMBER() OVER (PARTITION BY nhl_points.game_season ORDER BY nhl_points.points DESC) ranking
FROM nhl_points
ORDER BY nhl_points.game_season DESC, ranking