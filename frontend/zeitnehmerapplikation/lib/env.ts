export interface AppConfig {
    serverApiUrl: string;
    mqttWorkerApiUrl: string;
    apiKey: string;
}

let config: AppConfig | null = null;

export async function getConfig(): Promise<AppConfig> {
    if (config) {
        return config;
    }

    const response = await fetch("/api/config");

    if (!response.ok) {
        throw new Error("Failed to load application configuration");
    }

    config = await response.json();

    return config;
}
