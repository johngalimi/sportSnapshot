import React from 'react';

export class SPGameList extends React.Component {
    constructor(props) {
        super(props);
        this.renderGames = this.renderGames.bind(this);
    }

    renderGames(raw_games) {
        if (raw_games.length > 0) {

            console.log(raw_games)

            var game_list = []

            for (let i = 0; i < raw_games.length; i++) {
                game_list.push(<p key={i}>{raw_games[i].team}</p>)
            }

            console.log(game_list)

            return (
                <div>{game_list}</div>
            )

            // return (games.map((game) => {
            //     <p>game['team']</p>
            // }))
        } else {
            return <p>NO GAMES</p>
        }
    }

    render() {

        const processed_games = this.renderGames(this.props.game_list)

        return (
            <div>
                { processed_games }
            </div>
        )
    }

}