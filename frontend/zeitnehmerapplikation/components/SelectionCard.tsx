'use client'

import { useMemo, useState } from "react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuTrigger,
    DropdownMenuRadioGroup,
    DropdownMenuRadioItem,
} from "@/components/ui/dropdown-menu"

import { Input } from "@/components/ui/input"

import { ChevronDown } from "lucide-react"

interface SelectionCardProps<T extends { id: number }> {
    title: string
    items: T[]
    selectedItem: T | null
    onSelect: (item: T | null) => void

    getDisplayName?: (item: T) => string

    // new
    searchable?: boolean
}

export function SelectionCard<T extends { id: number }>({
    title,
    items,
    selectedItem,
    onSelect,
    getDisplayName = (item) => (item as any).name || String(item.id),
    searchable = false,
}: SelectionCardProps<T>) {
    const [search, setSearch] = useState("")

    const filteredItems = useMemo(() => {
        if (!searchable || !search.trim()) return items

        return items.filter((item) =>
            getDisplayName(item)
                .toLowerCase()
                .includes(search.toLowerCase())
        )
    }, [items, search, searchable, getDisplayName])

    return (
        <Card>
            <CardHeader>
                <CardTitle>{title}</CardTitle>
            </CardHeader>

            <CardContent className="space-y-4">
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button
                            variant="outline"
                            className="w-full flex items-center justify-between"
                        >
                            {selectedItem
                                ? getDisplayName(selectedItem)
                                : `Select ${title}`}

                            <ChevronDown className="w-4 h-4" />
                        </Button>
                    </DropdownMenuTrigger>

                    <DropdownMenuContent className="w-64">
                        {searchable && (
                            <div className="p-2">
                                <Input
                                    placeholder={`Search ${title}...`}
                                    value={search}
                                    onChange={(e) =>
                                        setSearch(e.target.value)
                                    }
                                    onKeyDown={(e) => e.stopPropagation()}
                                />
                            </div>
                        )}

                        <DropdownMenuRadioGroup
                            value={selectedItem?.id.toString() || ""}
                            onValueChange={(value) => {
                                const item =
                                    items.find(
                                        (i) =>
                                            i.id.toString() === value
                                    ) || null

                                onSelect(item)
                            }}
                        >
                            {filteredItems.length > 0 ? (
                                filteredItems.map((item) => (
                                    <DropdownMenuRadioItem
                                        key={item.id}
                                        value={item.id.toString()}
                                    >
                                        {getDisplayName(item)}
                                    </DropdownMenuRadioItem>
                                ))
                            ) : (
                                <div className="px-2 py-1 text-sm text-muted-foreground">
                                    No results
                                </div>
                            )}
                        </DropdownMenuRadioGroup>
                    </DropdownMenuContent>
                </DropdownMenu>
            </CardContent>
        </Card>
    )
}