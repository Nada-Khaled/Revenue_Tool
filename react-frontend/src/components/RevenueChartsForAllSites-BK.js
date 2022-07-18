import React, { useEffect, useState } from "react";
import { trackPromise } from "react-promise-tracker";
import Dropdown from "react-dropdown";
import { PureComponent } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts";

import "react-dropdown/style.css";
import axios from "axios";
import "../config";

import "./revenueChart.css";
import { ContactlessOutlined } from "@mui/icons-material";
import { color } from "@mui/system";

export const RevenueChartsForAllSites = () => {
  const [sitesRevenue, setSitesRevenue] = useState({});
  const [siteCodesList, setSiteCodesList] = useState([]);
  const [siteCodeInfo, setSiteCodeInfo] = useState([]); // each site code has a list of objects to be passed to the chart
  const [areSiteCodesAvailable, setAreSiteCodesAvailable] = useState(false);
  const [isSiteCodeChosen, setIsSiteCodeChosen] = useState(false);
  const [buttonText, setButtonText] = useState("Show Roaming Revenue");
  const [showRoamingData, setShowRoamingData] = useState(false);

  const HandleSelectSiteCode = (evt) => {
    var selectedSiteCode = evt.target.value;
    var siteCodeInfo = sitesRevenue[selectedSiteCode]; // list of objects
    setSiteCodeInfo(siteCodeInfo);
    setIsSiteCodeChosen(true);
  };

  useEffect(() => {
    trackPromise(
      axios
        .get(global.config.BACKEND_IP + "/api/showCharts")
        .then((response) => {
          console.log(response.data);
          console.log(Object.keys(response.data));

          setSitesRevenue(response.data);
          setSiteCodesList(Object.keys(response.data));
          setAreSiteCodesAvailable(true);
        })
    );
  }, []);

  function ShowSiteChart(dataAvailable) {
    if (!dataAvailable) return null;
    console.log("data to be drawn:");
    console.log(siteCodeInfo);
    return (
      <React.Fragment>
        <ResponsiveContainer width="100%" height={600}>
          <LineChart data={siteCodeInfo}>
            <Line strokeWidth={3} stroke="#8884d8" dataKey="Total Revenue" />
            <Line strokeWidth={3} stroke="#82ca9d" dataKey="Total Data" />
            <Line strokeWidth={3} stroke="#ff0000" dataKey="Total Voice" />
            {showRoamingData && (
              <React.Fragment>
                <Line
                  strokeWidth={3}
                  stroke="#0000FF"
                  dataKey="Roaming Voice"
                />
                <Line strokeWidth={3} stroke="#000000" dataKey="Roaming Data" />
              </React.Fragment>
            )}
            <XAxis dataKey="Date" />
            <YAxis
              dataKey="Total Revenue"
              //   tickFormatter={(number) => `$${number.toFixed(2)}`}
            />
            <Tooltip />
            <CartesianGrid strokeDasharray="3 3" />
            <Legend />
            {/* <Line type="monotone" dataKey="uv" stroke="#82ca9d" /> */}
          </LineChart>
        </ResponsiveContainer>
        <button
          onClick={() => {
            if (buttonText === "Show Roaming Revenue")
              setButtonText("Hide Roaming Revenue");
            else setButtonText("Show Roaming Revenue");

            setShowRoamingData(!showRoamingData);
          }}
        >
          {buttonText}
        </button>
      </React.Fragment>
    );
  }

  function ShowSitesList(dataAvailable) {
    if (!dataAvailable) return null;
    else {
      return (
        <React.Fragment>
          <label style={{ marginBottom: 20 }}> Choose a site code:</label>
          <select
            placeholder="Select Site"
            className="form-select mb-4"
            onChange={HandleSelectSiteCode}
          >
            {siteCodesList.map((siteCode) => {
              return (
                <option value={siteCode} key={siteCode}>
                  {siteCode}
                </option>
              );
            })}
          </select>

          {ShowSiteChart(isSiteCodeChosen)}
        </React.Fragment>
      );
    }
  }

  return (
    <div className="container mt-5">
      <h1 style={{ textAlign: "center", color: "#f76300", marginBottom: 40 }}>
        {" "}
        Sites Charts
      </h1>

      {ShowSitesList(areSiteCodesAvailable)}
    </div>
  );
};
