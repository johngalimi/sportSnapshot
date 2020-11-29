DROP TABLE IF EXISTS tblLeague;
CREATE TABLE tblLeague (
    id serial PRIMARY KEY,
    league_abbr VARCHAR (4) NOT NULL,
    sport_name VARCHAR (10) NOT NULL
);

INSERT INTO tblLeague (league_abbr, sport_name) VALUES
    ('NBA', 'basketball'),
    ('NHL', 'hockey')
;

DROP TABLE IF EXISTS tblTeam;
CREATE TABLE tblTeam (
    id serial PRIMARY KEY,
    league_id INT NOT NULL,
    team_abbr VARCHAR (5) NOT NULL,
    team_location VARCHAR (50) NOT NULL,
    team_name VARCHAR (50) NOT NULL
);

INSERT INTO tblTeam (league_id, team_abbr, team_location, team_name) VALUES 
    (1, 'MIL', 'Milwaukee', 'Bucks'),
    (1, 'TOR', 'Toronto', 'Raptors'),
    (1, 'BOS', 'Boston', 'Celtics'),
    (1, 'MIA', 'Miami', 'Heat'),
    (1, 'IND', 'Indiana', 'Pacers'),
    (1, 'PHI', 'Philadelphia', '76ers'),
    (1, 'BRK', 'Brooklyn', 'Nets'),
    (1, 'ORL', 'Orlando', 'Magic'),
    (1, 'WAS', 'Washington', 'Wizards'),
    (1, 'CHO', 'Charlotte', 'Hornets'),
    (1, 'CHI', 'Chicago', 'Bulls'),
    (1, 'NYK', 'New York', 'Knicks'),
    (1, 'DET', 'Detroit', 'Pistons'),
    (1, 'ATL', 'Atlanta', 'Hawks'),
    (1, 'CLE', 'Cleveland', 'Cavaliers'),
    (1, 'LAL', 'Los Angeles', 'Lakers'),
    (1, 'LAC', 'Los Angeles', 'Clippers'),
    (1, 'DEN', 'Denver', 'Nuggets'),
    (1, 'UTA', 'Utah', 'Jazz'),
    (1, 'OKC', 'Oklahoma City', 'Thunder'),
    (1, 'HOU', 'Houston', 'Rockets'),
    (1, 'DAL', 'Dallas', 'Mavericks'),
    (1, 'MEM', 'Memphis', 'Grizzlies'),
    (1, 'POR', 'Portland', 'Trailblazers'),
    (1, 'NOP', 'New Orleans', 'Pelicans'),
    (1, 'SAC', 'Sacramento', 'Kings'),
    (1, 'SAS', 'San Antonio', 'Spurs'),
    (1, 'PHO', 'Phoenix', 'Suns'),
    (1, 'MIN', 'Minnesota', 'Timberwolves'),
    (1, 'GSW', 'Golden State', 'Warriors'),
    (2, 'BOS', 'Boston', 'Bruins'),
    (2, 'TBL', 'Tampa Bay', 'Lightning'),
    (2, 'TOR', 'Toronto', 'Maple Leafs'),
    (2, 'FLA', 'Florida', 'Panthers'),
    (2, 'MTL', 'Montreal', 'Canadiens'),
    (2, 'BUF', 'Buffalo', 'Sabres'),
    (2, 'OTT', 'Ottawa', 'Senators'),
    (2, 'DET', 'Detroit', 'Red Wings'),
    (2, 'WSH', 'Washington', 'Capitals'),
    (2, 'PHI', 'Philadelphia', 'Flyers'),
    (2, 'PIT', 'Pittsburgh', 'Penguins'),
    (2, 'CAR', 'Carolina', 'Hurricanes'),
    (2, 'CBJ', 'Columbus', 'Blue Jackets'),
    (2, 'NYI', 'New York', 'Islanders'),
    (2, 'NYR', 'New York', 'Rangers'),
    (2, 'NJD', 'New Jersey', 'Devils'),
    (2, 'STL', 'St. Louis', 'Blues'),
    (2, 'COL', 'Colorado', 'Avalanche'),
    (2, 'DAL', 'Dallas', 'Stars'),
    (2, 'WPG', 'Winnipeg', 'Jets'),
    (2, 'NSH', 'Nashville', 'Predators'),
    (2, 'MIN', 'Minnesota', 'Wild'),
    (2, 'CHI', 'Chicago', 'Blackhawks'),
    (2, 'VEG', 'Vegas', 'Golden Knights'),
    (2, 'EDM', 'Edmonton', 'Oilers'),
    (2, 'CGY', 'Calgary', 'Flames'),
    (2, 'VAN', 'Vancouver', 'Canucks'),
    (2, 'ARI', 'Arizona', 'Coyotes'),
    (2, 'ANA', 'Anaheim', 'Ducks'),
    (2, 'LAK', 'Los Angeles', 'Kings'),
    (2, 'SJS', 'San Jose', 'Sharks')
;

SELECT 
    team.id,
    team.team_abbr,
    team.team_location,
    team.team_name,
    league.league_abbr 
FROM tblTeam team
INNER JOIN tblLeague league
    ON team.league_id = league.id
;