'use client'

import React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import axios from "axios"
import { SERVER_API_URL, API_KEY } from "@/next.config"
import { Attempt, Penalty } from "@/components/types"

interface AttemptResultCardProps {
    selectedTeam: { id: number } | null
    selectedDriver: { id: number } | null
    selectedChallenge: { id: number } | null
    medianStartTimestamp: string
    medianEndTimestamp: string
    manualAttemptTime: string | null
    energyConsumption: number
    selectedPenalty: Penalty | null
    penaltyCount: number
}

export function AttemptResultCard({
    selectedTeam,
    selectedDriver,
    selectedChallenge,
    medianStartTimestamp,
    medianEndTimestamp,
    manualAttemptTime,
    energyConsumption,
    selectedPenalty,
    penaltyCount,
}: AttemptResultCardProps) {

    const calcAttemptTime = (): string => {
        let attemptMs = 0

        if (manualAttemptTime) {
            attemptMs = Number(manualAttemptTime)
        } else if (medianStartTimestamp && medianEndTimestamp) {
            attemptMs =
                new Date(medianEndTimestamp).getTime() -
                new Date(medianStartTimestamp).getTime()
        }

        const penaltyMs =
            (penaltyCount ?? 0) * (selectedPenalty?.amount ?? 0) * 1000

        attemptMs += penaltyMs

        const hours = Math.floor(attemptMs / 3600000)
        const minutes = Math.floor((attemptMs % 3600000) / 60000)
        const seconds = Math.floor((attemptMs % 60000) / 1000)
        const milliseconds = attemptMs % 1000

        return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}:${String(milliseconds).padStart(4, "0")}`
    }

    const toBackendDateTime = (isoString: string): string => {
        const date = new Date(isoString)
        return date
            .toISOString()              // 2024-01-01T10:11:00.123Z
            .replace("Z", "")           // remove Z
            .padEnd(26, "0")            // ensure microseconds
    }

    const createAttempt = () => {
        if (!selectedTeam?.id) return alert("Please select a team!")
        if (!selectedDriver?.id) return alert("Please select a driver!")
        if (!selectedChallenge?.id) return alert("Please select a challenge!")
        if (!energyConsumption || energyConsumption <= 0) return alert("Please enter energy consumption!")
        if (!selectedPenalty?.id) return alert("Please select a penalty!")

        let startTime: string
        let endTime: string

        if (manualAttemptTime) {
            const base = new Date(0) // 1970-01-01T00:00:00.000Z
            startTime = base.toISOString()
            endTime = new Date(base.getTime() + Number(manualAttemptTime)).toISOString()
        } else {
            if (!medianStartTimestamp || !medianEndTimestamp) {
                return alert("Please provide start and end timestamps!")
            }

            startTime = medianStartTimestamp
            endTime = medianEndTimestamp
        }

        const attempt: Attempt = {
            team_id: selectedTeam.id,
            driver_id: selectedDriver.id,
            challenge_id: selectedChallenge.id,
            start_time: toBackendDateTime(startTime),
            end_time: toBackendDateTime(endTime),
            energy_used: energyConsumption,
            penalty_id: selectedPenalty.id,
            penalty_count: penaltyCount ?? 0,
        }

        axios.post(`${SERVER_API_URL}/attempts/`, attempt, {
            headers: { "x-api-key": API_KEY },
        })
            .then(() => alert("Attempt submitted successfully!"))
            .catch((error) => {
                console.error("Failed to submit attempt", error)
                alert("Failed to submit attempt!")
            })
    }

    return (
        <Card className="md:col-span-1">
            <CardHeader>
                <CardTitle>Result</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
                <p>Result = {calcAttemptTime()}</p>
                <Button variant="outline" onClick={createAttempt}>
                    Submit
                </Button>
            </CardContent>
        </Card>
    )
}