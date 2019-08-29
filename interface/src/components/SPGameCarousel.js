import React from 'react';
import { Carousel } from 'antd';

import '.\\styling\\SPGameCarousel.css';

export class SPGameCarousel extends React.Component {
    constructor(props) {
        super(props);
        this.renderGames = this.renderGames.bind(this);
    }

    renderGames(raw_games) {

        var game_list = [];

        if (raw_games.length > 0) {

            for (let i = 0; i < raw_games.length; i++) {

                var g = raw_games[i]

                if (g['team_pts'] > g['oppt_pts']) {
                    var [winner, loser, win_pts, lose_pts] = [g['team'], g['opponent'], g['team_pts'], g['oppt_pts']]
                } else {
                    var [winner, loser, win_pts, lose_pts] = [g['opponent'], g['team'], g['oppt_pts'], g['team_pts']]
                }

                var game_type = g['is_playoff'] ? 'Playoffs' : 'Regular Season'

                game_list.push(

                    {
                        'league': g['league'],
                        'type': game_type,
                        'winner': winner,
                        'loser': loser,
                        'win_pts': win_pts,
                        'lose_pts': lose_pts,
                    }
                )
            }

        } 

        return game_list
    }

    render() {

        const processed_games = this.renderGames(this.props.game_list)

        return (

            <Carousel>

                {processed_games.map((g, idx) => {

                    return (
                        <div key = {idx}>
                            <h3>{g.league}</h3>
                        </div>
                    )
                    
                })}

            </Carousel>
        )
    }

}