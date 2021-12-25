import { Box, SimpleGrid, Text } from "@chakra-ui/layout";
import { Tooltip } from "@chakra-ui/tooltip";
import React, { useState, useEffect } from "react";
import { getLocation } from "../../services/locationService";

export default function LocationView(props) {
  let componentData;

  if (props.fetchData) {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [data, setData] = useState([]);

    useEffect(() => {
      getLocation(props.id).then(
        (result) => {
          setIsLoaded(true);
          setData(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      );
    }, []);

    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      componentData = data;
    }
  } else {
    componentData = props;
  }

  return (
    <div className="info-data-type">
      <SimpleGrid columns={2} spacing={2}>
        <Text>Name</Text>
        <Tooltip label={componentData.note} aria-label="A tooltip">
          <Text fontWeight="bold">{componentData.name}</Text>
        </Tooltip>
        <Text>Parent</Text>
        {componentData.in_location && (
          <LocationView {...componentData.in_location} />
        )}
      </SimpleGrid>
    </div>
  );
}
