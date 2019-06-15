import pandas as pd
import numpy as np
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

	new_data = []
	for record in data:
		item = record.find_all(text = True)

		if len(item) == 0: value = np.nan
		else: value = item[0]

		new_data.append(value)

	return new_data


def crawl_single_season(url, target_fields, table_ids, data_attr):

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


def generate_team_df(league_abbr, team_abbr, target_fields, target_seasons, table_ids, data_attr):

	if league_abbr == 'NHL': 
		sitename = 'hockey'
	elif league_abbr == 'NBA':
		sitename = 'basketball'

	team_df = pd.DataFrame()

	for target_season in target_seasons:
		print(f'    {target_season}')

		input_url = f'https://www.{sitename}-reference.com/teams/{team_abbr}/{target_season}_games.html'

		season_df = crawl_single_season(input_url, target_fields, table_ids, data_attr)
		team_df = pd.concat([team_df, season_df])

	team_df['team_name'] = team_abbr

	return team_df


def generate_league_df(league_abbr, target_teams, target_fields, target_seasons, table_ids, data_attr):

	league_df = pd.DataFrame()

	for target_team in target_teams:
		print(f'Crawling {target_team}')

		team_df = generate_team_df(league_abbr, target_team, target_fields, target_seasons, table_ids, data_attr)
		league_df = pd.concat([league_df, team_df])

	league_df['league_name'] = league_abbr

	return league_df
