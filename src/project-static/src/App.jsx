import React, { useState } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Items from "./pages/Items";
import Tags from "./pages/Tags";
import Entities from "./pages/Entities";
import Products from "./pages/Products";
import DataTypes from "./pages/DataTypes";
import Overlays from "./pages/Overlays";
import Locations from "./pages/Locations";
import DataUpdateContext from "./context/DataUpdateContext";

function App() {
  const [lastUpdate, setLastUpdate] = useState(Date.now());

  return (
    <DataUpdateContext.Provider value={{ lastUpdate, setLastUpdate }}>
      <Router>
        <Layout>
          <Switch>
            <Route path="/app/products">
              <Products />
            </Route>
            <Route path="/app/locations">
              <Locations />
            </Route>
            <Route path="/app/overlays">
              <Overlays />
            </Route>
            <Route path="/app/entities">
              <Entities />
            </Route>
            <Route path="/app/tags">
              <Tags />
            </Route>
            <Route path="/app/datatypes">
              <DataTypes />
            </Route>
            <Route path="/app/">
              <Items />
            </Route>
          </Switch>
        </Layout>
      </Router>
    </DataUpdateContext.Provider>
  );
}

export default App;
