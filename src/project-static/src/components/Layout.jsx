import React from "react";
import {
  Box,
  Flex,
  Square,
  Text,
  Button,
  useColorModeValue,
  Container,
  Stack,
} from "@chakra-ui/react";
import Footer from "./Footer";
import Navbar from "./Navbar";
import { useHistory } from "react-router";

export default function Layout(props) {
  let history = useHistory();

  return (
    <>
      <Flex minH={"100vh"} flexDirection={"column"}>
        <Navbar />
        <Box flex={1}>
          <Container
            as={Stack}
            maxW={"7xl"}
            py={4}
            direction={{ base: "column", md: "row" }}
            spacing={4}
            justify={{ base: "center", md: "space-between" }}
            align={{ base: "flex-start", md: "flex-start" }}
          >
            {props.children}
          </Container>
        </Box>
        <Footer />
      </Flex>
    </>
  );
}
