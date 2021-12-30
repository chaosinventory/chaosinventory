import React from "react";
import {
  Tag,
  Link,
} from "@chakra-ui/react";
import { TriangleDownIcon } from "@chakra-ui/icons";
import { Link as RouterLink } from "react-router-dom";

export default function TagLabel({ data }) {
  return (
    <Link
      as={RouterLink}
      to={"/app/tags/" + data.id}
    >
      <Tag>
        {data.name}
      </Tag>
    </Link>
  );
}
