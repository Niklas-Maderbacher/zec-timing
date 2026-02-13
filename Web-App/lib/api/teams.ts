import { authenticatedFetch } from "@/lib/auth"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL

export enum TeamCategory {
  CLOSE_TO_SERIES = "close_to_series",
  ADVANCED_CLASS = "advanced_class",
  PROFESSIONAL_CLASS = "professional_class"
}

export interface Team {
  id: number
  category: TeamCategory
  name: string
  mean_power: number
  vehicle_weight: number
  rfid_identifier: string
  created_at: string
}

export interface TeamCreate {
  category: TeamCategory
  name: string
  mean_power: number
  vehicle_weight: number
  rfid_identifier: string
  created_at?: string
}

export interface TeamUpdate {
  name?: string
  vehicle_weight?: number
  mean_power?: number
  rfid_identifier?: string
  category?: TeamCategory
}

export const teamsApi = {
  async listTeams(): Promise<Team[]> {
    const response = await authenticatedFetch(`${API_BASE_URL}/teams/`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to fetch teams' }))
      throw new Error(error.detail || 'Failed to fetch teams')
    }
    return response.json()
  },

  async getTeamById(id: number): Promise<Team> {
    const response = await authenticatedFetch(`${API_BASE_URL}/teams/${id}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Team not found' }))
      throw new Error(error.detail || 'Team not found')
    }
    return response.json()
  },

  async getTeamsByIds(teamIds: number[]): Promise<Team[]> {
    const params = new URLSearchParams()
    teamIds.forEach(id => params.append('team_ids', id.toString()))
    
    const response = await authenticatedFetch(`${API_BASE_URL}/teams/by-ids/?${params}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to fetch teams' }))
      throw new Error(error.detail || 'Failed to fetch teams')
    }
    return response.json()
  },

  async createTeam(data: TeamCreate): Promise<Team> {
    const response = await authenticatedFetch(`${API_BASE_URL}/teams/`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to create team' }))
      throw new Error(error.detail || 'Failed to create team')
    }
    return response.json()
  },

  async updateTeam(id: number, data: TeamUpdate): Promise<Team> {
    const response = await authenticatedFetch(`${API_BASE_URL}/teams/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to update team' }))
      throw new Error(error.detail || 'Failed to update team')
    }
    return response.json()
  },

  async deleteTeam(id: number): Promise<void> {
    const response = await authenticatedFetch(`${API_BASE_URL}/teams/${id}`, {
      method: 'DELETE',
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to delete team' }))
      throw new Error(error.detail || 'Failed to delete team')
    }
  },
}