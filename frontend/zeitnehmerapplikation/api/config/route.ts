import { NextResponse } from "next/server";

export async function GET() {
    return NextResponse.json({
        serverApiUrl: process.env.NEXT_PUBLIC_DESKTOP_APP_API_URL,
        mqttWorkerApiUrl: process.env.NEXT_PUBLIC_MQTT_WORKER_API_URL,
        apiKey: process.env.NEXT_PUBLIC_API_KEY,
    });
}
