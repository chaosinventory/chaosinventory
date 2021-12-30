import React, { useEffect, useState } from "react";
import { getItems } from "../../services/itemService";
import {
  Alert,
  AlertIcon,
  Table,
  Thead,
  Tbody,
  Spinner,
  Tr,
  Th,
  Td,
  HStack,
} from "@chakra-ui/react";
import { useContext } from "react";
import DataUpdateContext from "../../context/DataUpdateContext";
import TagList from "../tag/TagList";

export default function ItemTable() {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);

  const { lastUpdate, setLastUpdate } = useContext(DataUpdateContext);

  useEffect(() => {
    getItems().then(
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
            <Th>Typ</Th>
            <Th>Amount</Th>
            <Th>Location</Th>
            <Th>Belongs to</Th>
            <Th>Tags</Th>
          </Tr>
        </Thead>
        <Tbody>
          {items.map((item) => (
            <Tr key={item.id}>
              <Td>{item.name}</Td>
              <Td>{item.product.name}</Td>
              <Td>{item.amount}</Td>
              <Td>{item.actual_location != null ? item.actual_location.name : <>...</>}</Td>
              <Td>{item.actual_item != null ? <>?</> : <>...</>}</Td>
              <Td><TagList data={item.tags} /></Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    );
  }
}
