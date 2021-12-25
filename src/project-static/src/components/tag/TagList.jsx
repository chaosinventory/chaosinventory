import React from "react";
import TagView from "./TagView";

export default function TagList({ data }) {
  return (
    <div>
      {data.map((tag) => {
        return <TagView key={tag.id} name={tag.name} parent={tag.parent} />;
      })}
    </div>
  );
}
