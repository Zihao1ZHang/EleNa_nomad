import React from 'react';

class SideBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          selectedGoal: "Shortest Route", // Initialize selectedGoal to "Shortest Route"
        };
      }
    
      
      handleGoalChange = (event) => {
        // Update selectedGoal state whenever a new goal is selected
        this.setState({ selectedGoal: event.target.value });
      }
      render() {
        return (
          <div className="mainpage">
            <text id="source">85 Cowls Road, Amherst, MA</text>
            <text id="destination">133 Belchertown Road, Amherst, MA</text>
            <text id="min_max">max</text>
            <text id="percentage">10.2</text>
            <button onClick={this.sendRequest}>
              <span>Search!</span>
            </button>
            <fieldset>
              <legend>Goal - Please click your goal below</legend>
              <ul id="goals">
                <li>
                  <input
                    type="radio"
                    name="goal"
                    value="Shortest Route"
                    checked={this.state.selectedGoal === "Shortest Route"}
                    onChange={this.handleGoalChange}
                  />
                  Shortest Route
                </li>
                <li>
                  <input
                    type="radio"
                    name="goal"
                    value="Max Elevation"
                    checked={this.state.selectedGoal === "Max Elevation"}
                    onChange={this.handleGoalChange}
                  />
                  Max Elevation
                </li>
                <li>
                  <input
                    type="radio"
                    name="goal"
                    value="Min Elevation"
                    checked={this.state.selectedGoal === "Min Elevation"}
                    onChange={this.handleGoalChange}
                  />
                  Min Elevation
                </li>
              </ul>
            </fieldset>
          </div>
        );
      }
      
}


export default SideBar;