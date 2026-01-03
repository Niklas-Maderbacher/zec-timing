import path from "path";
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Empty turbopack config to acknowledge you want to use it
  turbopack: {},
  
  // Keep your webpack config but it won't be used with Turbopack
  // This is just for the build command
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname, 'src'),
    };
    return config;
  },
};

export default nextConfig;