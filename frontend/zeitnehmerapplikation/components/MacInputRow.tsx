'use client'

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import React, { Dispatch, SetStateAction } from "react"

interface MacInputRowProps {
    label: string
    value: string
    placeholder?: string
    onChange: (newValue: string) => void
    onUpdate: () => void
}

export function MacInputRow({ label, value, placeholder, onChange, onUpdate }: MacInputRowProps) {
    return (
        <div className="flex items-center gap-2 mt-4">
            <Input
                aria-label={`${label} ESP32 MAC`}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                placeholder={placeholder ?? "ESP32 MAC"}
            />
            <Button onClick={onUpdate}>{label}</Button>
        </div>
    )
}
