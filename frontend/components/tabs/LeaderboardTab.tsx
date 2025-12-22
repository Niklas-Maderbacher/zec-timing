"use client"

import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Trophy } from "lucide-react"

interface Props {
  raceCategories: string[]
  selectedCategory: string
  setSelectedCategory: (c: string) => void
  mockLeaderboardData: Record<string, any[]>
}

export default function LeaderboardTab({
  raceCategories,
  selectedCategory,
  setSelectedCategory,
  mockLeaderboardData,
}: Props) {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Race Leaderboard</h2>

        <Select
          value={selectedCategory}
          onValueChange={setSelectedCategory}
        >
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Select category" />
          </SelectTrigger>
          <SelectContent>
            {raceCategories.map((category) => (
              <SelectItem key={category} value={category}>
                {category}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Leaderboard */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="h-5 w-5" />
            <span>{selectedCategory} Standings</span>
          </CardTitle>
        </CardHeader>

        <CardContent>
          <div className="space-y-4">
            {(mockLeaderboardData[selectedCategory] || []).length === 0 && (
              <div className="text-sm text-muted-foreground">
                No leaderboard data available.
              </div>
            )}

            {(mockLeaderboardData[selectedCategory] || []).map(
              (entry) => (
                <div
                  key={entry.position}
                  className="flex items-center justify-between rounded-lg bg-slate-50 p-3"
                >
                  <div className="flex items-center gap-4">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">
                      {entry.position}
                    </div>

                    <div>
                      <div className="font-medium">
                        {entry.driver}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {entry.team}
                      </div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="font-mono font-medium">
                      {entry.bestTime}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {entry.points} pts
                    </div>
                  </div>
                </div>
              )
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
