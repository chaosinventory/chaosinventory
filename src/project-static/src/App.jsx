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
            <Route path="/login">
              <Login />
            </Route>
            <ProtectedRoute path="/products">
              <Products />
            </ProtectedRoute>
            <ProtectedRoute path="/locations">
              <Locations />
            </ProtectedRoute>
            <ProtectedRoute path="/overlays">
              <Overlays />
            </ProtectedRoute>
            <ProtectedRoute path="/entities">
              <Entities />
            </ProtectedRoute>
            <ProtectedRoute path="/tags">
              <Tags />
            </ProtectedRoute>
            <ProtectedRoute path="/datatypes">
              <DataTypes />
            </ProtectedRoute>
            <ProtectedRoute path="/">
              <Items />
            </ProtectedRoute>
          </Switch>
        </Layout>
      </Router>
    </DataUpdateContext.Provider>
  );
}

export default App;
