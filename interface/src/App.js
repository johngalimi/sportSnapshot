import React from 'react';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loaded: false,
      game_data: [],
    }
    this.retrieveData = this.retrieveData.bind(this);
  }

  componentDidMount() {
    console.log('Mounted!')
  }

  retrieveData = () => {
    fetch('http://127.0.0.1:5000/games/?year=2018&month=12&day=25')
    .then(res => res.json())
    .then((data) => {
      console.log(data)
      this.setState({
        game_data: data,
      })
    })
  }

  render() {
    return (
      <div>
        <button onClick={this.retrieveData}>
          Fetch Data
        </button>
      </div>
    )
  }

}

export default App;
