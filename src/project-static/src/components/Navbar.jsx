import React from "react";
import {
  Box,
  Flex,
  Avatar,
  HStack,
  Link,
  IconButton,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Switch,
  useDisclosure,
  useColorModeValue,
  Stack,
  useColorMode,
  Image,
} from "@chakra-ui/react";
import { HamburgerIcon, CloseIcon, MoonIcon } from "@chakra-ui/icons";
import { useHistory } from "react-router";
import { Link as RouterLink } from "react-router-dom";
import { authenticationService } from "../services/authenticationService";

const Links = [
  { name: "Items", link: "/items" },
  { name: "Products", link: "/products" },
  { name: "Overlays", link: "/overlays" },
  { name: "Locations", link: "/locations" },
  { name: "Tags", link: "/tags" },
  { name: "Entities", link: "/entities" },
  { name: "Data types", link: "/datatypes" },
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

function logout(history) {
  authenticationService.logout();
  history.push("/login");
}

export default function Navbar() {
  let history = useHistory();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { colorMode, toggleColorMode } = useColorMode();

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
                alt="Segun Adebayo"
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
            <Menu>
              <MenuButton
                as={Button}
                rounded={"full"}
                variant={"link"}
                cursor={"pointer"}
              >
                <Avatar size={"sm"} />
              </MenuButton>
              <MenuList>
                <MenuItem onClick={toggleColorMode}>
                  Swtich to {colorMode === "light" ? "Dark" : "Light"} Mode
                </MenuItem>
                <MenuItem
                  onClick={() => {
                    logout(history);
                  }}
                >
                  Logout
                </MenuItem>
              </MenuList>
            </Menu>
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
