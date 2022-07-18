import React, { useEffect, useState } from "react";
import axios from "axios";
import { trackPromise } from "react-promise-tracker";
import { BasicTable } from "./BasicTable";
import { TableData } from "./TableData";
import Grid from "@material-ui/core/Grid";
import { Container } from "@material-ui/core";
import Card from "@mui/material/Card";
import { CardHeader } from "@mui/material";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

import "bootstrap/dist/css/bootstrap.min.css";
import "./home.css";
import "../config";

export const Home = () => {
  const [in_tech_No_DWH_list, set_in_tech_No_DWH_list] = useState([]);
  const [in_tech_No_DWH_total_revenue, set_in_tech_No_DWH_total_revenue] =
    useState(0.0);
  const [in_tech_No_DWH_buffer, set_in_tech_No_DWH_buffer] = useState("");

  const [in_DWH_No_tech_list, set_in_DWH_No_tech_list] = useState([]);
  const [in_DWH_No_tech_total_revenue, set_in_DWH_No_tech_total_revenue] =
    useState(0.0);
  const [in_DWH_No_tech_buffer, set_in_DWH_No_tech_buffer] = useState("");

  const [DWH_Not_Match_tech_list, set_DWH_Not_Match_tech_list] = useState([]);
  const [
    DWH_Not_Match_tech_total_revenue,
    set_DWH_Not_Match_tech_total_revenue,
  ] = useState(0.0);
  const [DWH_Not_Match_tech_buffer, set_DWH_Not_Match_tech_buffer] =
    useState("");

  const [Total_Revenue, set_Total_Revenue] = useState(0.0);
  const [Total_Data, set_Total_Data] = useState(0.0);
  const [Total_Voice, set_Total_Voice] = useState(0.0);

  const [isDataAvailable, set_isDataAvailable] = useState(false);
  const [showTable, set_showTable] = useState(false);
  const [current_table_to_display, set_current_table_to_display] = useState([]);

  const [Years_Months_List, set_Years_Months_List] = useState([]);
  const [Selected_Month, set_Selected_Month] = useState("");

  // fih moskela f-el download kda, hagibo mnen w ana mb2tsh b save el file 3la el server asln
  const downloadFile = (file_name) => {
    file_name += "|" + Selected_Month;
    // console.log("DOWNLOAD BUTTON CLICKED with file name: ", file_name);

    var file_URL = global.config.BACKEND_IP + "/api/downloadFiles/" + file_name;

    // Make a request to the backend to get the file, then open it in a new tab to download it
    axios.get(file_URL).then(() => {
      window.open(file_URL, "_blank");
    });
  };

  // On loading the component, get all months
  useEffect(() => {

    // console.log('In useEffect() of Home.js...')
    // console.log(global.config.BACKEND_IP + "/api/getAllYearsMonths")

    // used to stop updating the state if I navigated to another component
    // to avoid a warning, by stopping the fetch operation
    // it is used in fetch functions
    const abortController = new AbortController();
    trackPromise(
      axios.get(global.config.BACKEND_IP + "/api/getAllYearsMonths", {
          signal: abortController.signal,
        }).then((response) => {
          // console.log('response.data["YearsMonthsList"]')
          // console.log(response.data["YearsMonthsList"])
          set_Years_Months_List(response.data["YearsMonthsList"]);
        })
    );

    // Clean up function to stop updating the state if I navigated
    // to another component to avoid a warning
    return () => abortController.abort();

  // trackPromise(
  //     fetch('http://127.0.0.1:5000/api/getAllYearsMonths')
  //     // fetch(global.config.BACKEND_IP + "/api/getAllYearsMonths")
  //     // fetch('https://jsonplaceholder.typicode.com/todos/1')
  //       .then(response => response.json())
  //       .then(json => console.log(json)).then((response) => {
  //               console.log('response.data["YearsMonthsList"]')
  //               console.log(response.data["YearsMonthsList"])
  //               set_Years_Months_List(response.data["YearsMonthsList"]);
  //             })
  // );
  }, []);

  const GetMonthRevenues = (evt) => {
    var selectedMonth = evt.target.value;

    set_isDataAvailable(false);

    // console.log('In onChange for GetMonthRevenues after choosing a month')

    set_Selected_Month(selectedMonth);

    trackPromise(
      axios
        .get(
          global.config.BACKEND_IP + "/api/getMonthRevenues/" + selectedMonth
        )
        .then((response) => {
          console.log("Got the response");

          set_in_tech_No_DWH_list(
            response.data.in_tech_No_DWH.in_tech_No_DWH_list
          );
          set_in_tech_No_DWH_total_revenue(
            response.data.in_tech_No_DWH.in_tech_No_DWH_total_revenue
          );
          set_in_tech_No_DWH_buffer(
            response.data.in_tech_No_DWH.in_tech_No_DWH_buffer
          );

          set_in_DWH_No_tech_list(
            response.data.in_DWH_No_tech.in_DWH_No_tech_list
          );
          set_in_DWH_No_tech_total_revenue(
            response.data.in_DWH_No_tech.in_DWH_No_tech_total_revenue
          );
          set_in_DWH_No_tech_buffer(
            response.data.in_DWH_No_tech.in_DWH_No_tech_buffer
          );

          set_DWH_Not_Match_tech_list(
            response.data.DWH_Not_Match_tech.DWH_Not_Match_tech_list
          );
          set_DWH_Not_Match_tech_total_revenue(
            response.data.DWH_Not_Match_tech.DWH_Not_Match_tech_total_revenue
          );
          set_DWH_Not_Match_tech_buffer(
            response.data.DWH_Not_Match_tech.DWH_Not_Match_tech_buffer
          );

          set_Total_Revenue(response.data.Total_Revenue);
          set_Total_Data(response.data.Total_Data);
          set_Total_Voice(response.data.Total_Voice);

          set_isDataAvailable(true);
        })
    );
  };

  const ViewTableData = (tableContent) => {
    set_showTable(true);
    set_current_table_to_display(tableContent);
  };

  function ViewMonthRevenue() {
    if (showTable) {
      return (
        <React.Fragment>
          <div className="container">
            <button
              className="mt-4 mb-4 ml-7"
              onClick={() => set_showTable(false)}
              // startIcon={<ArrowBackIosNewOutlinedIcon fontSize="large" />}
            >
              Back
            </button>
          </div>
          <BasicTable data={current_table_to_display}></BasicTable>
        </React.Fragment>
      );
    } else {
      return (
        <div className="mt-7 container">
          <div className="info">
            <label className="form-label">Choose month to show revenue:</label>
            <select
              placeholder="Select Month"
              className="form-select mb-4"
              onChange={GetMonthRevenues}
            >
              {Years_Months_List.map((yearMonth) => {
                return (
                  <option value={yearMonth} key={yearMonth}>
                    {yearMonth}
                  </option>
                );
              })}
            </select>
          </div>

          {isDataAvailable && (
            <div className="test">
              {/* spacing = to add margin between the items: 3*base = 3*8px */}
              <Grid container spacing={3}>
                <Grid item xs={4}>
                  <Card elevation={2}>
                    <CardHeader title="Total Revenue For Sites Found In Tech and not in DWH:"></CardHeader>
                    <CardContent>
                      {/* gutterBottom => to give a margin-bottom to the text */}
                      <Typography gutterBottom variant="h4" align="center">
                        {in_tech_No_DWH_total_revenue}
                      </Typography>
                    </CardContent>

                    <CardActions>
                      <Button
                        onClick={() => downloadFile(in_tech_No_DWH_buffer)}
                        size="small"
                      >
                        Download File
                      </Button>
                      <Button
                        size="small"
                        onClick={() => ViewTableData(in_tech_No_DWH_list)}
                      >
                        View File Content
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>

                <Grid item xs={4}>
                  <Card elevation={2}>
                    <CardHeader title="Total Revenue For Sites Found In DWH and not in Tech:"></CardHeader>
                    <CardContent>
                      <Typography gutterBottom variant="h4" align="center">
                        {in_DWH_No_tech_total_revenue}
                      </Typography>
                    </CardContent>

                    <CardActions>
                      <Button
                        onClick={() => downloadFile(in_DWH_No_tech_buffer)}
                        size="small"
                      >
                        Download File
                      </Button>
                      <Button
                        size="small"
                        onClick={() => ViewTableData(in_DWH_No_tech_list)}
                      >
                        View File Content
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>

                <Grid item xs={4}>
                  <Card elevation={2}>
                    <CardHeader title="Total Revenue For Sites That don't match In Tech and DWH:"></CardHeader>
                    <CardContent>
                      <Typography gutterBottom variant="h4" align="center">
                        {DWH_Not_Match_tech_total_revenue}
                      </Typography>
                    </CardContent>

                    <CardActions>
                      <Button
                        onClick={() => downloadFile(DWH_Not_Match_tech_buffer)}
                        size="small"
                      >
                        Download File
                      </Button>
                      <Button
                        size="small"
                        onClick={() => ViewTableData(DWH_Not_Match_tech_list)}
                      >
                        View File Content
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>

                <Grid item xs={4}>
                  <Card elevation={2}>
                    <CardHeader title="Total Revenue:"></CardHeader>
                    <CardContent>
                      <Typography gutterBottom variant="h4" align="center">
                        {Total_Revenue}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={4}>
                  <Card elevation={2}>
                    <CardHeader title="Total Data:"></CardHeader>
                    <CardContent>
                      <Typography gutterBottom variant="h4" align="center">
                        {Total_Data}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={4}>
                  <Card elevation={2}>
                    <CardHeader title="Total Voice:"></CardHeader>
                    <CardContent>
                      <Typography gutterBottom variant="h4" align="center">
                        {Total_Voice}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </div>
          )}
        </div>
      );
    }
  }

  return <React.Fragment>{ViewMonthRevenue()}</React.Fragment>;
};
