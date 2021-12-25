import React, { useState } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import Items from "./pages/Items";
import Login from "./pages/Login";
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
            <Route path="/app/login">
              <Login />
            </Route>
            <ProtectedRoute path="/app/products">
              <Products />
            </ProtectedRoute>
            <ProtectedRoute path="/app/locations">
              <Locations />
            </ProtectedRoute>
            <ProtectedRoute path="/app/overlays">
              <Overlays />
            </ProtectedRoute>
            <ProtectedRoute path="/app/entities">
              <Entities />
            </ProtectedRoute>
            <ProtectedRoute path="/app/tags">
              <Tags />
            </ProtectedRoute>
            <ProtectedRoute path="/app/datatypes">
              <DataTypes />
            </ProtectedRoute>
            <ProtectedRoute path="/app/">
              <Items />
            </ProtectedRoute>
          </Switch>
        </Layout>
      </Router>
    </DataUpdateContext.Provider>
  );
}

export default App;
