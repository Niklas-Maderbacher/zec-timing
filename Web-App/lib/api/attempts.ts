import { authenticatedFetch } from "@/lib/auth"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL

export interface Attempt {
  id: number
  team_id: number
  driver_id: number
  challenge_id: number
  start_time: string
  end_time: string
  energy_used: number
  is_valid: boolean
  created_at: string
}

export interface AttemptUpdate {
  start_time?: string
  end_time?: string
  energy_used?: number
  is_valid?: boolean
}

export const attemptsApi = {
  async listAttempts(): Promise<Attempt[]> {
    const response = await authenticatedFetch(`${API_BASE_URL}/attempts/`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to fetch attempts' }))
      throw new Error(error.detail || 'Failed to fetch attempts')
    }
    return response.json()
  },

  async getAttemptById(id: number): Promise<Attempt> {
    const response = await authenticatedFetch(`${API_BASE_URL}/attempts/${id}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Attempt not found' }))
      throw new Error(error.detail || 'Attempt not found')
    }
    return response.json()
  },

  async getAttemptsForChallenge(challengeId: number): Promise<Attempt[]> {
    const response = await authenticatedFetch(`${API_BASE_URL}/attempts/challenges/${challengeId}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to fetch attempts' }))
      throw new Error(error.detail || 'Failed to fetch attempts')
    }
    return response.json()
  },

  async getFastestAttempt(challengeId: number): Promise<Attempt> {
    const response = await authenticatedFetch(`${API_BASE_URL}/attempts/fastest/${challengeId}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'No attempts found' }))
      throw new Error(error.detail || 'No attempts found')
    }
    return response.json()
  },

  async getFastestAttemptForTeam(challengeId: number, teamId: number): Promise<Attempt> {
    const response = await authenticatedFetch(
      `${API_BASE_URL}/attempts/fastest/per-team/?challenge_id=${challengeId}&team_id=${teamId}`
    )
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'No attempts found' }))
      throw new Error(error.detail || 'No attempts found')
    }
    return response.json()
  },

  async getLeastEnergyAttempt(challengeId: number): Promise<Attempt> {
    const response = await authenticatedFetch(`${API_BASE_URL}/attempts/least-energy/${challengeId}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'No attempts found' }))
      throw new Error(error.detail || 'No attempts found')
    }
    return response.json()
  },

  async getLeastEnergyAttemptForTeam(challengeId: number, teamId: number): Promise<Attempt> {
    const response = await authenticatedFetch(
      `${API_BASE_URL}/attempts/least-energy/per-team/?challenge_id=${challengeId}&team_id=${teamId}`
    )
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'No attempts found' }))
      throw new Error(error.detail || 'No attempts found')
    }
    return response.json()
  },

  async updateAttempt(id: number, data: AttemptUpdate): Promise<Attempt> {
    const response = await authenticatedFetch(`${API_BASE_URL}/attempts/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to update attempt' }))
      throw new Error(error.detail || 'Failed to update attempt')
    }
    return response.json()
  },

  async deleteAttempt(id: number): Promise<void> {
    const response = await authenticatedFetch(`${API_BASE_URL}/attempts/${id}`, {
      method: 'DELETE',
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to delete attempt' }))
      throw new Error(error.detail || 'Failed to delete attempt')
    }
  },
}