import {
  Flex,
  Box,
  FormControl,
  FormLabel,
  Input,
  Stack,
  Button,
  Heading,
  useColorModeValue,
} from "@chakra-ui/react";
import React from "react";
import { useHistory } from "react-router";
import { authenticationService } from "../services/authenticationService";
import { useContext } from "react";
import { useForm } from "react-hook-form";
import DataUpdateContext from "../context/DataUpdateContext";
import { patchEntity, postEntity } from "../services/entityService";
import NameInput from "../components/input/NameInput";
import NoteInput from "../components/input/NoteInput";
import { useCiToast } from "../hooks/Toast";
import ProductSelect from "../components/product/ProductSelect";
import { SubmitButton } from "../components/button/Button";
import { patchItem, postItem } from "../services/itemService";

function loginUser(event, history) {
  event.preventDefault();
  authenticationService.login(
    event.target.username.value,
    event.target.password.value
  );
  history.push("/");
}

export default function Login() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();
  let history = useHistory();
  const toast = useCiToast();
  const onSubmit = (data) => {
    authenticationService.login(data.username, data.password).then(() => {
      console.log("Login successful");
      history.push("/items");
    });
  };

  return (
    <Flex
      minH={"100%"}
      minW={"100%"}
      align={"center"}
      justify={"center"}
      bg={useColorModeValue("blue.50", "blue.800")}
    >
      <Stack spacing={8} mx={"auto"} maxW={"lg"} py={12} px={6}>
        <Stack align={"center"}>
          <Heading fontSize={"4xl"}>Chaosinventory</Heading>
        </Stack>
        <Box
          rounded={"lg"}
          bg={useColorModeValue("white", "gray.700")}
          boxShadow={"lg"}
          p={8}
        >
          <form onSubmit={handleSubmit(onSubmit)}>
            <Stack spacing={4}>
              <FormControl id="username">
                <FormLabel>Username</FormLabel>
                <Input
                  type="username"
                  placeholder="janedoe"
                  {...register("username", { required: "Name is required!" })}
                />
              </FormControl>
              <FormControl id="password">
                <FormLabel>Password</FormLabel>
                <Input
                  type="password"
                  placeholder="*********"
                  {...register("password", {
                    required: "Password is required!",
                  })}
                />
              </FormControl>
              <Stack spacing={10}>
                <Button
                  bg={"blue.400"}
                  color={"white"}
                  type="submit"
                  _hover={{
                    bg: "blue.500",
                  }}
                >
                  Sign in
                </Button>
              </Stack>
            </Stack>
          </form>
        </Box>
      </Stack>
    </Flex>
  );
}
