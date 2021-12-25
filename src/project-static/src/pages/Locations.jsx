import React from "react";
import LocationTable from "../components/location/LocationTable";
import LocationForm from "../components/location/LocationForm";

export default function Locations() {
  return (
    <>
      <LocationForm />
      <LocationTable />
    </>
  );
}
