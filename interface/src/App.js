import React from 'react';
import '.\\App.css'

import { SPDateSelect } from '.\\components\\SPDateSelect';
import { SPAppHeader } from '.\\components\\SPAppHeader';

import '..\\node_modules\\antd\\dist\\antd.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      game_toggle: false,
      game_data: [],
    }
    this.retrieveData = this.retrieveData.bind(this);
    this.handleDateToggle = this.handleDateToggle.bind(this);
    this.toggleGames = this.toggleGames.bind(this);
  }

  retrieveData = (selected_year, selected_month, selected_day) => {

    fetch('http://127.0.0.1:5000/games/?year=' + selected_year +'&month=' + selected_month + '&day=' + selected_day)
    .then(res => res.json())
    .then((data) => {
      this.setState({
        game_data: data,
      })
    })

  }

  handleDateToggle = (date, dateString) => {

    var selected_date_arr = dateString.split('-');

    if (selected_date_arr.length > 1) {
      var date_int_arr = selected_date_arr.map(Number)
      this.retrieveData(date_int_arr[0], date_int_arr[1], date_int_arr[2])      
    }
  }

  toggleGames = () => {
    this.setState({
      game_toggle: !this.state.game_toggle
    })
  }

  render() {

    const isToggled = this.state.game_toggle;

    return (

      <div
        className = 'main_app'
      >

        {!isToggled ? (
          
          <div>

            <SPAppHeader />

            <br />

            <SPDateSelect 
              changeHandler = {this.handleDateToggle}
            />

            <br />

            <button
              onClick = {this.toggleGames}
              style = {{color: 'black', padding: '5px'}}
            >
              Find Games
            </button>

          </div>

        ) : (

          <div>

            <p>toggled</p>

            <br />

            <button
              onClick = {this.toggleGames}
              style = {{color: 'black', padding: '5px'}}
            >
              Go Home
            </button>

          </div>

        )}

      </div>

    )
  }

}

export default App;
