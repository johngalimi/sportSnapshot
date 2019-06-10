import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup


def generate_soup(target_url):

	page = requests.get(target_url)
	good_url = True

	if page.status_code != 404:
		soup = BeautifulSoup(page.content, 'html.parser')

	else:
		soup = None
		good_url = False

	return soup, good_url


def locate_table_div(soup, table_id):

	table = soup.find('div', {'id': table_id})

	return table


def extract_from_td(table_name, attr_name, field_name):

	data = table_name.find_all('td', attrs = {attr_name: field_name})
	data = [i.find_all(text = True)[0] for i in data]

	return data


def crawl_single_season(urls, target_fields):

	season_soup, url_status = generate_soup(url)

	if url_status:
		season_df = pd.DataFrame()

		for game_type, table_id in table_ids.items():
			table = locate_table_div(season_soup, table_id)

			# checking for playoff sub table
			if table is not None:
				df = pd.DataFrame()

				for target_field in target_fields:
					data = extract_from_td(table, data_attr, target_field)
					df[target_field] = data

				df['game_type'] = game_type
				season_df = pd.concat([season_df, df])

		return season_df


def generate_team_df(team_abbr, target_fields, target_seasons):

	team_df = pd.DataFrame()

	for target_season in target_seasons:
		print(f'    {target_season}')

		input_url = f'https://www.hockey-reference.com/teams/{team_abbr}/{target_season}_games.html'

		season_df = crawl_single_season(input_url, target_fields)
		team_df = pd.concat([team_df, season_df])

	team_df['team_name'] = team_abbr

	return team_df


def generate_league_df(league_abbr, target_teams, target_fields, target_seasons):

	league_df = pd.DataFrame()

	for target_team in target_teams:
		print(f'Crawling {target_team}')

		team_df = generate_team_df(target_team, target_fields, target_seasons)
		league_df = pd.concat([league_df, team_df])

	league_df['league_name'] = league_abbr

	return league_df


if __name__ == '__main__':

	reference_file = 'settings/reference.csv'
	base_season = 2000

	table_ids = {
	
		'regular': 'all_games'
		,'playoff': 'all_games_playoffs'

	}

	data_attr = 'data-stat'

	desired_fields = [

		'date_game'
		,'opp_name'
		,'goals'
		,'opp_goals'

		]

	reference_df = pd.read_csv(reference_file)
	
	league_name = reference_df['league'].iloc[0] 
	team_list = reference_df['team'].to_list()

	# filter out '04 lockout season and current season (until season complete)
	season_range = list(range(base_season, datetime.datetime.now().year + 1))
	season_range = [season for season in season_range if season not in [2005, 2019]]

	team_list = ['BOS', 'WSH', 'TBL']

	df = generate_league_df(league_name, team_list, desired_fields, season_range)

	print(df.head())
	print(df.info())

	

