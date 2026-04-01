import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Heading,
  Text,
  VStack,
  Flex,
  HStack,
} from "@chakra-ui/react";
import { useAuth } from "../contexts/AuthContext";
import {
  FiCloud,
  FiLogOut,
  FiFolder,
  FiUploadCloud,
  FiShare2,
} from "react-icons/fi";

export function DashboardPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const features = [
    {
      icon: <FiFolder />,
      title: "Мои файлы",
      desc: "Управляйте файлами",
      color: "#1a8cff",
    },
    {
      icon: <FiUploadCloud />,
      title: "Загрузить",
      desc: "Добавить новые файлы",
      color: "#6c5ce7",
    },
    {
      icon: <FiShare2 />,
      title: "Общий доступ",
      desc: "Поделиться файлами",
      color: "#00b894",
    },
  ];

  return (
    <Flex
      minH="100vh"
      direction="column"
      bgGradient="to-br"
      gradientFrom="#0f0c29"
      gradientVia="#302b63"
      gradientTo="#24243e"
      position="relative"
      overflow="hidden"
    >
      {/* Фоновые декоративные элементы */}
      <Box
        position="absolute"
        top="10%"
        right="-5%"
        w="500px"
        h="500px"
        borderRadius="full"
        bg="rgba(26, 140, 255, 0.08)"
        filter="blur(100px)"
      />
      <Box
        position="absolute"
        bottom="10%"
        left="-5%"
        w="400px"
        h="400px"
        borderRadius="full"
        bg="rgba(108, 92, 231, 0.08)"
        filter="blur(80px)"
      />

      {/* Header */}
      <Flex
        justify="space-between"
        align="center"
        px={8}
        py={4}
        borderBottom="1px solid rgba(255, 255, 255, 0.06)"
        backdropFilter="blur(12px)"
        position="relative"
        zIndex={10}
      >
        <HStack gap={3}>
          <Flex
            align="center"
            justify="center"
            w="40px"
            h="40px"
            borderRadius="lg"
            bgGradient="to-br"
            gradientFrom="#1a8cff"
            gradientTo="#6c5ce7"
            fontSize="18px"
            color="white"
          >
            <FiCloud />
          </Flex>
          <Heading size="md" color="white" fontWeight="600">
            Cloud Storage
          </Heading>
        </HStack>

        <HStack gap={4}>
          <Text color="whiteAlpha.700" fontSize="sm">
            {user?.username || user?.email}
          </Text>
          <Button
            onClick={handleLogout}
            size="sm"
            variant="ghost"
            color="whiteAlpha.700"
            _hover={{ color: "white", bg: "rgba(255,255,255,0.08)" }}
            borderRadius="lg"
          >
            <FiLogOut />
            <Text ml={2} display={{ base: "none", md: "inline" }}>
              Выйти
            </Text>
          </Button>
        </HStack>
      </Flex>

      {/* Main content */}
      <Flex
        flex={1}
        align="center"
        justify="center"
        px={8}
        position="relative"
        zIndex={10}
      >
        <VStack gap={10} maxW="700px" w="full">
          <VStack gap={3}>
            <Heading
              size="2xl"
              color="white"
              fontWeight="700"
              textAlign="center"
            >
              Добро пожаловать{user?.username ? `, ${user.username}` : ""}! 👋
            </Heading>
            <Text
              color="whiteAlpha.600"
              fontSize="lg"
              textAlign="center"
              maxW="500px"
            >
              Вы успешно авторизованы. Ваше облачное хранилище готово к работе.
            </Text>
          </VStack>

          {/* Feature cards */}
          <Flex
            gap={5}
            wrap="wrap"
            justify="center"
            w="full"
          >
            {features.map((feature) => (
              <Box
                key={feature.title}
                p={6}
                borderRadius="2xl"
                bg="rgba(255, 255, 255, 0.05)"
                backdropFilter="blur(16px)"
                border="1px solid rgba(255, 255, 255, 0.08)"
                minW="200px"
                flex="1"
                cursor="pointer"
                transition="all 0.3s"
                _hover={{
                  bg: "rgba(255, 255, 255, 0.08)",
                  transform: "translateY(-4px)",
                  boxShadow: `0 8px 30px rgba(0, 0, 0, 0.3)`,
                  border: `1px solid ${feature.color}33`,
                }}
              >
                <VStack align="start" gap={3}>
                  <Flex
                    align="center"
                    justify="center"
                    w="48px"
                    h="48px"
                    borderRadius="xl"
                    bg={`${feature.color}1a`}
                    color={feature.color}
                    fontSize="22px"
                  >
                    {feature.icon}
                  </Flex>
                  <Box>
                    <Text color="white" fontWeight="600" fontSize="md">
                      {feature.title}
                    </Text>
                    <Text color="whiteAlpha.500" fontSize="sm" mt={1}>
                      {feature.desc}
                    </Text>
                  </Box>
                </VStack>
              </Box>
            ))}
          </Flex>
        </VStack>
      </Flex>
    </Flex>
  );
}
