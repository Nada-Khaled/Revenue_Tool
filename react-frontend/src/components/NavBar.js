import { useState } from "react";
import { Link } from "react-router-dom";
import "./revenueChart.css";

export const NavBar = () => {
  const [linksStyle, setLinksStyle] = useState({});

  const HandleLinkClicked = () => {
    if (linksStyle === {})
      setLinksStyle({
        borderRadius: 25,
        backgroundColor: "#e2e2e2",
      });
    else
      setLinksStyle({
        borderRadius: 25,
        backgroundColor: "",
      });
  };
  return (
    <div className="nav-bar">
      <nav className="navbar">
        <Link
          // style={linksStyle}
          className="navbar-brand"
          to="/"
          // onClick={HandleLinkClicked}
        >
          Home
        </Link>
        <Link
          // style={linksStyle}
          className="navbar-brand"
          to="/RevenueChartsPerSite"
          // onClick={HandleLinkClicked}
        >
          Show Sites Revenue
        </Link>
        <Link
          // style={{linksStyle}}
          className="navbar-brand"
          to="/RevenueChartsPerNetwork"
          // onClick={HandleLinkClicked}
        >
          Show Network Revenue
        </Link>
      </nav>
    </div>
  );
};

export default NavBar;
