import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;

export const API_URL = process.env.NEXT_PUBLIC_DESKTOP_APP_API_URL!;

