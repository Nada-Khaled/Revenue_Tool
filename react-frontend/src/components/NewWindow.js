import React, { useState, useEffect } from "react";
import { Button } from "reactstrap";
import NewWindow from "react-new-window";
import parse from "html-react-parser";

const dataX12 =
  '<html><head><style>.yolo{background-color:yellow; color: red}</style></head><body><div><h1 class="yolo">Hello World</h1><button onclick="myFunction()">Try it</button><script>function myFunction() {alert("Hello! I am an alert box!");}</script></body></html>';

// let htmlX12 = parse(dataX12);

const createMarkup = () => {
  return { __html: dataX12 };
};

const Viewer = () => {
  const [title, setTitle] = useState(null);

  useEffect(() => {
    // Update the document title using the browser API
    document.title = `You clicked times`;
  }, []);

  return (
    <NewWindow
      title="yolo"
      features={{
        outerHeight: "100%",
        outerWidth: "100%",
      }}
    >
      <html dangerouslySetInnerHTML={createMarkup()} />
    </NewWindow>
  );
};

export default Viewer;
