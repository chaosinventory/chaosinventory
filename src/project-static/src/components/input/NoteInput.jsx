import React from "react";
import {
  FormLabel,
  FormControl,
  FormErrorMessage,
  Textarea,
} from "@chakra-ui/react";

export default function NoteInput(props) {
  return (
    <FormControl mt={props.topMargin ? 4 : 0} isInvalid={props.isInvalid}>
      <FormLabel htmlFor="note">Note</FormLabel>
      <Textarea name="note" placeholder="Enter note..." {...props} />
      <FormErrorMessage>{props.errors}</FormErrorMessage>
    </FormControl>
  );
}
