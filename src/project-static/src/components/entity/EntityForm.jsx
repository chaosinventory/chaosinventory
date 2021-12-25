import React from "react";
import { useContext } from "react";
import { useForm } from "react-hook-form";
import DataUpdateContext from "../../context/DataUpdateContext";
import { patchEntity, postEntity } from "../../services/entityService";
import NameInput from "../input/NameInput";
import NoteInput from "../input/NoteInput";
import { useCiToast } from "../../hooks/Toast";
import EntitySelect from "../entity/EntitySelect";
import { SubmitButton } from "../button/Button";

export default function EntityForm({ type, id, data }) {
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
      patchEntity(id, data).then(
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
      console.log(data);
      postEntity(data).then(
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
      <EntitySelect
        topMargin
        label="Part Of"
        name="part_of"
        registerFunction={register("part_of", { valueAsNumber: true })}
      />

      <SubmitButton mt={4} isLoading={isSubmitting} />
    </form>
  );
}
