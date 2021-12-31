import React from "react";
import {
  Link,
} from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";

export default function EntityLabel({ data }) {
  if (!data) {
    return <>...</>;
  } else {
    return (
      <Link
        as={RouterLink}
        to={"/app/entities/" + data.id}
      >
        {data.name}
      </Link>
    );
  }
}
