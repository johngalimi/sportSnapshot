import React from "react";

import ".\\styling\\SPGameList.css";

export class SPGameList extends React.Component {
  constructor(props) {
    super(props);
    this.renderGames = this.renderGames.bind(this);
  }

  renderGames(raw_games) {
    if (raw_games.length > 0) {
      var game_list = [];

      for (let i = 0; i < raw_games.length; i++) {
        var g = raw_games[i];

        if (g["team_pts"] > g["oppt_pts"]) {
          var [winner, loser, win_pts, lose_pts] = [
            g["team"],
            g["opponent"],
            g["team_pts"],
            g["oppt_pts"],
          ];
        } else {
          var [winner, loser, win_pts, lose_pts] = [
            g["opponent"],
            g["team"],
            g["oppt_pts"],
            g["team_pts"],
          ];
        }

        var game_type = g["is_playoff"] ? "Playoffs" : "Regular Season";

        var game_string =
          g["league"] +
          " " +
          game_type +
          ": " +
          winner +
          " defeated " +
          loser +
          " " +
          win_pts +
          " to " +
          lose_pts;

        game_list.push(<p key={i}>{game_string}</p>);
      }

      return <div>{game_list}</div>;
    } else {
      return <p>No Games</p>;
    }
  }

  render() {
    const processed_games = this.renderGames(this.props.game_list);

    return <div className="game_list">{processed_games}</div>;
  }
}
