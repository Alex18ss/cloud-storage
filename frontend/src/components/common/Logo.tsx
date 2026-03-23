import { Flex } from "@chakra-ui/react"
import { FiCloud } from "react-icons/fi"

export const Logo = () => {
    return (
        <Flex
            align="center"
            justify="center"
            w="64px"
            h="64px"
            borderRadius="xl"
            bgGradient="to-br"
            gradientFrom="#1a8cff"
            gradientTo="#6c5ce7"
            fontSize="28px"
            color="white"
            alignSelf="center"
        >
            <FiCloud />
        </Flex>
    )
}