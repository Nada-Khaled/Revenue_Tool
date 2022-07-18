import React, { useEffect, useState } from "react";
import { trackPromise } from "react-promise-tracker";
import Grid from "@material-ui/core/Grid";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

import "react-dropdown/style.css";
import axios from "axios";

import "./revenueChart.css";
import "../config";

export const RevenueChartsPerSite = () => {
  const [siteCodesList, setSiteCodesList] = useState([]);
  const [siteCodeInfo, setSiteCodeInfo] = useState([]); // each site code has a list of objects to be passed to the chart
  const [areSiteCodesAvailable, setAreSiteCodesAvailable] = useState(false);
  // const [isSiteCodeChosen, setIsSiteCodeChosen] = useState(false);
  const [siteCodeAndTechnologyChosen, setSiteCodeAndTechnologyChosen] =
    useState(0);
  const [areSiteCodeAndTechnologyChosen, setAreSiteCodeAndTechnologyChosen] =
    useState(false);
  const [showRoamingData, setShowRoamingData] = useState(false);
  // Either make 3 different boolean variables for each filter or:
  // make a dictionary, and the keys are the values of the <option> tags
  const [showTotalRevenue, setShowTotalRevenue] = useState(true);
  const [showDataRevenue, setShowDataRevenue] = useState(true);
  const [showVoiceRevenue, setShowVoiceRevenue] = useState(true);
  const [showInBoundRoamDuration, setShowInBoundRoamDuration] = useState(true);
  const [showTotalMB, setShowTotalMB] = useState(true);
  const [showNationalRoamDuration, setShowNationalRoamDuration] =
    useState(true);
  const [showOutInternationalEGP, setShowOutInternationalEGP] = useState(true);
  const [showRoamDataMB, setShowRoamDataMB] = useState(true);

  const [buttonText, setButtonText] = useState("Show Roaming Revenue");

  const HandleSelectTechnologyAndSiteCode = (evt) => {
    setSiteCodeAndTechnologyChosen(siteCodeAndTechnologyChosen + 1);
  };

  const HandleSelectSiteCode = (evt) => {
    var selectedSiteCode = evt.target.value;

    axios
      .get(
        global.config.BACKEND_IP + "/api/showChartBySite/" + selectedSiteCode
      )
      .then((response) => {
        console.log(response.data);
        console.log(Object.keys(response.data));

        // setSitesRevenue(response.data);
        setSiteCodeInfo(response.data[selectedSiteCode]);
      });

    console.log("siteCode data:");
    console.log(siteCodeInfo);
    setSiteCodeAndTechnologyChosen(true);
  };

  const HandleFilterBy = (evt) => {
    var filterBy = evt.target.value;

    console.log("filterBy");
    console.log(filterBy);

    if (filterBy === "") {
      setShowTotalRevenue(true);
      setShowVoiceRevenue(true);
      setShowDataRevenue(true);
      setShowInBoundRoamDuration(true);
      setShowNationalRoamDuration(true);
      setShowTotalMB(true);
      setShowOutInternationalEGP(true);
      setShowRoamDataMB(true);
    }
    if (filterBy === "Data Revenue") {
      setShowTotalRevenue(false);
      setShowVoiceRevenue(false);
      setShowDataRevenue(true);
      setShowInBoundRoamDuration(false);
      setShowNationalRoamDuration(false);
      setShowTotalMB(false);
      setShowOutInternationalEGP(false);
      setShowRoamDataMB(false);
    }
    if (filterBy === "Voice Revenue") {
      setShowTotalRevenue(false);
      setShowVoiceRevenue(true);
      setShowDataRevenue(false);
      setShowInBoundRoamDuration(false);
      setShowNationalRoamDuration(false);
      setShowTotalMB(false);
      setShowOutInternationalEGP(false);
      setShowRoamDataMB(false);
    }
    if (filterBy === "Total Revenue") {
      setShowTotalRevenue(true);
      setShowVoiceRevenue(false);
      setShowDataRevenue(false);
      setShowInBoundRoamDuration(false);
      setShowNationalRoamDuration(false);
      setShowTotalMB(false);
      setShowOutInternationalEGP(false);
      setShowRoamDataMB(false);
    }

    if (filterBy === "InBound Roaming Duration") {
      setShowTotalRevenue(false);
      setShowVoiceRevenue(false);
      setShowDataRevenue(false);
      setShowInBoundRoamDuration(true);
      setShowNationalRoamDuration(false);
      setShowTotalMB(false);
      setShowOutInternationalEGP(false);
      setShowRoamDataMB(false);
    }
    if (filterBy === "Total MB") {
      setShowTotalRevenue(false);
      setShowVoiceRevenue(false);
      setShowDataRevenue(false);
      setShowInBoundRoamDuration(false);
      setShowNationalRoamDuration(false);
      setShowTotalMB(true);
      setShowOutInternationalEGP(false);
      setShowRoamDataMB(false);
    }
    if (filterBy === "National Roaming Duration") {
      setShowTotalRevenue(false);
      setShowVoiceRevenue(false);
      setShowDataRevenue(false);
      setShowInBoundRoamDuration(false);
      setShowNationalRoamDuration(true);
      setShowTotalMB(false);
      setShowOutInternationalEGP(false);
      setShowRoamDataMB(false);
    }
    if (filterBy === "Out International EGP") {
      setShowTotalRevenue(false);
      setShowVoiceRevenue(false);
      setShowDataRevenue(false);
      setShowInBoundRoamDuration(false);
      setShowNationalRoamDuration(false);
      setShowTotalMB(false);
      setShowOutInternationalEGP(true);
      setShowRoamDataMB(false);
    }
    if (filterBy === "Roam Data MB") {
      setShowTotalRevenue(false);
      setShowVoiceRevenue(false);
      setShowDataRevenue(false);
      setShowInBoundRoamDuration(false);
      setShowNationalRoamDuration(false);
      setShowTotalMB(false);
      setShowOutInternationalEGP(false);
      setShowRoamDataMB(true);
    }
  };

  useEffect(() => {
    // used to stop updating the state if I navigated to another component
    // to avoid a warning, by stopping the fetch operation
    // it is used in fetch functions
    const abortController = new AbortController();

    trackPromise(
      axios
        .get(global.config.BACKEND_IP + "/api/getAllSiteCodes", {
          signal: abortController.signal,
        })
        .then((response) => {
          console.log(response.data);
          console.log(Object.keys(response.data));

          setSiteCodesList(response.data["SiteCodes"]);
          console.log("site codes:");
          console.log(siteCodesList);
          setAreSiteCodesAvailable(true);
        })
    );

    // Clean up function to stop updating the state if I navigated
    // to another component to avoid a warning
    return () => abortController.abort();
  }, []);

  // Not used
  function ShowSiteChart(siteCodeChosen) {
    if (!siteCodeChosen) return null;
    console.log("data to be drawn:");
    console.log(siteCodeInfo);
    return (
      <React.Fragment>
        <ResponsiveContainer width="100%" height={600}>
          <LineChart
            data={siteCodeInfo.map((item) => ({
              ...item,
              //   Revenue: parseFloat(item.Revenue),
              Total_Revenue: Number(item.Total_Revenue),
              Total_Data: Number(item.Total_Data),
              Total_Voice: Number(item.Total_Voice),
              Roaming_Voice: Number(item.Roaming_Voice),
              Roaming_Data: Number(item.Roaming_Data),
              In_Bound_Roam_Duration: Number(item.In_Bound_Roam_Duration),
              Total_MB: Number(item.Total_MB),
              National_Roam_Duration: Number(item.National_Roam_Duration),
              Out_International_EGP: Number(item.Out_International_EGP),
              Roam_Data_MB: Number(item.Roam_Data_MB),
            }))}
          >
            {showTotalRevenue && (
              <Line strokeWidth={3} stroke="#8884d8" dataKey="Total_Revenue" />
            )}
            {showDataRevenue && (
              <Line strokeWidth={3} stroke="#82ca9d" dataKey="Total_Data" />
            )}
            {showVoiceRevenue && (
              <Line strokeWidth={3} stroke="#ff0000" dataKey="Total_Voice" />
            )}
            {showRoamingData && (
              <React.Fragment>
                <Line
                  strokeWidth={3}
                  stroke="#FF00FF"
                  dataKey="Roaming_Voice"
                />
                <Line strokeWidth={3} stroke="#000000" dataKey="Roaming_Data" />
              </React.Fragment>
            )}
            <XAxis dataKey="Date" />
            <YAxis
              dataKey="Total_Revenue"
              width={140}
              //   dataKey="Revenue"
              //   tickFormatter={(number) => `$${number.toFixed(2)}`}
            />
            <Tooltip
              formatter={(value) => new Intl.NumberFormat().format(value)}
            />
            <CartesianGrid strokeDasharray="3 3" />
            <Legend />
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

  function ShowSitesList(siteCodesAvailable) {
    if (!siteCodesAvailable) return null;
    else {
      return (
        <React.Fragment>
          <Grid container style={{ marginTop: 30 }}>
            <Grid
              item
              md={2}
              xs={2}
              style={{ marginRight: 40, paddingLeft: 50 }}
            >
              <label
                style={{ fontWeight: 500, fontSize: 26, marginBottom: 20 }}
              >
                {" "}
                Choose a Technology:
              </label>
              <select
                placeholder="Select Technology"
                className="form-select mb-4"
                onChange={HandleSelectTechnologyAndSiteCodeAndSiteCode}
              >
                <option value="" key=""></option>
                <option value="2G" key="2G">
                  2G
                </option>
                <option value="3G" key="3G">
                  3G
                </option>
                <option value="4G" key="4G">
                  4G
                </option>
              </select>
            </Grid>
            <Grid
              item
              md={2}
              xs={2}
              style={{ marginRight: 40, paddingLeft: 50 }}
            >
              <label
                style={{ fontWeight: 500, fontSize: 26, marginBottom: 20 }}
              >
                {" "}
                Choose a site code:
              </label>
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
            </Grid>

            <Grid item md={2} xs={2}>
              <label
                style={{ fontWeight: 500, fontSize: 26, marginBottom: 20 }}
              >
                {" "}
                Filter By:
              </label>
              <select
                placeholder="Select Site"
                className="form-select mb-4"
                onChange={HandleFilterBy}
              >
                <option value="" key=""></option>
                <option value="Total Revenue" key="Total Revenue">
                  Total Revenue
                </option>
                <option value="Data Revenue" key="Data Revenue">
                  Data Revenue
                </option>
                <option value="Voice Revenue" key="Voice Revenue">
                  Voice Revenue
                </option>
                <option
                  value="InBound Roaming Duration"
                  key="InBound Roaming Duration"
                >
                  InBound Roaming Duration
                </option>
                <option value="Total MB" key="Total MB">
                  Total MB
                </option>
                <option
                  value="National Roaming Duration"
                  key="National Roaming Duration"
                >
                  National Roaming Duration
                </option>
                <option
                  value="Out International EGP"
                  key="Out International EGP"
                >
                  Out International EGP
                </option>
                <option value="Roam Data MB" key="Data MB">
                  Roaming Data MB
                </option>
              </select>
            </Grid>

            <Grid item md={2} xs={2}>
              <button
                onClick={() => {
                  setShowTotalRevenue(true);
                  setShowVoiceRevenue(true);
                  setShowDataRevenue(true);
                }}
                style={{
                  marginTop: 30,
                  marginLeft: 40,
                  paddingLeft: 50,
                  paddingRight: 50,
                }}
              >
                Reset Filters
              </button>
            </Grid>

            {areSiteCodeAndTechnologyChosen && (
              <Grid item md={2} xs={2}>
                <button
                  onClick={() => {
                    if (buttonText === "Show Roaming Revenue")
                      setButtonText("Hide Roaming Revenue");
                    else setButtonText("Show Roaming Revenue");

                    setShowRoamingData(!showRoamingData);
                  }}
                  style={{
                    marginTop: 30,
                    // marginLeft: 10,
                  }}
                >
                  {buttonText}
                </button>
              </Grid>
            )}
          </Grid>

          {/* {ShowSiteChart(areSiteCodeAndTechnologyChosen)} */}

          {areSiteCodeAndTechnologyChosen && (
            <React.Fragment>
              <ResponsiveContainer width="100%" height={600}>
                <LineChart
                  data={siteCodeInfo.map((item) => ({
                    ...item,
                    //   Revenue: parseFloat(item.Revenue),
                    Total_Revenue: parseFloat(item.Total_Revenue),
                    Total_Data: parseFloat(item.Total_Data),
                    Total_Voice: parseFloat(item.Total_Voice),
                    Roaming_Voice: parseFloat(item.Roaming_Voice),
                    Roaming_Data: parseFloat(item.Roaming_Data),
                    In_Bound_Roam_Duration: Number(item.In_Bound_Roam_Duration),
                    Total_MB: Number(item.Total_MB),
                    National_Roam_Duration: Number(item.National_Roam_Duration),
                    Out_International_EGP: Number(item.Out_International_EGP),
                    Roam_Data_MB: Number(item.Roam_Data_MB),
                  }))}
                >
                  {showTotalRevenue && (
                    <Line
                      strokeWidth={3}
                      stroke="#8884d8"
                      dataKey="Total_Revenue"
                    />
                  )}

                  {showDataRevenue && (
                    <Line
                      strokeWidth={3}
                      stroke="#82ca9d"
                      dataKey="Total_Data"
                    />
                  )}
                  {showVoiceRevenue && (
                    <Line
                      strokeWidth={3}
                      stroke="#ff0000"
                      dataKey="Total_Voice"
                    />
                  )}

                  {showRoamingData && (
                    <React.Fragment>
                      <Line
                        strokeWidth={3}
                        stroke="#FF00FF"
                        dataKey="Roaming_Voice"
                      />
                      <Line
                        strokeWidth={3}
                        stroke="#000000"
                        dataKey="Roaming_Data"
                      />
                    </React.Fragment>
                  )}
                  {/* Additional Charts */}
                  {showInBoundRoamDuration && (
                    <Line
                      strokeWidth={3}
                      stroke="#a9a9a9"
                      dataKey="In_Bound_Roam_Duration"
                    />
                  )}

                  {showTotalMB && (
                    <Line strokeWidth={3} stroke="#9A6324" dataKey="Total_MB" />
                  )}

                  {showNationalRoamDuration && (
                    <Line
                      strokeWidth={3}
                      stroke="#000075"
                      dataKey="National_Roam_Duration"
                    />
                  )}

                  {showOutInternationalEGP && (
                    <Line
                      strokeWidth={3}
                      stroke="#f032e6"
                      dataKey="Out_International_EGP"
                    />
                  )}

                  {showRoamDataMB && (
                    <Line
                      strokeWidth={3}
                      stroke="#469990"
                      dataKey="Roam_Data_MB"
                    />
                  )}

                  <XAxis dataKey="Date" />
                  <YAxis
                    dataKey="Total_Revenue"
                    //   dataKey="Revenue"
                    //   tickFormatter={(number) => `$${number.toFixed(2)}`}
                  />
                  <Tooltip
                    formatter={(value) =>
                      new Intl.NumberFormat("en").format(value)
                    }
                  />
                  <CartesianGrid strokeDasharray="3 3" />
                  <Legend />
                  {/* <Line type="monotone" dataKey="uv" stroke="#82ca9d" /> */}
                </LineChart>
              </ResponsiveContainer>
              {/* <button
                style={{ marginLeft: "4rem" }}
                onClick={() => {
                  if (buttonText === "Show Roaming Revenue")
                    setButtonText("Hide Roaming Revenue");
                  else setButtonText("Show Roaming Revenue");

                  setShowRoamingData(!showRoamingData);
                }}
              >
                {buttonText}
              </button> */}
            </React.Fragment>
          )}
        </React.Fragment>
      );
    }
  }

  return (
    <div style={{ paddingRight: 20, paddingLeft: 30, paddingTop: 20 }}>
      {/* <h1 style={{ textAlign: "center", color: "#f76300", marginBottom: 40 }}>
        {" "}
        Sites Charts
      </h1> */}

      {ShowSitesList(areSiteCodesAvailable)}
    </div>
  );
};
