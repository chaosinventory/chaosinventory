import React, { useEffect, useState } from "react";
import { getLocation } from "../../services/locationService";

export default function LocationLabel(props) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [data, setData] = useState([]);

  useEffect(() => {
    getLocation(props.id).then(
      (d) => {
        setIsLoaded(true);
        setData(d);
      },
      (e) => {
        setIsLoaded(true);
        setError(e);
      }
    );
  }, []);

  if (error) {
    return <>{error.message}</>;
  } else if (!isLoaded) {
    return <>...</>;
  } else {
    return <>{data.name}</>;
  }
}
