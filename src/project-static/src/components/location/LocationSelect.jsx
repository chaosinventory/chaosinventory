import {
  FormLabel,
  FormControl,
  Select,
  Spinner,
  Alert,
} from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { getLocations } from "../../services/locationService";

export default function LocationSelect(props) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [locations, setLocations] = useState([]);

  useEffect(() => {
    getLocations().then(
      (d) => {
        setIsLoaded(true);
        setLocations(d);
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
          placeholder="Select location"
          name={props.name}
          {...props.registerFunction}
        >
          {locations.map((location) => (
            <option key={location.id} value={location.id}>
              {location.name}
            </option>
          ))}
        </Select>
      </FormControl>
    );
  }
}
