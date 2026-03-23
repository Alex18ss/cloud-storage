import { useState, type FormEvent } from "react";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Heading,
  Input,
  Text,
  VStack,
  Link,
  Flex,
  Stack,
  HStack,
} from "@chakra-ui/react";
import { useAuth } from "../contexts/AuthContext";
import { FiMail, FiLock, FiCloud } from "react-icons/fi";
import { Logo } from "../components/common/Logo";

export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    if (!email || !password) {
      setError("Заполните все поля");
      return;
    }

    setLoading(true);
    try {
      await login({ email, password });
      navigate("/");
    } catch (err: unknown) {
      const axiosError = err as { response?: { data?: { detail?: string } } };
      setError(
        axiosError.response?.data?.detail || "Ошибка входа. Попробуйте снова."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Flex
      minH="100vh"
      align="center"
      justify="center"
      bgGradient="to-br"
      gradientFrom="#0f0c29"
      gradientVia="#302b63"
      gradientTo="#24243e"
      position="relative"
      overflow="hidden"
    >
      <Box
        as="form"
        onSubmit={handleSubmit}
        w="full"
        maxW="440px"
        mx={4}
        p={10}
        borderRadius="2xl"
        bg="rgba(255, 255, 255, 0.06)"
        backdropFilter="blur(24px)"
        border="1px solid rgba(255, 255, 255, 0.1)"
        boxShadow="0 8px 32px rgba(0, 0, 0, 0.4)"
      >
        <Stack gap={6} alignItems='stretch'>
          <Logo />
          <VStack gap={1}>
            <Heading size="xl" color="white" fontWeight="700">
              Добро пожаловать
            </Heading>
            <Text color="whiteAlpha.600" fontSize="sm">
              Войдите в ваше облачное хранилище
            </Text>
          </VStack>

          {error && (
            <Box
              w="full"
              p={3}
              borderRadius="lg"
              bg="rgba(255, 69, 58, 0.15)"
              border="1px solid rgba(255, 69, 58, 0.3)"
            >
              <Text color="#ff6b6b" fontSize="sm" textAlign="center">
                {error}
              </Text>
            </Box>
          )}
          <Flex
            align="center"
            gap={3}
            px={4}
            h="52px"
            borderRadius="xl"
            bg="rgba(255, 255, 255, 0.06)"
            border="1px solid rgba(255, 255, 255, 0.08)"
            transition="all 0.2s"
            _focusWithin={{
              border: "1px solid rgba(26, 140, 255, 0.5)",
              bg: "rgba(255, 255, 255, 0.08)",
            }}
          >
            <Box color="whiteAlpha.500" fontSize="lg">
              <FiMail />
            </Box>
            <Input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              color="white"
              _placeholder={{ color: "whiteAlpha.400" }}
              fontSize="sm"
              bg='transparent'
              border='none'
              _focusVisible={{ outline: 'none' }}
            />
          </Flex>
          <Flex
            align="center"
            gap={3}
            px={4}
            h="52px"
            borderRadius="xl"
            bg="rgba(255, 255, 255, 0.06)"
            border="1px solid rgba(255, 255, 255, 0.08)"
            transition="all 0.2s"
            _focusWithin={{
              border: "1px solid rgba(26, 140, 255, 0.5)",
              bg: "rgba(255, 255, 255, 0.08)",
            }}
          >
            <Box color="whiteAlpha.500" fontSize="lg">
              <FiLock />
            </Box>
            <Input
              type="password"
              placeholder="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              color="white"
              _placeholder={{ color: "whiteAlpha.400" }}
              fontSize="sm"
              bg='transparent'
              border='none'
              _focusVisible={{ outline: 'none' }}
            />
          </Flex>

          <Button
            type="submit"
            w="full"
            h="52px"
            borderRadius="xl"
            bgGradient="to-r"
            gradientFrom="#1a8cff"
            gradientTo="#6c5ce7"
            color="white"
            fontWeight="600"
            fontSize="sm"
            loading={loading}
            _hover={{
              opacity: 0.9,
              transform: "translateY(-1px)",
              boxShadow: "0 4px 20px rgba(26, 140, 255, 0.4)",
            }}
            _active={{ transform: "translateY(0)" }}
            transition="all 0.2s"
          >
            Войти
          </Button>
          <HStack gap='8px'>
            <Text color="whiteAlpha.500" fontSize="sm">
              Нет аккаунта?
            </Text>
            <Link
              asChild
              color="brand.400"
              _hover={{ color: "brand.300" }}
              fontSize="sm"
            >
              <RouterLink to="/register">
                Зарегистрироваться
              </RouterLink>
            </Link>
          </HStack>
        </Stack>
      </Box>
    </Flex >
  );
}
