import React, { useEffect, useState } from "react";
import { getTag } from "../../services/tagService";
import { Tag } from "@chakra-ui/react";
import { TriangleDownIcon } from "@chakra-ui/icons";

export default function TagView(props) {
  let name;
  let hasParent;

  if (props.fetchData) {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [data, setData] = useState([]);

    useEffect(() => {
      getTag(props.id).then(
        (d) => {
          setIsLoaded(true);
          setData(d);
        },
        (e) => {
          setIsLoaded(true);
          setError(e);
        }
      );
    }, []);

    if (error) {
      return <>{error.message}</>;
    } else if (!isLoaded) {
      return <>...</>;
    } else {
      name = data.name;
      hasParent = data.parent ? true : false;
    }
  } else {
    name = props.name;
    hasParent = props.parent ? true : false;
  }

  return (
    <Tag>
      {hasParent && <TriangleDownIcon />} {name}
    </Tag>
  );
}
