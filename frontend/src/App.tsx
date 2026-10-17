import { RouterProvider, createBrowserRouter } from "react-router-dom";

import HomePage from "./app/dashboard/page.tsx"
const router = createBrowserRouter([
  {
    children: [
      { path: "", element: <HomePage /> },

    ]
  }])


export default function App() {
  return <RouterProvider router={router} />;
}