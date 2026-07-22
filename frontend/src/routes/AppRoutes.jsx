import { Routes, Route, Navigate } from "react-router-dom";

import Login from "../pages/Login/Login";
import Signup from "../pages/Signup/Signup";
import Dashboard from "../pages/Dashboard/Dashboard";
import Archived from "../pages/Archived/Archived";
import RecentlyUpdated from "../pages/RecentlyUpdated/RecentlyUpdated";
import Profile from "../pages/Profile/Profile";
import NotFound from "../pages/NotFound/NotFound";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />

      <Route path="/login" element={<Login />} />

      <Route path="/signup" element={<Signup />} />

      <Route path="/dashboard" element={<Dashboard />} />

      <Route path="/archived" element={<Archived />} />

      <Route
        path="/recently-updated"
        element={<RecentlyUpdated />}
      />

      <Route path="/profile" element={<Profile />} />

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default AppRoutes;