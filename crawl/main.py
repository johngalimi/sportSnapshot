import datetime
import pandas as pd

import database as db
import crawler as cr

pd.set_option('display.max_columns', 20)


def main():

	mongo_collection = 'sportSnapshot'
	mongo_database = 'games'

	reference_file = 'settings/reference.csv'

	table_ids = {'regular': 'all_games', 'playoff': 'all_games_playoffs'}
	table_ids = {0: 'all_games', 1: 'all_games_playoffs'}
	data_attr = 'data-stat'

	final_columns = {

		'date_game': 'game_date'
		,'league_name': 'league'
		,'game_type': 'is_playoff'
		,'team_name': 'team'
		,'opp_name': 'opponent'
		,'goals': 'team_pts'
		,'opp_goals': 'oppt_pts'
		,'pts': 'team_pts'
		,'opp_pts': 'oppt_pts' 

		}

	reordered_columns = ['game_year', 'game_month', 'game_day', 'is_playoff', 'league', 'team', 'opponent', 'team_pts', 'oppt_pts']
	
	base_season = 2000
	season_range = list(range(base_season, datetime.datetime.now().year + 1))

	my_client, my_database = db.connect_mongo(mongo_collection, mongo_database)
	
	db.clear_out_db(my_database)

	db.close_mongo(my_client)

	reference_df = pd.read_csv(reference_file)

	leagues = reference_df['league'].unique()

	for league in leagues:

		desired_fields = ['date_game', 'opp_name']

		if league == 'NHL': 
			desired_fields += ['goals', 'opp_goals']

			# excluding 2005 season b/c of NHL lockout
			desired_seasons = [season for season in season_range if season != 2005]

		elif league == 'NBA':
			desired_fields += ['pts', 'opp_pts']
			desired_seasons = season_range

		team_list = (reference_df[reference_df['league'] == league])['team'].to_list()

		df = cr.generate_league_df(league, team_list, desired_fields, desired_seasons, table_ids, data_attr)

		name_mapping = reference_df[reference_df['league'] == league][['team', 'full_name']]

		prepared_data = cr.prepare_league_data(df, league, final_columns, reordered_columns, name_mapping)

		my_client, my_database = db.connect_mongo(mongo_collection, mongo_database)
	
		db.insert_into_db(my_database, prepared_data)

		db.close_mongo(my_client)


if __name__ == '__main__':
	
	main()