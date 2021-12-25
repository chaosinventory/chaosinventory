import React, { useEffect, useState } from "react";
import { Spinner, Table, Thead, Tr, Th, Tbody, Td } from "@chakra-ui/react";
import { getLocations } from "../../services/locationService";
import { useContext } from "react";
import DataUpdateContext from "../../context/DataUpdateContext";

export default function ProductTable() {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);

  const { lastUpdate, setLastUpdate } = useContext(DataUpdateContext);

  useEffect(() => {
    getLocations().then(
      (data) => {
        setIsLoaded(true);
        setItems(data);
      },
      (err) => {
        setIsLoaded(true);
        setError(err);
      }
    );
  }, [lastUpdate]);

  if (error) {
    return (
      <Alert status="error">
        <AlertIcon />
        {error.message}
      </Alert>
    );
  } else if (!isLoaded) {
    return <Spinner />;
  } else {
    return (
      <Table variant="simple" size="sm">
        <Thead>
          <Tr>
            <Th>Name</Th>
            <Th>Note</Th>
            <Th>In Location</Th>
          </Tr>
        </Thead>
        <Tbody>
          {items.map((item) => (
            <Tr key={item.id}>
              <Td>{item.name}</Td>
              <Td>{item.note}</Td>
              <Td>{item.in_location ? item.in_location.name : "..."}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    );
  }
}
