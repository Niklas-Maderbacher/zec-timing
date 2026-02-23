"use client"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import { Download, Loader2 } from "lucide-react"
import { toast } from "sonner"
import { leaderboardApi, TeamCategory } from "@/lib/api/leaderboard"
import { attemptsApi } from "@/lib/api/attempts"
import { challengesApi, type Challenge } from "@/lib/api/challenges"

const CATEGORY_LABELS: Record<TeamCategory, string> = {
  [TeamCategory.CLOSE_TO_SERIES]: "Close to Series",
  [TeamCategory.ADVANCED_CLASS]: "Advanced Class",
  [TeamCategory.PROFESSIONAL_CLASS]: "Professional Class",
}

export default function ExportTab() {
  const [challenges, setChallenges] = useState<Challenge[]>([])
  const [isLoadingChallenges, setIsLoadingChallenges] = useState(false)

  const [leaderboardChallenge, setLeaderboardChallenge] = useState<number | null>(null)
  const [leaderboardFormat, setLeaderboardFormat] = useState<"csv" | "xlsx">("csv")
  const [leaderboardCategory, setLeaderboardCategory] = useState<TeamCategory>(TeamCategory.ADVANCED_CLASS)
  const [isExportingLeaderboard, setIsExportingLeaderboard] = useState(false)

  const [attemptsChallenge, setAttemptsChallenge] = useState<number | null>(null)
  const [attemptsFormat, setAttemptsFormat] = useState<"csv" | "xlsx">("csv")
  const [attemptsCategory, setAttemptsCategory] = useState<string>("all")
  const [isExportingAttempts, setIsExportingAttempts] = useState(false)

  useEffect(() => {
    const loadChallenges = async () => {
      setIsLoadingChallenges(true)
      try {
        const data = await challengesApi.listChallenges()
        setChallenges(data)
        if (data.length > 0) {
          setLeaderboardChallenge(data[0].id)
          setAttemptsChallenge(data[0].id)
        }
      } catch {
        toast.error("Failed to load challenges")
      } finally {
        setIsLoadingChallenges(false)
      }
    }
    loadChallenges()
  }, [])

  const handleExportLeaderboard = async () => {
    if (!leaderboardChallenge) return toast.error("Select a challenge first")
    setIsExportingLeaderboard(true)
    try {
      await leaderboardApi.exportLeaderboard(leaderboardChallenge, leaderboardCategory, leaderboardFormat)
      toast.success("Leaderboard exported!")
    } catch (error: any) {
      toast.error(error.message || "Failed to export leaderboard")
    } finally {
      setIsExportingLeaderboard(false)
    }
  }

  const handleExportAttempts = async () => {
    if (!attemptsChallenge) return toast.error("Select a challenge first")
    setIsExportingAttempts(true)
    try {
      await attemptsApi.exportAttempts(
        attemptsChallenge,
        attemptsFormat,
        attemptsCategory === "all" ? undefined : attemptsCategory
      )
      toast.success("Attempts exported!")
    } catch (error: any) {
      toast.error(error.message || "Failed to export attempts")
    } finally {
      setIsExportingAttempts(false)
    }
  }

  const ChallengeSelect = ({
    value,
    onChange,
  }: {
    value: number | null
    onChange: (v: number) => void
  }) => (
    <div>
      <Label>Challenge</Label>
      <Select
        value={value?.toString()}
        onValueChange={(v) => onChange(parseInt(v))}
        disabled={isLoadingChallenges}
      >
        <SelectTrigger className="mt-2">
          <SelectValue placeholder={isLoadingChallenges ? "Loading..." : "Select a challenge"} />
        </SelectTrigger>
        <SelectContent>
          {challenges.map((c) => (
            <SelectItem key={c.id} value={c.id.toString()}>{c.name}</SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Data Export</h2>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Leaderboard Export</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            <ChallengeSelect value={leaderboardChallenge} onChange={setLeaderboardChallenge} />
            <div>
              <Label>Category</Label>
              <Select
                value={leaderboardCategory}
                onValueChange={(v) => setLeaderboardCategory(v as TeamCategory)}
              >
                <SelectTrigger className="mt-2"><SelectValue /></SelectTrigger>
                <SelectContent>
                  {Object.values(TeamCategory).map((cat) => (
                    <SelectItem key={cat} value={cat}>{CATEGORY_LABELS[cat]}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Format</Label>
              <Select
                value={leaderboardFormat}
                onValueChange={(v) => setLeaderboardFormat(v as "csv" | "xlsx")}
              >
                <SelectTrigger className="mt-2"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="csv">CSV</SelectItem>
                  <SelectItem value="xlsx">Excel</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button
              onClick={handleExportLeaderboard}
              disabled={isExportingLeaderboard || !leaderboardChallenge}
              className="w-full flex items-center gap-2"
            >
              {isExportingLeaderboard
                ? <><Loader2 className="h-4 w-4 animate-spin" />Exporting...</>
                : <><Download className="h-4 w-4" />Export Leaderboard</>
              }
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Attempts Export</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            <ChallengeSelect value={attemptsChallenge} onChange={setAttemptsChallenge} />
            <div>
              <Label>Category <span className="text-muted-foreground text-xs">(optional)</span></Label>
              <Select value={attemptsCategory} onValueChange={setAttemptsCategory}>
                <SelectTrigger className="mt-2"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All categories</SelectItem>
                  {Object.values(TeamCategory).map((cat) => (
                    <SelectItem key={cat} value={cat}>{CATEGORY_LABELS[cat]}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Format</Label>
              <Select
                value={attemptsFormat}
                onValueChange={(v) => setAttemptsFormat(v as "csv" | "xlsx")}
              >
                <SelectTrigger className="mt-2"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="csv">CSV</SelectItem>
                  <SelectItem value="xlsx">Excel</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button
              onClick={handleExportAttempts}
              disabled={isExportingAttempts || !attemptsChallenge}
              className="w-full flex items-center gap-2"
            >
              {isExportingAttempts
                ? <><Loader2 className="h-4 w-4 animate-spin" />Exporting...</>
                : <><Download className="h-4 w-4" />Export Attempts</>
              }
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}