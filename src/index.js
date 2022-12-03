import React from "react";
import ReactDOM from "react-dom/client";
// import './styles/index.css';
import MainPage from "./MainPage";

class Game extends React.Component {
  render() {
    return (
      <div className="game">
        <div className="game-board"></div>
        <div className="game-info">
          <div>asdad</div>
          <div>{/*TODO*/}</div>
        </div>
      </div>
    );
  }
}

// const root = ReactDOM.render(<MainPage />, document.getElementById("root"));
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<MainPage />);
