import React from 'react';

export class SPGameList extends React.Component {
    constructor(props) {
        super(props);
        this.renderGames = this.renderGames.bind(this);
    }

    renderGames(games) {
        if (games.length > 0) {
            return (games.map((game) => {
                <p>game['team']</p>
            }))
        } else {
            return <p>NO GAMES</p>
        }
    }

    render() {

        const games = this.renderGames(this.props.game_list)

        return (
            <div>
                { games }
            </div>
        )
    }

}