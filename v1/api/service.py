from flask import Flask, request, jsonify
from flask_cors import CORS

import database as db

app = Flask(__name__)
CORS(app)


def get_games(collection_name, database_name, date_dict):

	games_client, games_database = db.connect_mongo(collection_name, database_name)

	games = games_database.find(

			{
				'game_year': date_dict['year'],
				'game_month': date_dict['month'],
				'game_day': date_dict['day'],
			},

			{
				'is_playoff': 1,
				'league': 1,
				'team': 1,
				'opponent': 1,
				'team_pts': 1,
				'oppt_pts': 1,
				'game_id': 1,
				'_id': 0,
			}

		)

	db.close_mongo(games_client)

	game_array, seen_games = [], []

	for game in games:

		if game['game_id'] not in seen_games:
			seen_games.append(game['game_id'])

			game_element = {

				'league': game['league'],
				'team': game['team'],
				'opponent': game['opponent'],
				'team_pts': game['team_pts'],
				'oppt_pts': game['oppt_pts'],
				'is_playoff': game['is_playoff'],

			}

			game_array.append(game_element)

	return game_array


@app.route('/games/', methods = ['GET'])
def retrieve_games():

	selected_date = request.args.to_dict()

	formatted_date = {k: int(v) for k, v in selected_date.items()}

	selected_games = get_games('sportSnapshot', 'games', formatted_date)

	return jsonify(selected_games)


if __name__ == '__main__':

	app.run(debug = True)