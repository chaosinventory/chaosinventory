import React, { useEffect, useState } from "react";
import { getProduct } from "../../services/productService";

export default function ProductLabel(props) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [data, setData] = useState([]);

  useEffect(() => {
    getProduct(props.id).then(
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
