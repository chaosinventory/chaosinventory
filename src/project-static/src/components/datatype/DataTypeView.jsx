import { Text } from "@chakra-ui/layout";
import { Tooltip } from "@chakra-ui/tooltip";
import React, { useState, useEffect } from "react";
import { getDatatype } from "../../services/datatypeService";

export default function DataTypeView(props) {
  let name;
  let note;

  if (props.fetchData) {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [data, setData] = useState([]);

    useEffect(() => {
      getDatatype(props.id).then(
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
      name = data.name;
      note = data.note;
    }
  } else {
    name = props.name;
    note = props.note;
  }

  return (
    <div className="info-data-type">
      <Tooltip label={note} aria-label="A tooltip">
        <Text fontWeight="bold">{name}</Text>
      </Tooltip>
    </div>
  );
}
