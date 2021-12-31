import React, { useEffect, useState, useContext } from "react";
import {
  Spinner,
  Table,
  Thead,
  Tr,
  Th,
  Tbody,
  Td,
  Button,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
} from "@chakra-ui/react";
import { EditIcon, DeleteIcon } from "@chakra-ui/icons";
import { deleteDatatype, getDatatypes } from "../../services/datatypeService";
import DataTypeForm from "./DataTypeForm";
import DataTypeLabel from "./DataTypeLabel";
import DataUpdateContext from "../../context/DataUpdateContext";
import { DeleteButton, EditButton } from "../button/Button";

export default function DataTypeTable() {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [selectedData, setSelectedData] = useState({});
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { lastUpdate, setLastUpdate } = useContext(DataUpdateContext);

  useEffect(() => {
    getDatatypes().then(
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
      <>
        <Table variant="simple" size="sm">
          <Thead>
            <Tr>
              <Th>Name</Th>
              <Th>Note</Th>
              <Th></Th>
            </Tr>
          </Thead>
          <Tbody>
            {items.map((item) => (
              <Tr key={item.id}>
                <Td><DataTypeLabel data={item} /></Td>
                <Td>{item.note}</Td>
                <Td textAlign="right">
                  <EditButton
                    onClick={() => {
                      setSelectedData(item);
                      onOpen();
                    }}
                  />
                  <DeleteButton
                    onClick={() => {
                      deleteDatatype(item.id);
                      setLastUpdate(Date.now());
                    }}
                  />
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>

        <Modal isOpen={isOpen} onClose={onClose}>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Modal Title</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <DataTypeForm
                type="edit"
                id={selectedData.id}
                data={selectedData}
              />
            </ModalBody>
          </ModalContent>
        </Modal>
      </>
    );
  }
}
