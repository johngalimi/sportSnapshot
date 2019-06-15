import datetime
import pandas as pd
from crawler import generate_league_df

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 20)


def main():

	reference_file = 'settings/reference.csv'

	table_ids = {'regular': 'all_games', 'playoff': 'all_games_playoffs'}
	data_attr = 'data-stat'

	final_columns = {

		'date_game': 'game_date'
		,'team_name': 'team'
		,'opp_name': 'opponent'
		,'league_name': 'league'
		,'game_type': 'type'
		,'goals': 'team_pts'
		,'opp_goals': 'oppt_pts'
		,'pts': 'team_pts'
		,'opp_pts': 'oppt_pts' 

		}

	reordered_columns = ['league', 'game_date', 'type', 'team', 'opponent', 'team_pts', 'oppt_pts']
	
	base_season = 2000
	season_range = list(range(base_season, datetime.datetime.now().year + 1))

	reference_df = pd.read_csv(reference_file)

	leagues = reference_df['league'].unique()

	for league in leagues:

		desired_fields = ['date_game', 'opp_name']

		if league == 'NHL': 
			desired_fields += ['goals', 'opp_goals']
			season_range = [season for season in season_range if season != 2005]

		elif league == 'NBA':
			desired_fields += ['pts', 'opp_pts']

		team_list = (reference_df[reference_df['league'] == league])['team'].to_list()
		team_list = team_list[0:1]

		# TODO - standardize column names

		df = generate_league_df(league, team_list, desired_fields, season_range, table_ids, data_attr)

		df.rename(columns = final_columns, inplace = True)
		print(df.head())
		df = df[reordered_columns]

		print(df.head())
		print(df.info())

		df.to_csv(f'testing/{league}.csv', index=False)


if __name__ == '__main__':
	main()