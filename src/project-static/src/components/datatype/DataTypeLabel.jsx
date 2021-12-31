import React from "react";
import {
  Link,
} from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";

export default function DataTypeLabel({ data }) {
  if (!data) {
    return <>...</>;
  } else {
    return (
      <Link
        as={RouterLink}
        to={"/app/datatypes/" + data.id}
      >
        {data.name}
      </Link>
    );
  }
}
