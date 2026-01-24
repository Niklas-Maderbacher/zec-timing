"use client"
import { useState, useEffect } from "react"
import DriversTab from "@/components/tabs/DriversTab"
import TeamsTab from "@/components/tabs/TeamsTab"
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
  const [isAddDriverOpen, setIsAddDriverOpen] = useState(false)
  const [isAddTeamOpen, setIsAddTeamOpen] = useState(false)
  const [isAddChallengeOpen, setIsAddChallengeOpen] = useState(false)
  const [editingDriver, setEditingDriver] = useState<any | null>(null)
  const [editingTeam, setEditingTeam] = useState<any | null>(null)
  const [editingChallenge, setEditingChallenge] = useState<any | null>(null)
  const [drivers, setDrivers] = useState<any[]>([])
  const [visibleTeams, setVisibleTeams] = useState<any[]>([])
  const [challenges, setChallenges] = useState<any[]>([])
  const [exportFormat, setExportFormat] = useState("csv")
  const [exportDateRange, setExportDateRange] = useState({
    from: new Date().toISOString(),
    to: new Date().toISOString(),
  })
  const raceCategories = ["test1", "test2"]
  const [selectedCategory, setSelectedCategory] = useState(raceCategories[0])
  const mockLeaderboardData = {
    test1: [
      { position: 1, driver: "Pro One", team: "Gamma", bestTime: "1:11.999", points: 100 },
      { position: 2, driver: "Pro One", team: "Gamma", bestTime: "1:11.999", points: 100 },
      { position: 3, driver: "Pro One", team: "Gamma", bestTime: "1:11.999", points: 100 },
      { position: 4, driver: "Pro One", team: "Gamma", bestTime: "1:11.999", points: 100 },
      { position: 5, driver: "Pro One", team: "Gamma", bestTime: "1:11.999", points: 100 },
      { position: 6, driver: "Pro One", team: "Gamma", bestTime: "1:11.999", points: 100 },
      { position: 7, driver: "Pro One", team: "Gamma", bestTime: "1:11.999", points: 100 },
      { position: 8, driver: "Pro One", team: "Gamma", bestTime: "1:11.999", points: 100 },
    ],
    test2: [
      { position: 1, driver: "Am One", team: "Delta", bestTime: "1:15.123", points: 80 },
    ],
  }

  // Get user permissions
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
          // Set default tab based on role
          setActiveTab(getDefaultTab(role))
        }
      }
    }
  }, [])

  const handleLogin = async (username: string, password: string) => {
    try {
      const tokenData = await AuthService.login(username, password)
      const role = AuthService.getUserRole(tokenData.access_token)
      const userUsername = AuthService.getUsername(tokenData.access_token)
      
      const user = {
        id: userUsername || username,
        username: userUsername || username,
        role: role || "viewer",
      }
      
      setCurrentUser(user)
      setIsLoggedIn(true)
      // Navigate to default tab for user's role
      setActiveTab(getDefaultTab(user.role))
    } catch (error) {
      console.error("Login failed:", error)
      throw error 
    }
  }

  const handleLogout = () => {
    AuthService.clearTokens()
    setCurrentUser(null)
    setIsLoggedIn(false)
    setActiveTab("login")
  }

  // Enhanced tab change handler that checks permissions
  const handleTabChange = (tab: Tabs) => {
    if (canAccessTab(currentUser?.role || null, tab)) {
      setActiveTab(tab)
    } else {
      console.warn(`Access denied to tab: ${tab}`)
    }
  }

  const handleDeleteTeam = (id: string | number) => {
    if (!permissions.canEditTeams) {
      alert("You don't have permission to delete teams")
      return
    }
    // Your delete logic here
  }
  
  const handleExport = () => {
    if (!permissions.canExport) {
      alert("You don't have permission to export data")
      return
    }
    // Your export logic here
  }
  
  const toggleUserStatus = (id: string | number) => {
    if (!permissions.canEditUsers) {
      alert("You don't have permission to edit users")
      return
    }
    // Your toggle logic here
  }
  
  const handleEditUser = (user: any) => {
    if (!permissions.canEditUsers) {
      alert("You don't have permission to edit users")
      return
    }
    setIsAddUserOpen(true)
    setEditingUser(user)
  }
  
  const deleteChallenge = (id: string | number) => {
    if (!permissions.canEditChallenges) {
      alert("You don't have permission to delete challenges")
      return
    }
    setChallenges(challenges.filter((c) => c.id !== id))
  }
  
  const handleEditChallenge = (challenge: any) => {
    if (!permissions.canEditChallenges) {
      alert("You don't have permission to edit challenges")
      return
    }
    setIsAddChallengeOpen(true)
    setEditingChallenge(challenge)
  }
  
  const getTeamName = (id: string | number | undefined): string => {
    const team = visibleTeams.find((team) => team.id === id)
    return team ? team.name : "N/A"
  }

  return (
    <SideBarLayout 
      activeTab={activeTab} 
      setActiveTab={handleTabChange}
      userRole={currentUser?.role}
    >
      {activeTab === "leaderboard" && (
        <LeaderboardTab
          raceCategories={raceCategories}
          selectedCategory={selectedCategory}
          setSelectedCategory={setSelectedCategory}
          mockLeaderboardData={mockLeaderboardData}
        />
      )}
      {activeTab === "drivers" && permissions.canEditDrivers && (
        <DriversTab
          drivers={drivers}
          setDrivers={setDrivers}
          setIsAddDriverOpen={setIsAddDriverOpen}
          setEditingDriver={setEditingDriver}
        />
      )}
      {activeTab === "teams" && (
        <TeamsTab
          visibleTeams={visibleTeams}
          setIsAddTeamOpen={setIsAddTeamOpen}
          setEditingTeam={setEditingTeam}
          handleDeleteTeam={handleDeleteTeam}
          canEdit={permissions.canEditTeams}
        />
      )}
      {activeTab === "challenges" && permissions.canEditChallenges && (
        <ChallengeTab
          challenges={challenges}
          setIsAddChallengeOpen={setIsAddChallengeOpen}
          setEditingChallenge={handleEditChallenge}
          deleteChallenge={deleteChallenge}
        />
      )}
      {activeTab === "users" && permissions.canEditUsers && (
        <UsersTab />
      )}
      {activeTab === "export" && permissions.canExport && (
        <ExportTab
          exportFormat={exportFormat}
          setExportFormat={setExportFormat}
          exportDateRange={exportDateRange}
          setExportDateRange={setExportDateRange}
          handleExport={handleExport}
        />
      )}
      {activeTab === "login" && (
        <LoginTab
          isLoggedIn={isLoggedIn}
          user={currentUser}
          onLogin={handleLogin}
          onLogout={handleLogout}
        />
      )}
    </SideBarLayout>
  )
}