import React, { useContext } from "react";
import { useForm } from "react-hook-form";
import TagSelectSingle from "./TagSelectSingle";
import { SubmitButton } from "../button/Button";
import { useCiToast } from "../../hooks/Toast";
import DataUpdateContext from "../../context/DataUpdateContext";
import NameInput from "../input/NameInput";
import { patchTag, postTag } from "../../services/tagService";

export default function TagForm({ type, id, data }) {
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
      patchTag(id, data).then(
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
      postTag(data).then(
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
      <TagSelectSingle
        topMargin
        registerFunction={register("parent", { valueAsNumber: true })}
      />

      <SubmitButton mt={4} isLoading={isSubmitting} />
    </form>
  );
}
