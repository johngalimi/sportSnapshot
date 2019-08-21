from flask import Flask, request, jsonify

import database as db

app = Flask(__name__)


def get_games(collection_name, database_name, date_dict):

	# need to address duplicate game records (NJD vs NYR 5/25/12)

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
				'_id': 0,
			}

		)

	db.close_mongo(games_client)

	game_array = [game for game in games]

	return game_array


@app.route('/games/', methods = ['GET'])
def retrieve_games():

	selected_date = request.args.to_dict()

	formatted_date = {k: int(v) for k, v in selected_date.items()}

	selected_games = get_games('sportSnapshot', 'games', formatted_date)

	return jsonify(selected_games)


if __name__ == '__main__':

	app.run(debug = True)