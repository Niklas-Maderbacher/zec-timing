// lib/config.ts
export function getApiBaseUrl(): string {
    if (typeof window === "undefined") {
        return "";
    }

    return window.__ENV__?.API_URL ?? "";
}