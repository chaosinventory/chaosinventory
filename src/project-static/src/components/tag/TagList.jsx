import React from "react";
import TagLabel from "./TagLabel";

export default function TagList({ data }) {
  return (
    <div>
      {data.map((tag) => {
        return <TagLabel data={tag} />;
      })}
    </div>
  );
}
