import PropTypes from "prop-types";
import React, { Component } from "react";
import * as qs from 'qs';
// const qs = require("qs");

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
        {/* <form>
          <label>First name:</label><br/>
          <input type="text" id="fname" name="fname"/><br/>
          <label>Last name:</label><br/>
          <input type="text" id="lname" name="lname"/>
          <button
            onClick={() => {
              this.sendRequest();
            }}
          >
            <span>Search!</span>
          </button>
        </form> */}
        
        <text id="source">85 Cowls Road, Amherst, MA</text>
        <br />
        <text id="destination">133 Belchertown Road, Amherst, MA</text>
        <br />
        <text id="min_max">max</text>
        <br />
        <text id="percentage">10.2</text>
        <br />
        <button
          onClick={() => {
            this.sendRequest();
          }}
        >
          <span>Search!</span>
        </button>
        
      </div>
    );
  }

  sendRequest() {
    // const src = document.getElementById("fname").value;
    // const dest = document.getElementById("fname").value;
    // const min_max = document.getElementById("lname").value;
    // const percentage = document.getElementById("lname").value;
    let src = "85 Cowls Road, Amherst, MA";
    let dest = "133 Belchertown Road, Amherst, MA";
    let min_max = "max";
    let percentage = "10.23";
    console.log("sending request to server...");
    console.log(src);
    console.log(dest);
    console.log(min_max);
    fetch("http://localhost:8080/get_route", {
      method: "POST",
      // mode: "no-cors",
      headers: {
        Accept: 'application/json, text/plain, */*',
        'Content-Type': 'application/json; charset=utf-8',
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({
        "Source": src,
        "Destination": dest,
        "Min_max": min_max,
        "Percentage": percentage,
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
      });
  }
}

export default MainPage;
