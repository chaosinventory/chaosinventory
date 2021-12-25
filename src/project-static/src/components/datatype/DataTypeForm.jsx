import React, { useContext } from "react";
import { useForm } from "react-hook-form";
import { patchDatatype, postDatatype } from "../../services/datatypeService";
import PropTypes from "prop-types";
import DataUpdateContext from "../../context/DataUpdateContext";
import NameInput from "../input/NameInput";
import NoteInput from "../input/NoteInput";
import { SubmitButton } from "../button/Button";
import { useCiToast } from "../../hooks/Toast";

function DataTypeForm({ type, id, data }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();
  const toast = useCiToast();
  const { lastUpdate, setLastUpdate } = useContext(DataUpdateContext);
  let onSubmit;

  if (type === "edit") {
    onSubmit = (data) => {
      patchDatatype(id, data).then(
        (data) => {
          setLastUpdate(Date.now());
          toast({
            status: "success",
            title: "Created",
            description: `The datatype ${data.name} with the id ${data.id} has been updated`,
          });
        },
        (err) => {
          toast({
            status: "error",
            title: "Error",
            description: err.message,
          });
        }
      );
    };
  } else {
    onSubmit = (data) => {
      postDatatype(data).then(
        (data) => {
          setLastUpdate(Date.now());
          toast({
            status: "success",
            title: "Created",
            description: `The datatype ${data.name} with the id ${data.id} has been created`,
          });
        },
        (err) => {
          toast({
            status: "error",
            title: "Error",
            description: err.message,
          });
        }
      );
    };
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <NameInput
        required
        isInvalid={errors.name}
        defaultValue={type === "edit" ? data.name : null}
        errors={errors.name && errors.name.message}
        {...register("name", { required: "Name is required!" })}
      />
      <NoteInput
        topMargin
        isInvalid={errors.note}
        defaultValue={type === "edit" ? data.note : null}
        errors={errors.note && errors.note.message}
        {...register("note")}
      />
      <SubmitButton mt={4} isLoading={isSubmitting} />
    </form>
  );
}

DataTypeForm.propTypes = {
  type: PropTypes.oneOf(["create", "edit"]),
  id: PropTypes.number,
  data: PropTypes.object,
};

export default DataTypeForm;
