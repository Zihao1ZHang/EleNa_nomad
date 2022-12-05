import React from 'react';

class SideBar extends React.Component {
    render(){
        return(
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
                    <span>Search!</span>
                </button>
            </div>
        );
    }
}

export default SideBar;