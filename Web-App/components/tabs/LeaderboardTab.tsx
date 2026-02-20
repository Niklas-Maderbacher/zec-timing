"use client"
import { useState, useEffect } from "react"
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
import { Trophy, Loader2 } from "lucide-react"
import { leaderboardApi, type LeaderboardEntry, TeamCategory } from "@/lib/api/leaderboard"
import { challengesApi, type Challenge } from "@/lib/api/challenges"
import { toast } from "sonner"

const CATEGORY_LABELS: Record<TeamCategory, string> = {
  [TeamCategory.CLOSE_TO_SERIES]: "Close to Series",
  [TeamCategory.ADVANCED_CLASS]: "Advanced Class",
  [TeamCategory.PROFESSIONAL_CLASS]: "Professional Class",
}

const CATEGORIES = Object.values(TeamCategory)

export default function LeaderboardTab() {
  const [challenges, setChallenges] = useState<Challenge[]>([])
  const [selectedChallenge, setSelectedChallenge] = useState<number | null>(null)
  const [leaderboards, setLeaderboards] = useState<Record<TeamCategory, LeaderboardEntry[]>>({
    [TeamCategory.CLOSE_TO_SERIES]: [],
    [TeamCategory.ADVANCED_CLASS]: [],
    [TeamCategory.PROFESSIONAL_CLASS]: [],
  })
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingChallenges, setIsLoadingChallenges] = useState(false)

  useEffect(() => {
    loadChallenges()
  }, [])

  useEffect(() => {
    if (selectedChallenge) {
      loadAllLeaderboards()
    }
  }, [selectedChallenge])

  const loadChallenges = async () => {
    setIsLoadingChallenges(true)
    try {
      const data = await challengesApi.listChallenges()
      setChallenges(data)
      if (data.length > 0 && !selectedChallenge) {
        setSelectedChallenge(data[0].id)
      }
    } catch (error: any) {
      console.error("Failed to load challenges:", error)
    } finally {
      setIsLoadingChallenges(false)
    }
  }

  const loadAllLeaderboards = async () => {
    if (!selectedChallenge) return

    setIsLoading(true)
    try {
      const results = await Promise.all(
        CATEGORIES.map(async (category) => {
          try {
            const data = await leaderboardApi.getLeaderboard(selectedChallenge, category)
            return { category, data }
          } catch (error) {
            console.error(`Failed to load ${category}:`, error)
            return { category, data: [] }
          }
        })
      )

      const newLeaderboards = results.reduce((acc, { category, data }) => {
        acc[category] = data
        return acc
      }, {} as Record<TeamCategory, LeaderboardEntry[]>)

      setLeaderboards(newLeaderboards)
    } catch (error: any) {
      console.error("Failed to load leaderboards:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const getPositionColor = (position: number) => {
    switch (position) {
      case 1:
        return "bg-yellow-500 text-white"
      case 2:
        return "bg-gray-400 text-white"
      case 3:
        return "bg-orange-600 text-white"
      default:
        return "bg-blue-600 text-white"
    }
  }

  const renderLeaderboard = (category: TeamCategory, entries: LeaderboardEntry[]) => (
    <Card key={category}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Trophy className="h-5 w-5" />
          <span>{CATEGORY_LABELS[category]}</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <div className="space-y-3">
            {entries.length === 0 && (
              <div className="text-sm text-muted-foreground text-center py-8">
                No attempts in this category.
              </div>
            )}
            {entries.map((entry, index) => {
              const position = index + 1
              return (
                <div
                  key={entry.score.id}
                  className="flex items-center justify-between rounded-lg bg-slate-50 p-3 hover:bg-slate-100 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div
                      className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold ${getPositionColor(position)}`}
                    >
                      {position}
                    </div>
                    <div>
                      <div className="font-medium">
                        {entry.team.name}
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-mono font-medium">
                      {parseFloat(entry.score.value!.toFixed(3))}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </CardContent>
    </Card>
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Leaderboard</h2>
        <Select
          value={selectedChallenge?.toString()}
          onValueChange={(value) => setSelectedChallenge(parseInt(value))}
          disabled={isLoadingChallenges}
        >
          <SelectTrigger className="w-64">
            <SelectValue placeholder="Select challenge" />
          </SelectTrigger>
          <SelectContent>
            {challenges.map((challenge) => (
              <SelectItem key={challenge.id} value={challenge.id.toString()}>
                {challenge.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-3">
        {CATEGORIES.map((category) => 
          renderLeaderboard(category, leaderboards[category])
        )}
      </div>
    </div>
  )
}
