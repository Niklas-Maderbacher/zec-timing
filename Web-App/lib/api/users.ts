// lib/api/users.ts
import { authenticatedFetch } from "@/lib/auth"

const API_BASE_URL = typeof window !== 'undefined' 
  ? (process.env.NEXT_PUBLIC_API_URL || 'http://localhost'): 'http://localhost'

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
  // List all users
  async listUsers(): Promise<any[]> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to fetch users' }))
      throw new Error(error.detail || 'Failed to fetch users')
    }
    return response.json()
  },

  // Create a new user
  async createUser(data: CreateUserRequest): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to create user' }))
      throw new Error(error.detail || 'Failed to create user')
    }
    return response.json()
  },

  // Get user by username
  async getUserByUsername(username: string): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/username/${username}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'User not found' }))
      throw new Error(error.detail || 'User not found')
    }
    return response.json()
  },

  // Get user by ID
  async getUserById(id: string): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/id/${id}`)
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'User not found' }))
      throw new Error(error.detail || 'User not found')
    }
    return response.json()
  },

  // Update user
  async updateUser(userId: string, data: UpdateUserRequest): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to update user' }))
      throw new Error(error.detail || 'Failed to update user')
    }
    return response.json()
  },

  // Delete user
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

  // Assign roles to user
  async assignRoles(userId: string, roles: string[]): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/${userId}/roles`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ roles }),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to assign roles' }))
      throw new Error(error.detail || 'Failed to assign roles')
    }
    return response.json()
  },

  // Remove roles from user
  async removeRoles(userId: string, roles: string[]): Promise<any> {
    const response = await authenticatedFetch(`${API_BASE_URL}/users/${userId}/roles`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ roles }),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to remove roles' }))
      throw new Error(error.detail || 'Failed to remove roles')
    }
    return response.json()
  },
}