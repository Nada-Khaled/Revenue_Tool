import React from "react";
import { usePromiseTracker } from "react-promise-tracker";

import { TailSpin } from "react-loader-spinner";

const LoadingIndicator = (props) => {
  const { promiseInProgress } = usePromiseTracker();
  let initialization = false;

  return (
    <div className="container">
      {promiseInProgress && (
        <div
          style={{
            width: "100%",
            height: "100",
            marginTop: 10,
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <span style={{ fontWeight: 500, fontSize: 30, marginBottom: 30 }}>
            Please wait...{" "}
          </span>
          <TailSpin color="#00BFFF" height={80} width={80} />
        </div>
      )}
    </div>

    // <div className='container'>
    // {
    //     promiseInProgress
    //     ? <h1>Please wait until uploading your files! </h1>
    //     : <h1>Your files are ready :) </h1>
    // }
    // </div>
  );
};

export default LoadingIndicator;
