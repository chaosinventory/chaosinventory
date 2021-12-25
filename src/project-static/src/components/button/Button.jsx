import { Button } from "@chakra-ui/react";
import React from "react";
import { EditIcon, DeleteIcon } from "@chakra-ui/icons";

export function EditButton(props) {
  return (
    <Button
      leftIcon={<EditIcon />}
      size="sm"
      colorScheme="blue"
      variant="ghost"
      {...props}
    >
      Edit
    </Button>
  );
}

export function DeleteButton(props) {
  return (
    <Button
      leftIcon={<DeleteIcon />}
      size="sm"
      colorScheme="red"
      variant="ghost"
      {...props}
    >
      Delete
    </Button>
  );
}

export function SubmitButton(props) {
  return (
    <Button colorScheme="green" type="submit" {...props}>
      Submit
    </Button>
  );
}
