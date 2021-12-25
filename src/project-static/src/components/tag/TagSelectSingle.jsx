import React, { useEffect, useState } from "react";
import {
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  FormLabel,
  FormControl,
  Input,
  Select,
  Button,
  Textarea,
  Spinner,
  Alert,
} from "@chakra-ui/react";
import { useForm } from "react-hook-form";
import { getProducts } from "../../services/productService";
import { getTags, postTag } from "../../services/tagService";

export default function TagSelectSingle(props) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [data, setData] = useState([]);

  useEffect(() => {
    getTags().then(
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
    return <Alert status="error">{error.message}</Alert>;
  } else if (!isLoaded) {
    return <Spinner />;
  } else {
    return (
      <FormControl mt={props.topMargin ? 4 : 0}>
        <FormLabel htmlFor="parent">Parent</FormLabel>
        <Select
          placeholder="Select tag"
          name="parent"
          {...props.registerFunction}
        >
          {data.map((parent) => (
            <option key={parent.id} value={parent.id}>
              {parent.name}
            </option>
          ))}
        </Select>
      </FormControl>
    );
  }
}
