import { Tabs } from "@/components/layout/sidebarlayout"

export type UserRole = 'admin' | 'teamlead' | 'viewer'

export interface RolePermissions {
  allowedTabs: Tabs[]
  canViewAttempts: boolean
  canEditDrivers: boolean
  canEditTeams: boolean
  canEditUsers: boolean
  canEditChallenges: boolean
  canExport: boolean
}

const rolePermissions: Record<UserRole, RolePermissions> = {
  admin: {
    allowedTabs: ['leaderboard', 'attempts', 'teams', 'challenges', 'users', 'export', 'login'],
    canViewAttempts: true,
    canEditDrivers: true,
    canEditTeams: true,
    canEditUsers: true,
    canEditChallenges: true,
    canExport: true,
  },
  teamlead: {
    allowedTabs: ['leaderboard', 'teams', 'login'],
    canViewAttempts: false,
    canEditDrivers: false,
    canEditTeams: true,
    canEditUsers: false,
    canEditChallenges: false,
    canExport: false,
  },
  viewer: {
    allowedTabs: ['leaderboard', 'login'],
    canViewAttempts: false,
    canEditDrivers: false,
    canEditTeams: false,
    canEditUsers: false,
    canEditChallenges: false,
    canExport: false,
  },
}

export function getPermissions(role: string | null): RolePermissions {
  if (!role) {
    return rolePermissions.viewer
  }
  
  const normalizedRole = role.toLowerCase() as UserRole
  return rolePermissions[normalizedRole] || rolePermissions.viewer
}

export function canAccessTab(role: string | null, tab: Tabs): boolean {
  const permissions = getPermissions(role)
  return permissions.allowedTabs.includes(tab)
}

export function getDefaultTab(role: string | null): Tabs {
  const permissions = getPermissions(role)
  return permissions.allowedTabs[0] || 'leaderboard'
}