import React from "react";
import {
  Box,
  Container,
  Stack,
  Text,
  Link,
  useColorModeValue,
} from "@chakra-ui/react";

export default function Footer() {
  return (
    <Box
      bg={useColorModeValue("gray.50", "gray.900")}
      borderTopWidth={2}
      borderTopColor={useColorModeValue("teal.500", "teal.200")}
      minWidth={"100%"}
    >
      <Container
        as={Stack}
        maxW={"6xl"}
        py={4}
        direction={{ base: "column", md: "row" }}
        spacing={4}
        justify={{ base: "center", md: "space-between" }}
        align={{ base: "center", md: "center" }}
      >
        <Stack direction={"row"} spacing={6}>
          <Link
            href={"https://chaosinventory.readthedocs.io/en/latest/"}
            rel="nofollow noopener"
            target="_blank"
          >
            📕 Docs
          </Link>
          <Link
            href={"https://github.com/chaosinventory"}
            rel="nofollow noopener"
            target="_blank"
          >
            📄 Sources
          </Link>
        </Stack>
        <Text>© 2020 - {new Date().getFullYear()} Chaosinventory</Text>
      </Container>
    </Box>
  );
}
