import pandas as pd

from base_crawler import BaseCrawler
from typing import List, Dict

SEASON_TYPES = [
    {"table_id": "stats_basic_plus_nhl", "is_postseason": False},
    # {"table_id": "stats_basic_plus_nhl_po", "is_postseason": True},
]


class PlayerCrawler(BaseCrawler):
    def crawl(self, player_code):

        url = f"https://www.hockey-reference.com/players/{player_code}.html"

        blob = self.get_html(url)
        text = self.get_response_text(blob)
        soup = self.get_soup(text)

        # helpful to grab name, position and other player metadata while we're here

        player_season_data: List[Dict[str, str]] = []

        for season_type in SEASON_TYPES:

            season_table = soup.find("table", {"id": season_type["table_id"]})

            season_records = season_table.find_all("tr")

            for season_record in season_records:
                season_year = season_record.find("th", {"data-stat": "season"})

                if season_year is not None:
                    season_year_value = season_year.text

                    if season_year_value[0].isdigit():

                        season_data_points = {
                            season_data_point.attrs["data-stat"]: season_data_point.text
                            for season_data_point in season_record.findChildren(
                                name="td"
                            )
                        }

                        season_data_points.update(
                            {
                                "season": season_year_value,
                                "is_postseason": season_type["is_postseason"],
                                "player_code": player_code,
                            }
                        )

                        player_season_data.append(season_data_points)

        return player_season_data


if __name__ == "__main__":

    pd.set_option("display.max_columns", 999)

    # this only works for skaters, not goalies right now
    PLAYER_CODES: Dict[str, str] = {
        "patrice_bergeron": "b/bergepa01",
        "alex_ovechkin": "o/ovechal01",
        "patrick_kane": "k/kanepa01",
        "drew_doughty": "d/doughdr01",
    }

    player_crawler = PlayerCrawler()

    all_players: List[Dict] = []

    for player_name, player_code in PLAYER_CODES.items():
        print("******************", player_name)
        player_result = player_crawler.crawl(player_code)

        all_players.extend(player_result)

    player_df = pd.DataFrame(all_players)

    print(player_df.tail())