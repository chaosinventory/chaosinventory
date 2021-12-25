import { useToast } from "@chakra-ui/react";

const defaultToast = {
  position: "top",
  duration: 9000,
  isClosable: true,
  variant: "solid",
};

export const useCiToast = () => {
  const toast = useToast({
    ...defaultToast,
  });

  return toast;
};
