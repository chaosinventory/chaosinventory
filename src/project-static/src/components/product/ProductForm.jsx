import React, { useContext } from "react";
import { useForm } from "react-hook-form";
import { SubmitButton } from "../button/Button";
import { useCiToast } from "../../hooks/Toast";
import DataUpdateContext from "../../context/DataUpdateContext";
import NameInput from "../input/NameInput";
import NoteInput from "../input/NoteInput";
import { postProduct } from "../../services/productService";

export default function ProductForm({ type, id, data }) {
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
      patchProduct(id, data).then(
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
      postProduct(data).then(
        (data) => {
          setLastUpdate(Date.now());
          toast({
            status: "success",
            title: "Created",
            description: `The entity ${data.name} with the id ${data.id} has been created`,
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
