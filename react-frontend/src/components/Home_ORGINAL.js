import React, { Component } from "react";
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
import FileUploadOutlinedIcon from "@mui/icons-material/FileUploadOutlined";
import ArrowBackIosNewOutlinedIcon from "@mui/icons-material/ArrowBackIosNewOutlined";
import { makeStyles } from "@material-ui/core";
import NewWindow from "react-new-window";

import "bootstrap/dist/css/bootstrap.min.css";
import "./home.css";
import "../config";

const useStyle = makeStyles({
  uploadBtn: {
    backgroundColor: "#f76300",
    marginTop: "2rem",
    float: "right",
  },
});

class Home extends Component {
  state = {
    uploadedFiles: [],

    in_tech_No_DWH_list: [],
    in_tech_No_DWH_total_revenue: 0.0,
    in_tech_No_DWH_buffer: "",

    in_DWH_No_tech_list: [],
    in_DWH_No_tech_total_revenue: 0.0,
    in_DWH_No_tech_buffer: "",

    DWH_Not_Match_tech_list: [],
    DWH_Not_Match_tech_total_revenue: 0.0,
    DWH_Not_Match_tech_buffer: "",

    Total_Revenue: 0.0,
    Total_Data: 0.0,
    Total_Voice: 0.0,

    isDataAvailable: false,
    showTable: false,
    current_table_to_display: [],
  };

  downloadFile = (file_name) => {
    console.log("DOWNLOAD BUTTON CLICKED!!!!!!!!!!");

    var file_URL = global.config.BACKEND_IP + "/api/downloadFiles/" + file_name;

    // Make a request to the backend to get the file, then open it in a new tab to download it
    axios.get(file_URL).then(() => {
      window.open(file_URL, "_blank");
    });
  };

  onFileChange = (event) => {
    // Update the state, append to it the file names

    if (this.state.uploadedFiles.length >= 2) {
      this.setState({
        uploadedFiles: [],
      });
    }
    this.setState((state) => {
      const files = [...state.uploadedFiles, event.target.files[0].name];
      return {
        uploadedFiles: files,
      };
    });
  };

  // On file upload (click the upload button)
  // handle if click upload without choosing a file
  onFileUpload = () => {
    var data = new FormData();
    const files = this.state;

    if (files.uploadedFiles.length == 0) alert("Please Choose a file");
    else {
      console.log("files.uploadedFiles.length");
      console.log(files.uploadedFiles.length);
      for (var f = 0; f < files.uploadedFiles.length; f++) {
        data.append(files.uploadedFiles[f], files.uploadedFiles[f]);
        // data.append("files", files.uploadedFiles[f]);
      }

      // Details of the uploaded file
      for (var p of data) {
        console.log("dataaaaaaaa:");
        console.log(p);
      }
      // Make a request to the backend api
      // Use trackPromise to display the spinner until the request is completed
      trackPromise(
        axios
          .post(global.config.BACKEND_IP + "/api/uploadExcelFiles", data)
          .then((response) => {
            console.log("Got the response");
            this.setState({
              in_tech_No_DWH_list:
                response.data.in_tech_No_DWH.in_tech_No_DWH_list,
              in_tech_No_DWH_total_revenue:
                response.data.in_tech_No_DWH.in_tech_No_DWH_total_revenue,
              in_tech_No_DWH_buffer:
                response.data.in_tech_No_DWH.in_tech_No_DWH_buffer,

              in_DWH_No_tech_list:
                response.data.in_DWH_No_tech.in_DWH_No_tech_list,
              in_DWH_No_tech_total_revenue:
                response.data.in_DWH_No_tech.in_DWH_No_tech_total_revenue,
              in_DWH_No_tech_buffer:
                response.data.in_DWH_No_tech.in_DWH_No_tech_buffer,

              DWH_Not_Match_tech_list:
                response.data.DWH_Not_Match_tech.DWH_Not_Match_tech_list,
              DWH_Not_Match_tech_total_revenue:
                response.data.DWH_Not_Match_tech
                  .DWH_Not_Match_tech_total_revenue,
              DWH_Not_Match_tech_buffer:
                response.data.DWH_Not_Match_tech.DWH_Not_Match_tech_buffer,

              Total_Revenue: response.data.Total_Revenue,
              Total_Data: response.data.Total_Data,
              Total_Voice: response.data.Total_Voice,

              isDataAvailable: true,
            }).then(() => console.log(response.data));
          })
      );
    }
  };

