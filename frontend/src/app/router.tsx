import {createBrowserRouter, Navigate} from "react-router-dom";
import {ProtectedRoute} from "../components/ProtectedRoute.tsx";
import {DashboardPage} from "../pages/DashboardPage.tsx";
import {LoginPage} from "../pages/LoginPage.tsx";
import {RegisterPage} from "../pages/RegisterPage.tsx";

export const router = createBrowserRouter([
    {
        path: "/",
        element: (<ProtectedRoute>
        <DashboardPage />
    </ProtectedRoute>)
},
    {
    path: '/login',
    element: <LoginPage />,
},
    {
        path: '/register',
        element: <RegisterPage />
    },
    {
        path: '*',
        element: <Navigate to="/" replace />,
    }
])