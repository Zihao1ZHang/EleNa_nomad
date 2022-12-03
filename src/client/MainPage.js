import PropTypes from "prop-types";
import React, { Component } from "react";

class MainPage extends Component {
  static propTypes = {};
  constructor(props) {
    super(props);
    this.state = {
      renderRoute: false,
    };
  }

  render() {
    const { classes } = this.props;

    return (
      <div className="mainpage">
        <text id="source">85 Cowls Road, Amherst, MA</text>
        <text id="destination">133 Belchertown Road, Amherst, MA</text>
        <text id="min_max">max</text>
        <text id="percentage">10.2</text>
        <button
          onClick={() => {
            this.sendRequest();
          }}
        >
          <span className={classes.goText}>Search!</span>
        </button>
      </div>
    );
  }

  sendRequest() {
    const src = document.getElementById("source").value;
    const dest = document.getElementById("destination").value;
    const min_max = document.getElementById("min_max").value;
    const percentage = document.getElementsById("percentage").value;
    fetch("http://localhost:8080/get_route", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({
        source: src,
        destination: dest,
        Min_max: min_max,
        Percentage: percentage,
      }),
    })
      .then((res) => res.json())
      .then((json) => {
        this.setState({
          route: json["Route"],
          renderRoute: true,
          distance: json["Distance"],
          elevation: json["Elevation Gain"],
        });
        console.log(json["Route"]);
        console.log(json["Distance"]);
        console.log(json["Elevation Gain"]);
      });
  }
}

export default MainPage;
