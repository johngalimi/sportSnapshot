import flask
import pprint

import database as db


def get_games(collection_name, database_name, selected_year, selected_month, selected_day):

	games_client, games_database = db.connect_mongo(collection_name, database_name)

	games = games_database.find(
		
		{
			'game_year': selected_year,
			'game_month': selected_month,
			'game_day': selected_day,
		},

		{
			'is_playoff': 1,
			'league': 1,
			'team': 1,
			'opponent': 1,
			'team_pts': 1,
			'oppt_pts': 1,
			'_id': 0,
		}

		)

	db.close_mongo(games_client)

	game_array = [game for game in games]

	print(game_array)


get_games('sportSnapshot', 'games', 1999, 10, 2)