import React from 'react';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
    }
  }

  componentDidMount() {
    console.log('Mounted!')
  }

  render() {
    return (
      <div>Testing</div>
    )
  }

}

export default App;
