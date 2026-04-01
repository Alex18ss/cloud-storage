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
} from "@chakra-ui/react";
import { useAuth } from "../contexts/AuthContext";
import { FiMail, FiLock, FiUser, FiCloud } from "react-icons/fi";

export function RegisterPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    if (!username || !email || !password || !confirmPassword) {
      setError("Заполните все поля");
      return;
    }

    if (password.length < 6) {
      setError("Пароль должен содержать минимум 6 символов");
      return;
    }

    if (password !== confirmPassword) {
      setError("Пароли не совпадают");
      return;
    }

    setLoading(true);
    try {
      await register({ username, email, password });
      navigate("/");
    } catch (err: unknown) {
      const axiosError = err as { response?: { data?: { detail?: string } } };
      setError(
        axiosError.response?.data?.detail ||
          "Ошибка регистрации. Попробуйте снова."
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
      {/* Декоративные круги */}
      <Box
        position="absolute"
        top="-100px"
        left="-100px"
        w="350px"
        h="350px"
        borderRadius="full"
        bg="rgba(108, 92, 231, 0.15)"
        filter="blur(80px)"
      />
      <Box
        position="absolute"
        bottom="-100px"
        right="-100px"
        w="400px"
        h="400px"
        borderRadius="full"
        bg="rgba(26, 140, 255, 0.12)"
        filter="blur(60px)"
      />

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
        <VStack gap={5}>
          {/* Logo */}
          <Flex
            align="center"
            justify="center"
            w="64px"
            h="64px"
            borderRadius="xl"
            bgGradient="to-br"
            gradientFrom="#6c5ce7"
            gradientTo="#1a8cff"
            fontSize="28px"
            color="white"
          >
            <FiCloud />
          </Flex>

          <VStack gap={1}>
            <Heading size="xl" color="white" fontWeight="700">
              Создать аккаунт
            </Heading>
            <Text color="whiteAlpha.600" fontSize="sm">
              Начните пользоваться облачным хранилищем
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

          {/* Name */}
          <Box w="full">
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
                border: "1px solid rgba(108, 92, 231, 0.5)",
                bg: "rgba(255, 255, 255, 0.08)",
              }}
            >
              <Box color="whiteAlpha.500" fontSize="lg">
                <FiUser />
              </Box>
              <Input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                color="white"
                _placeholder={{ color: "whiteAlpha.400" }}
                fontSize="sm"
                bg='transparent'
              border='none'
              _focusVisible={{ outline: 'none' }}
              />
            </Flex>
          </Box>

          {/* Email */}
          <Box w="full">
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
                border: "1px solid rgba(108, 92, 231, 0.5)",
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
          </Box>

          {/* Password */}
          <Box w="full">
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
                border: "1px solid rgba(108, 92, 231, 0.5)",
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
          </Box>

          {/* Confirm password */}
          <Box w="full">
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
                border: "1px solid rgba(108, 92, 231, 0.5)",
                bg: "rgba(255, 255, 255, 0.08)",
              }}
            >
              <Box color="whiteAlpha.500" fontSize="lg">
                <FiLock />
              </Box>
              <Input
                type="password"
                placeholder="Подтвердите пароль"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                color="white"
                _placeholder={{ color: "whiteAlpha.400" }}
                fontSize="sm"
                bg='transparent'
              border='none'
              _focusVisible={{ outline: 'none' }}
              />
            </Flex>
          </Box>

          <Button
            type="submit"
            w="full"
            h="52px"
            borderRadius="xl"
            bgGradient="to-r"
            gradientFrom="#6c5ce7"
            gradientTo="#1a8cff"
            color="white"
            fontWeight="600"
            fontSize="sm"
            loading={loading}
            _hover={{
              opacity: 0.9,
              transform: "translateY(-1px)",
              boxShadow: "0 4px 20px rgba(108, 92, 231, 0.4)",
            }}
            _active={{ transform: "translateY(0)" }}
            transition="all 0.2s"
          >
            Зарегистрироваться
          </Button>

          <Text color="whiteAlpha.500" fontSize="sm">
            Уже есть аккаунт?{" "}
            <Link
              asChild
              color="brand.400"
              _hover={{ color: "brand.300" }}
            >
              <RouterLink to="/login">Войти</RouterLink>
            </Link>
          </Text>
        </VStack>
      </Box>
    </Flex>
  );
}
