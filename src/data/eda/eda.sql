WITH outcomes AS (
    SELECT
        game.*,
        CASE
            WHEN game.team_points >= opponent_points THEN 1
            ELSE 0
        END AS is_team_win 
    FROM tblGameRaw game
    WHERE game.team_id = 31 and game.game_season = 2019
)

SELECT * FROM outcomes


    SELECT
        *
    FROM tblGameRaw game
    WHERE game.team_id = 31 and game.game_season = 2019