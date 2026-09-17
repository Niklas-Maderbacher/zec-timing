// tests/TestTimestampSelector.tsx

"use client"

import { useState } from "react"
import { TimestampSelector } from "@/components/TimestampSelector"

export function TestTimestampSelector() {
    const [selected, setSelected] = useState<string[] | null>([])

    const timestamps = [
        "2026-01-01T00:00:01.000Z",
        "2026-01-01T00:00:02.000Z",
        "2026-01-01T00:00:03.000Z",
    ]

    return (
        <TimestampSelector
            label="Start timestamp"
            timestamps={timestamps}
            selectedTimestamps={selected ?? []}
            setSelectedTimestamps={setSelected}
        />
    )
}