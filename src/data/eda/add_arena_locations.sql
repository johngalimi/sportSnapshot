DROP TABLE IF EXISTS tblArena;
CREATE TABLE tblArena (
    team_id INT,
    arena_lat FLOAT NULL,
    arena_lon FLOAT NULL
);

-- https://raw.githubusercontent.com/nhlscorebot/arenas/master/teams.json
INSERT INTO tblArena (team_id, arena_lat, arena_lon) VALUES
    (34, 42.3662019, -71.0643293),
    (35, 27.942742, -82.4539604),
    (36, 43.64333, -79.37917),
    (37, 26.15833, -80.32556),
    (38, 45.49611, -73.56944),
    (39, 42.875, -78.87639),
    (40, 45.29694, -75.92722),
    (41, 42.32528, -83.05139),
    (42, 38.89806, -77.02083),
    (43, 39.90111, -71.0622278),
    (44, 40.43944, -79.98917),
    (45, 35.80333, -78.72194),
    (46, 39.9692833, -83.0061111),
    (47, 40.72278, -73.59056),
    (48, 40.75056, -73.99361),
    (49, 40.73361, -74.17111),
    (50, 38.62667, -90.2025),
    (51, 39.74861, -105.0075),
    (52, 32.79056, -96.81028),
    (53, 49.89278, -97.14361),
    (54, 36.15917, -86.77861),
    (55, 44.94472, -93.10111),
    (56, 41.88056, -87.67417),
    (57, 36.102881, -115.1806157),
    (58, 53.57139, -113.45611),
    (59, 51.0375, -114.05194),
    (60, 49.27778, -123.10889),
    (61, 33.53194, -112.26111),
    (62, 33.80778, -117.87667),
    (63, 34.04306, -118.26722),
    (64, 37.33278, -121.90111),
    (65, 33.53194, -112.26111),
    (66, 33.7572935, -84.3985077)
;

WITH game_origins AS (
    SELECT
        game.id AS game_id,
        CASE 
            WHEN game.is_team_home IS TRUE THEN game.team_id
            ELSE game.opponent_id
        END AS origin_team_id
    FROM tblGameRaw game
),

game_locations AS (
    SELECT
        origin.game_id,
        arena.arena_lat AS game_lat,
        arena.arena_lon AS game_lon
    FROM game_origins origin
    LEFT JOIN tblArena arena
        ON origin.origin_team_id = arena.team_id
),

latest_bos_nhl_games AS (
    SELECT
        game.game_date,
        team.team_abbr,
        opponent.team_abbr AS opponent_abbr,
        game.team_points,
        game.opponent_points,
        locations.game_lat,
        locations.game_lon
    FROM tblGameRaw game
    INNER JOIN tblTeam team ON game.team_id = team.id
    INNER JOIN tblTeam opponent ON game.opponent_id = opponent.id
    INNER JOIN tblLeague league ON team.league_id = league.id
    INNER JOIN game_locations locations ON game.id = locations.game_id
    WHERE league.id = 2 --only have NHL arenas
        AND team.team_abbr = 'BOS' 
        AND game.game_season = 2019
)

SELECT * FROM latest_bos_nhl_games