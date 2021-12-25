import { Box, Divider, SimpleGrid, Text } from "@chakra-ui/layout";
import { Tooltip } from "@chakra-ui/tooltip";
import React, { useState, useEffect } from "react";
import { getItem } from "../../services/itemService";
import EntityView from "../entity/EntityView";
import LocationView from "../location/LocationView";
import TagList from "../tag/TagList";

export default function ItemView(props) {
  let componentData;

  if (props.fetchData) {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [data, setData] = useState([]);

    useEffect(() => {
      getItem(props.id).then(
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
      <Text fontSize="4xl">{componentData.name}</Text>
      <SimpleGrid columns={2} spacing={2}>
        <Text>Name</Text>
        <Tooltip label={componentData.note} aria-label="A tooltip">
          <Text fontWeight="bold">{componentData.name}</Text>
        </Tooltip>
        <Text>Tags</Text>
        {/** <TagList data={componentData.tags} /> */}
      </SimpleGrid>
      <br></br>
      <Divider />
      <Text fontSize="3xl">Owner</Text>
      <EntityView {...componentData.belongs_to} />
      <br></br>
      <Divider />
      <Text fontSize="3xl">Location</Text>
      <SimpleGrid columns={2} spacing={2}>
        <Text fontSize="2xl">Actual Location</Text>
        <Text fontSize="2xl">Target Location</Text>
        <LocationView {...componentData.actual_location} />
        <LocationView {...componentData.target_location} />
      </SimpleGrid>
    </div>
  );
}
