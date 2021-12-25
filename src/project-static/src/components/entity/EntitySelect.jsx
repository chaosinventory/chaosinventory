import {
  FormLabel,
  FormControl,
  Select,
  Spinner,
  Alert,
} from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { getEntities } from "../../services/entityService";

export default function EntitySelect(props) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [entities, setEntities] = useState([]);

  useEffect(() => {
    getEntities().then(
      (d) => {
        setIsLoaded(true);
        setEntities(d);
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
        <Select placeholder="Select entity" {...props.registerFunction}>
          {entities.map((entity) => (
            <option key={entity.id} value={entity.id}>
              {entity.name}
            </option>
          ))}
        </Select>
      </FormControl>
    );
  }
}
