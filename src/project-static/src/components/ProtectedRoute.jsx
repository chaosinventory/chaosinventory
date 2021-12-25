import React from "react";
import { Route, Redirect } from "react-router-dom";
import { authenticationService } from "../services/authenticationService";

function ProtectedRoute({ children, ...rest }) {
  let auth = authenticationService.loggedIn();
  return (
    <Route
      {...rest}
      render={({ location }) =>
        auth ? (
          children
        ) : (
          <Redirect
            to={{
              pathname: "/login",
              state: { from: location },
            }}
          />
        )
      }
    />
  );
}

export default ProtectedRoute;
