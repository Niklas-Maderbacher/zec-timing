"use client"

import { useState, useEffect } from "react"
import TeamsTab from "@/components/tabs/TeamsTab"
import TeamLeadView from "@/components/tabs/TeamLeadView"
import AttemptsTab from "@/components/tabs/AttemptTab"
import UsersTab from "@/components/tabs/UsersTab"
import ChallengeTab from "@/components/tabs/ChallengeTab"
import ExportTab from "@/components/tabs/ExportTab"
import LeaderboardTab from "@/components/tabs/LeaderboardTab"
import LoginTab from "@/components/tabs/LoginTab"
import {SideBarLayout, type Tabs} from "@/components/layout/sidebarlayout"
import { AuthService } from "@/lib/auth"
import { getPermissions, getDefaultTab, canAccessTab } from "@/lib/permissions"

interface User {
  id: string
  username: string
  role: string
}

export default function Webapp() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [currentUser, setCurrentUser] = useState<User | null>(null)
  const [activeTab, setActiveTab] = useState<Tabs>("leaderboard")
  const permissions = getPermissions(currentUser?.role || null)

  useEffect(() => {
    if (AuthService.isLoggedIn()) {
      const token = AuthService.getAccessToken()
      if (token) {
        const username = AuthService.getUsername(token)
        const role = AuthService.getUserRole(token)
        
        if (username && role) {
          const user = {
            id: username,
            username,
            role,
          }
          setCurrentUser(user)
          setIsLoggedIn(true)
          setActiveTab(getDefaultTab(role))
        }
      }
    }
  }, [])

  const handleLoginSuccess = (user: User) => {
    setCurrentUser(user)
    setIsLoggedIn(true)
    setActiveTab(getDefaultTab(user.role))
  }

  const handleLogout = () => {
    setCurrentUser(null)
    setIsLoggedIn(false)
    setActiveTab("login")
  }

  const handleTabChange = (tab: Tabs) => {
    if (canAccessTab(currentUser?.role || null, tab)) {
      setActiveTab(tab)
    } else {
      console.warn(`Access denied to tab: ${tab}`)
    }
  }

  return (
    <SideBarLayout 
      activeTab={activeTab} 
      setActiveTab={handleTabChange}
      userRole={currentUser?.role}
    >
      {activeTab === "leaderboard" && (
        <LeaderboardTab />
      )}
      {activeTab === "attempts" && permissions.canViewAttempts && (
        <AttemptsTab />
      )}
      {activeTab === "teams" && (
        <>
          {currentUser?.role === "teamlead" && permissions.canEditTeams ? (
            <TeamLeadView />
          ) : currentUser?.role === "admin" && permissions.canEditTeams ? (
            <TeamsTab />
          ) : null}
        </>
      )}
      {activeTab === "challenges" && permissions.canEditChallenges && (
        <ChallengeTab />
      )}
      {activeTab === "users" && permissions.canEditUsers && (
        <UsersTab />
      )}
      {activeTab === "export" && permissions.canExport && (
        <ExportTab />
      )}
      {activeTab === "login" && (
        <LoginTab
          isLoggedIn={isLoggedIn}
          user={currentUser}
          onLoginSuccess={handleLoginSuccess}
          onLogout={handleLogout}
        />
      )}
    </SideBarLayout>
  )
}