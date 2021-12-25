import {
  FormLabel,
  FormControl,
  Select,
  Spinner,
  Alert,
} from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { getProducts } from "../../services/productService";

export default function ProductSelect(props) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [products, setProducts] = useState([]);

  useEffect(() => {
    getProducts().then(
      (d) => {
        setIsLoaded(true);
        setProducts(d);
      },
      (e) => {
        setIsLoaded(true);
        setError(e);
      }
    );
  }, []);

  if (error) {
    return <Alert status="error">{error.message}</Alert>;
  } else if (!isLoaded) {
    return <Spinner />;
  } else {
    return (
      <FormControl mt={props.topMargin ? 4 : 0}>
        <FormLabel htmlFor={props.name}>{props.label}</FormLabel>
        <Select
          placeholder="Select product"
          name={props.name}
          {...props.registerFunction}
        >
          {products.map((product) => (
            <option key={product.id} value={product.id}>
              {product.name}
            </option>
          ))}
        </Select>
      </FormControl>
    );
  }
}
