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

export default function Webapp() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [currentUser, setCurrentUser] = useState<any | null>(null)
  const [activeTab, setActiveTab] = useState<Tabs>("leaderboard")
  const [isAddDriverOpen, setIsAddDriverOpen] = useState(false)
  const [isAddTeamOpen, setIsAddTeamOpen] = useState(false)
  const [isAddUserOpen, setIsAddUserOpen] = useState(false)
  const [isAddChallengeOpen, setIsAddChallengeOpen] = useState(false)
  const [editingDriver, setEditingDriver] = useState<any | null>(null)
  const [editingTeam, setEditingTeam] = useState<any | null>(null)
  const [editingUser, setEditingUser] = useState<any | null>(null)
  const [editingChallenge, setEditingChallenge] = useState<any | null>(null)
  const [drivers, setDrivers] = useState<any[]>([])
  const [visibleTeams, setVisibleTeams] = useState<any[]>([])
  const [users, setUsers] = useState<any[]>([])
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
  const handleDeleteTeam = (id: string | number) => {}
  const handleExport = () => {}
  const toggleUserStatus = (id: string | number) => {}
  const handleEditUser = (user: any) => {
    setIsAddUserOpen(true)
    setEditingUser(user)
  }
  const deleteChallenge = (id: string | number) => {
    setChallenges(challenges.filter((c) => c.id !== id))
  }
  const handleEditChallenge = (challenge: any) => {
    setIsAddChallengeOpen(true)
    setEditingChallenge(challenge)
  }
  const getTeamName = (id: string | number | undefined): string => {
    const team = visibleTeams.find((team) => team.id === id)
    return team ? team.name : "N/A"
  }
  const handleLogin = (username: string, password: string) => {
    setCurrentUser({
      id: 1,
      username,
      role: "admin",
    })
    setIsLoggedIn(true)
  }

  const handleLogout = () => {
    setCurrentUser(null)
    setIsLoggedIn(false)
  }

  return (
    <SideBarLayout activeTab={activeTab} setActiveTab={setActiveTab}>
      {activeTab === "leaderboard" && (
        <LeaderboardTab
          raceCategories={raceCategories}
          selectedCategory={selectedCategory}
          setSelectedCategory={setSelectedCategory}
          mockLeaderboardData={mockLeaderboardData}
        />
      )}
      {activeTab === "drivers" && (
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
        />
      )}
      {activeTab === "challenges" && (
        <ChallengeTab
          challenges={challenges}
          setIsAddChallengeOpen={setIsAddChallengeOpen}
          setEditingChallenge={handleEditChallenge}
          deleteChallenge={deleteChallenge}
        />
      )}
      {activeTab === "users" && (
        <UsersTab
          users={users}
          setIsAddUserOpen={setIsAddUserOpen}
          handleEditUser={handleEditUser}
          toggleUserStatus={toggleUserStatus}
          getTeamName={getTeamName}
        />
      )}
      {activeTab === "export" && (
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
