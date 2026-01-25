import { authenticatedFetch } from "@/lib/auth"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost'

export interface Challenge {
  id: number
  name: string
  max_attempts?: number | null
  esp_mac_start1?: string | null
  esp_mac_start2?: string | null
  esp_mac_finish1?: string | null
  esp_mac_finish2?: string | null
  created_at?: string | null
}

export interface ChallengeUpdate {
  name?: string
  max_attempts?: number | null
  esp_mac_start1?: string | null
  esp_mac_start2?: string | null
  esp_mac_finish1?: string | null
  esp_mac_finish2?: string | null
}

export const challengesApi = {
  async listChallenges(): Promise<Challenge[]> {
    const response = await authenticatedFetch(`${API_BASE_URL}/challenges/`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to fetch challenges' }))
      throw new Error(error.detail || 'Failed to fetch challenges')
    }
    return response.json()
  },

  async getChallengeById(id: number): Promise<Challenge> {
    const response = await authenticatedFetch(`${API_BASE_URL}/challenges/${id}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Challenge not found' }))
      throw new Error(error.detail || 'Challenge not found')
    }
    return response.json()
  },

  async getChallengeByName(name: string): Promise<Challenge> {
    const response = await authenticatedFetch(`${API_BASE_URL}/challenges/name/${encodeURIComponent(name)}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Challenge not found' }))
      throw new Error(error.detail || 'Challenge not found')
    }
    return response.json()
  },

  async updateChallenge(id: number, data: ChallengeUpdate): Promise<Challenge> {
    const response = await authenticatedFetch(`${API_BASE_URL}/challenges/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to update challenge' }))
      throw new Error(error.detail || 'Failed to update challenge')
    }
    return response.json()
  },
}