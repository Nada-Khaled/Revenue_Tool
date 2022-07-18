import React from "react";
import ReactDOM from "react-dom";
import reportWebVitals from "./reportWebVitals";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Home } from "./components/Home";
import LoadingIndicator from "./components/LoadingIndicator";
import { RevenueChartsForAllSites } from "./components/RevenueChartsForAllSites";
import { RevenueChartsPerSite } from "./components/RevenueChartsPerSite";
import { RevenueChartsPerNetwork } from "./components/RevenueChartsPerNetwork";
import NavBar from "./components/NavBar";

import "bootstrap/dist/css/bootstrap.min.css";
import "./index.css";

ReactDOM.render(
  <React.Fragment>
    <Router>
      {/* this NavBar component should be written inside the <BrowserRouter>
      tag because it contains the <Link> tags which cannot be written outside
      the BrowserRouter tag */}
      <div className="container">
        <NavBar />
      </div>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/RevenueChartsPerSite"
          // path="/revenueChartsPerSite"
          element={<RevenueChartsPerSite />}
        />
        <Route
          path="/RevenueChartsPerNetwork"
          // path="/revenueChartsPerNetwork"
          element={<RevenueChartsPerNetwork />}
        />

        {/* inline Jsx Routing, no need to pass a component */}
        {/* <Route
          path="/test"
          element={
            <div>
              <h2>Test</h2>
              <p>test</p>
            </div>
          }
        /> */}
      </Routes>
      <LoadingIndicator />
    </Router>
  </React.Fragment>,

  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
