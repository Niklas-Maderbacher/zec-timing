import { authenticatedFetch, publicFetch } from "@/lib/auth"
import { triggerDownload } from "@/lib/utils/export"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL

export interface ScoreResponse {
  id: number
  attempt_id?: number | null
  challenge_id?: number | null
  value?: number | null
  created_at: string
}

export interface TeamResponse {
  id: number
  name: string
  category: string
  vehicle_weight?: number | null
  rfid_identifier?: string | null
  created_at?: string | null
}

export interface LeaderboardEntry {
  score: ScoreResponse
  team: TeamResponse
}

export enum TeamCategory {
  CLOSE_TO_SERIES = "close_to_series",
  ADVANCED_CLASS = "advanced_class",
  PROFESSIONAL_CLASS = "professional_class",
}

export const leaderboardApi = {
  async getLeaderboard(challengeId: number, category: TeamCategory): Promise<LeaderboardEntry[]> {
    const response = await publicFetch(
      `${API_BASE_URL}/leaderboard/${challengeId}/category/${category}`
    )
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Failed to fetch leaderboard" }))
      throw new Error(error.detail || "Failed to fetch leaderboard")
    }
    return response.json()
  },

  async exportLeaderboard(
    challengeId: number,
    category: TeamCategory,
    format: "csv" | "xlsx"
  ): Promise<void> {
    const response = await authenticatedFetch(
      `${API_BASE_URL}/export/leaderboard/${challengeId}/category/${category}?format=${format}`
    )
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Failed to export leaderboard" }))
      throw new Error(error.detail || "Failed to export leaderboard")
    }
    const blob = await response.blob()
    triggerDownload(blob, `leaderboard_challenge${challengeId}_${category}.${format}`)
  },
}