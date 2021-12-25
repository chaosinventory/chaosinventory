import React, { useEffect, useState } from "react";
import {
  Spinner,
  Table,
  Thead,
  Tr,
  Th,
  Tbody,
  Td,
  Button,
} from "@chakra-ui/react";
import { EditIcon, DeleteIcon } from "@chakra-ui/icons";
import { getEntities } from "../../services/entityService";
import TagList from "../tag/TagList";
import { useContext } from "react";
import DataUpdateContext from "../../context/DataUpdateContext";

export default function EntityTable() {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);

  const { lastUpdate, setLastUpdate } = useContext(DataUpdateContext);

  useEffect(() => {
    getEntities().then(
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
            <Th>Part of</Th>
            <Th>Tags</Th>
            <Th></Th>
          </Tr>
        </Thead>
        <Tbody>
          {items.map((item) => (
            <Tr key={item.id}>
              <Td>{item.name}</Td>
              <Td>{item.note}</Td>
              <Td>{item.part_of ? item.part_of.name : "Nothing"}</Td>
              <Td>
                <TagList data={item.tags} />
              </Td>
              <Td textAlign="right  ">
                <Button
                  leftIcon={<EditIcon />}
                  size="sm"
                  colorScheme="blue"
                  variant="ghost"
                >
                  Edit
                </Button>
                <Button
                  leftIcon={<DeleteIcon />}
                  size="sm"
                  colorScheme="red"
                  variant="ghost"
                >
                  Delete
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    );
  }
}
