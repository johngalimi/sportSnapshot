import React from 'react';
import '.\\App.css'

import { SPDateSelect } from '.\\components\\SPDateSelect';
import { SPAppHeader } from '.\\components\\SPAppHeader';

import '..\\node_modules\\antd\\dist\\antd.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loaded: true,
      game_data: [],
    }
    this.retrieveData = this.retrieveData.bind(this);
    this.handleDateToggle = this.handleDateToggle.bind(this);
  }

  retrieveData = (selected_year, selected_month, selected_day) => {

    // verify that this loading bool is working
    this.setState({loaded: false})

    fetch('http://127.0.0.1:5000/games/?year=' + selected_year +'&month=' + selected_month + '&day=' + selected_day)
    .then(res => res.json())
    .then((data) => {
      this.setState({
        game_data: data,
      })
    })

    this.setState({loaded: true})
  }

  handleDateToggle = (date, dateString) => {

    var selected_date_arr = dateString.split('-');

    if (selected_date_arr.length > 1) {
      var date_int_arr = selected_date_arr.map(Number)
      this.retrieveData(date_int_arr[0], date_int_arr[1], date_int_arr[2])      
    }
  }

  render() {

    return (

      <div 
        // style = {{paddingTop: '100px'}}
        className = 'main_app'
      >
        <SPAppHeader />
        <br />
        <SPDateSelect 
          changeHandler = {this.handleDateToggle}
        />
      </div>

    )
  }

}

export default App;
