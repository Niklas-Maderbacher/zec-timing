export async function GET() {
    return Response.json({
        desktopAppApiUrl: process.env.NEXT_PUBLIC_DESKTOP_APP_API_URL,
        mqttWorkerApiUrl: process.env.NEXT_PUBLIC_MQTT_WORKER_API_URL,
    });
}
