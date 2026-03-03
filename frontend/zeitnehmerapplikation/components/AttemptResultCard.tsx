'use client'

import React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import axios from "axios"
import { SERVER_API_URL, API_KEY } from "@/lib/env"
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
    onSubmitSuccess?: () => void  // Add callback prop
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
    onSubmitSuccess,  // Destructure callback
}: AttemptResultCardProps) {

    const calcAttemptTime = (): string => {
        let attemptMs = 0

        if (manualAttemptTime) {
            // manualAttemptTime is now in "HH:MM:SS" format
            attemptMs = durationToMs(manualAttemptTime)
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

        return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}:${String(milliseconds).padStart(3, "0")}`
    }

    function durationToMs(time: string): number {
        const parts = time.split(":").map(Number)

        if (parts.length === 2) {
            const [mm, ss] = parts
            return (mm * 60 + ss) * 1000
        }

        if (parts.length === 3) {
            const [hh, mm, ss] = parts
            return (hh * 3600 + mm * 60 + ss) * 1000
        }

        throw new Error("Invalid time format")
    }


    const toBackendDateTime = (isoString: string): string => {
        const date = new Date(isoString)

        const year = date.getFullYear()
        const month = date.getMonth() + 1 // months in js start with 0
        const day = date.getDate()
        const hours = date.getHours()
        const minutes = date.getMinutes()
        const seconds = date.getSeconds()
        const milliseconds = date.getMilliseconds()

        return `${year.toString().padStart(4, "0")}-` +
            `${month.toString().padStart(2, "0")}-` +
            `${day.toString().padStart(2, "0")}T` +
            `${hours.toString().padStart(2, "0")}:` +
            `${minutes.toString().padStart(2, "0")}:` +
            `${seconds.toString().padStart(2, "0")}.` +
            `${(milliseconds * 1000).toString().padStart(6, "0")}`

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
            endTime = new Date(base.getTime() + durationToMs(manualAttemptTime)).toISOString()

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
            penalty_type: selectedPenalty.id,
            penalty_count: penaltyCount ?? 0,
        }

        axios.post(`${SERVER_API_URL}/attempts/`, attempt, {
            headers: { "x-api-key": API_KEY },
        })
            .then(() => {
                alert("Attempt submitted successfully!")
                // Call the reset callback if provided
                if (onSubmitSuccess) {
                    onSubmitSuccess()
                }
            })
            .catch((error) => {
                console.error("Failed to submit attempt! This is probably because the team already made 3 attempts", error)
                alert("Failed to submit attempt! This is probably because the team already made 3 attempts")
            })
    }

    return (
        <Card className="md:col-span-1">
            <CardHeader>
                <CardTitle>Result</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
                <p>Result = {calcAttemptTime()}</p>
                <p>Start time: {medianStartTimestamp}</p>
                <p>End time: {medianEndTimestamp}</p>
                <Button variant="outline" onClick={createAttempt}>
                    Submit
                </Button>
            </CardContent>
        </Card>
    )
}