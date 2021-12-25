import React from "react";
import {
  FormLabel,
  FormControl,
  FormErrorMessage,
  Input,
} from "@chakra-ui/react";

export default function NameInput(props) {
  return (
    <FormControl mt={props.topMargin ? 4 : 0} isInvalid={props.isInvalid}>
      <FormLabel htmlFor="name">Name{props.required ? "*" : ""}</FormLabel>
      <Input name="name" placeholder="Enter name..." {...props} />
      <FormErrorMessage>{props.errors}</FormErrorMessage>
    </FormControl>
  );
}