  ViewTableData = (tableContent) => {
    this.setState({
      showTable: true,
      current_table_to_display: tableContent,
    });
  };

  render() {
    if (this.state.showTable) {
      return (
        <React.Fragment>
          <div className="container">
            <button
              className="mt-4 mb-4 ml-7"
              onClick={() => this.setState({ showTable: false })}
              // startIcon={<ArrowBackIosNewOutlinedIcon fontSize="large" />}
            >
              Back
            </button>
          </div>
          <BasicTable data={this.state.current_table_to_display}></BasicTable>
        </React.Fragment>
      );
    } else {
      return (
        <div className="mt-7 container">
          <div className="info">
            <label className="form-label">Upload Cell Mapping File:</label>
            <input
              className="form-control form-control-lg"
              type="file"
              onChange={this.onFileChange}
              name="cell-mapping-report"
            />
          </div>

          <div className="info">
            <label className="form-label">Upload Site Revenue File:</label>
            <input
              className="form-control form-control-lg"
              type="file"
              onChange={this.onFileChange}
              name="site-revenue"
            />
            {/* startIcon & endIcon: to add icons inside the Button Tag either on the right or on the left*/}
            <button
              // variant="contained"
              className="mt-4 uploadBtn"
              onClick={() => this.onFileUpload()}
              // endIcon={<FileUploadOutlinedIcon fontSize="large" />}
            >
              Upload Files
            </button>
          </div>

          {this.state.isDataAvailable && (
            <div className="test">
              {/* spacing = to add margin between the items: 3*base = 3*8px */}
              <Grid container spacing={3}>
                <Grid item xs={4}>
                  <Card elevation={2}>
                    <CardHeader title="Total Revenue For Sites Found In Tech and not in DWH:"></CardHeader>
                    <CardContent>
                      {/* gutterBottom => to give a margin-bottom to the text */}
                      <Typography gutterBottom variant="h4" align="center">
                        {this.state.in_tech_No_DWH_total_revenue}
                      </Typography>
                    </CardContent>

                    <CardActions>
                      <Button
                        onClick={() =>
                          this.downloadFile(this.state.in_tech_No_DWH_buffer)
                        }
                        size="small"
                      >
                        Download File
                      </Button>
                      <Button
                        size="small"
                        onClick={() =>
                          this.ViewTableData(this.state.in_tech_No_DWH_list)
                        }
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
                        {this.state.in_DWH_No_tech_total_revenue}
                      </Typography>
                    </CardContent>

                    <CardActions>
                      <Button
                        onClick={() =>
                          this.downloadFile(this.state.in_DWH_No_tech_buffer)
                        }
                        size="small"
                      >
                        Download File
                      </Button>
                      <Button
                        size="small"
                        onClick={() =>
                          this.ViewTableData(this.state.in_DWH_No_tech_list)
                        }
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
                        {this.state.DWH_Not_Match_tech_total_revenue}
                      </Typography>
                    </CardContent>

                    <CardActions>
                      <Button
                        onClick={() =>
                          this.downloadFile(
                            this.state.DWH_Not_Match_tech_buffer
                          )
                        }
                        size="small"
                      >
                        Download File
                      </Button>
                      <Button
                        size="small"
                        onClick={() =>
                          this.ViewTableData(this.state.DWH_Not_Match_tech_list)
                        }
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
                        {this.state.Total_Revenue}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={4}>
                  <Card elevation={2}>
                    <CardHeader title="Total Data:"></CardHeader>
                    <CardContent>
                      <Typography gutterBottom variant="h4" align="center">
                        {this.state.Total_Data}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={4}>
                  <Card elevation={2}>
                    <CardHeader title="Total Voice:"></CardHeader>
                    <CardContent>
                      <Typography gutterBottom variant="h4" align="center">
                        {this.state.Total_Voice}
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
}

export default Home;
