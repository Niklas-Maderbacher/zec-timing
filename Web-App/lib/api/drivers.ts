import { authenticatedFetch } from "@/lib/auth"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL

export interface Driver {
  id: number
  name: string
  team_id: number
  weight: number
  created_at: string
}

export interface DriverCreate {
  name: string
  team_id: number
  weight: number
  created_at?: string
}

export interface DriverUpdate {
  name?: string
  team_id?: number
  weight?: number
}

export const driversApi = {
  async listDrivers(): Promise<Driver[]> {
    const response = await authenticatedFetch(`${API_BASE_URL}/drivers/`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to fetch drivers' }))
      throw new Error(error.detail || 'Failed to fetch drivers')
    }
    return response.json()
  },

  async getDriverById(id: number): Promise<Driver> {
    const response = await authenticatedFetch(`${API_BASE_URL}/drivers/${id}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Driver not found' }))
      throw new Error(error.detail || 'Driver not found')
    }
    return response.json()
  },

  async getDriversByTeam(teamId: number): Promise<Driver[]> {
    const response = await authenticatedFetch(`${API_BASE_URL}/drivers/team/${teamId}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to fetch drivers' }))
      throw new Error(error.detail || 'Failed to fetch drivers')
    }
    return response.json()
  },

  async createDriver(data: DriverCreate): Promise<Driver> {
    const response = await authenticatedFetch(`${API_BASE_URL}/drivers/`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to create driver' }))
      throw new Error(error.detail || 'Failed to create driver')
    }
    return response.json()
  },

  async updateDriver(id: number, data: DriverUpdate): Promise<Driver> {
    const response = await authenticatedFetch(`${API_BASE_URL}/drivers/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to update driver' }))
      throw new Error(error.detail || 'Failed to update driver')
    }
    return response.json()
  },

  async deleteDriver(id: number): Promise<void> {
    const response = await authenticatedFetch(`${API_BASE_URL}/drivers/${id}`, {
      method: 'DELETE',
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to delete driver' }))
      throw new Error(error.detail || 'Failed to delete driver')
    }
  },
}