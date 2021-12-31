import React, { useContext, useEffect, useState } from "react";
import { getMe } from "../services/meService";
import {
  Box,
  Flex,
  Alert,
  AlertIcon,
  Avatar,
  HStack,
  Link,
  IconButton,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Spinner,
  Switch,
  useDisclosure,
  useColorModeValue,
  Stack,
  useColorMode,
  Image,
} from "@chakra-ui/react";
import { HamburgerIcon, CloseIcon, MoonIcon } from "@chakra-ui/icons";
import DataUpdateContext from "../context/DataUpdateContext";
import { useHistory } from "react-router";
import { Link as RouterLink } from "react-router-dom";

const Links = [
  { name: "Items", link: "/app/items" },
  { name: "Products", link: "/app/products" },
  { name: "Overlays", link: "/app/overlays" },
  { name: "Locations", link: "/app/locations" },
  { name: "Tags", link: "/app/tags" },
  { name: "Entities", link: "/app/entities" },
  { name: "Data types", link: "/app/datatypes" },
];

const NavLink = ({ children }) => (
  <Link
    as={RouterLink}
    to={children.link}
    px={2}
    py={1}
    rounded={"md"}
    _hover={{
      textDecoration: "none",
      bg: useColorModeValue("gray.200", "gray.700"),
    }}
  >
    {children.name}
  </Link>
);

function MeMenu() {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [me, setMe] = useState([]);

  const { lastUpdate, setLastUpdate } = useContext(DataUpdateContext);

  const { colorMode, toggleColorMode } = useColorMode();

  useEffect(() => {
    getMe().then(
      (data) => {
        setIsLoaded(true);
        setMe(data);
      },
      (err) => {
        setIsLoaded(true);
        setError(err);
      }
    );
  }, [lastUpdate]);

  if (error) {
    return (
      <Alert status="error">
        <AlertIcon />
        {error.message}
      </Alert>
    );
  } else if (!isLoaded) {
    return <Spinner />;
  } else {
    return (
      <Menu>
        <MenuButton
          as={Button}
          rounded={"full"}
          variant={"link"}
          cursor={"pointer"}
        >
          <Avatar size={"sm"} name={me.username} />
        </MenuButton>
        <MenuList>
          <MenuItem>
            {me.username}
          </MenuItem>
          <MenuItem onClick={toggleColorMode}>
            Swtich to {colorMode === "light" ? "Dark" : "Light"} Mode
          </MenuItem>
          <MenuItem
            onClick={() => {
              location.href = "/logout/";
            }}
          >
            Logout
          </MenuItem>
        </MenuList>
      </Menu>
    );
  }
}

export default function Navbar() {
  let history = useHistory();
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <>
      <Box
        borderBottomWidth={2}
        borderBottomColor={useColorModeValue("teal.500", "teal.200")}
        width="100vw"
        px={4}
      >
        <Flex h={16} alignItems={"center"} justifyContent={"space-between"}>
          <IconButton
            size={"md"}
            icon={isOpen ? <CloseIcon /> : <HamburgerIcon />}
            aria-label={"Open Menu"}
            display={{ md: !isOpen ? "none" : "inherit" }}
            onClick={isOpen ? onClose : onOpen}
          />
          <HStack spacing={8} alignItems={"center"}>
            <Box>
              <Image
                boxSize="50px"
                objectFit="cover"
                src="/assets/logo.png"
                alt="Logo"
              />
            </Box>
            <HStack
              as={"nav"}
              spacing={4}
              display={{ base: "none", md: "flex" }}
            >
              {Links.map((link, key) => (
                <NavLink key={key}>{link}</NavLink>
              ))}
            </HStack>
          </HStack>
          <Flex alignItems={"center"}>
            <MeMenu />
          </Flex>
        </Flex>

        {isOpen ? (
          <Box pb={4}>
            <Stack as={"nav"} spacing={4}>
              {Links.map((link) => (
                <NavLink key={link}>{link}</NavLink>
              ))}
            </Stack>
          </Box>
        ) : null}
      </Box>
    </>
  );
}
