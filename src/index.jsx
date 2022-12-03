//import React from "react";
//import ReactDOM from "react-dom/client";
//// import './styles/index.css';
//import MainPage from "./client/MainPage";
//import test from "./client/test";
//
//// const root = ReactDOM.render(<MainPage />, document.getElementById("root"));
//const root = ReactDOM.createRoot(document.getElementById("root"));
//root.render(<test />);

import React, { Component } from 'react';
import { render } from 'react-dom';
import MyMap from './client/test';
import './style.css';

class App extends Component {
    constructor(props) {
        super(props);
    }

    mapIsReadyCallback(map) {
        console.log(map);
    }

    render() {
        return <MyMap mapIsReadyCallback={this.mapIsReadyCallback} />;
    }
}

render(<App />, document.getElementById('root'));