import { authenticatedFetch } from "@/lib/auth"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL

export interface UserKC {
  id: string
  username: string
  email?: string
  firstName?: string
  lastName?: string
  enabled: boolean
  emailVerified?: boolean
  roles?: string[]
}

export interface CreateUserRequest {
  username: string
  password: string
}

export interface UpdateUserRequest {
  username?: string
  password?: string
}

export interface UserRolesRequest {
  roles: string[]
}

export const usersApi = {
  async listUsers(): Promise<any[]> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to fetch users' }))
      throw new Error(error.detail || 'Failed to fetch users')
    }
    return response.json()
  },

  async createUser(data: CreateUserRequest): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to create user' }))
      throw new Error(error.detail || 'Failed to create user')
    }
    return response.json()
  },

  async getUserByUsername(username: string): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/username/${username}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'User not found' }))
      throw new Error(error.detail || 'User not found')
    }
    return response.json()
  },

  async getUserById(id: string): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/id/${id}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'User not found' }))
      throw new Error(error.detail || 'User not found')
    }
    return response.json()
  },

  async updateUser(userId: string, data: UpdateUserRequest): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to update user' }))
      throw new Error(error.detail || 'Failed to update user')
    }
    return response.json()
  },

  async deleteUser(userId: string): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'DELETE',
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to delete user' }))
      throw new Error(error.detail || 'Failed to delete user')
    }
    return response.json()
  },

  async assignRoles(userId: string, roles: string[]): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/${userId}/roles`, {
      method: 'POST',
      body: JSON.stringify({ roles }),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to assign roles' }))
      throw new Error(error.detail || 'Failed to assign roles')
    }
    return response.json()
  },

  async removeRoles(userId: string, roles: string[]): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/${userId}/roles`, {
      method: 'DELETE',
      body: JSON.stringify({ roles }),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to remove roles' }))
      throw new Error(error.detail || 'Failed to remove roles')
    }
    return response.json()
  },
}
