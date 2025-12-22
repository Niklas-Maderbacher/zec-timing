"use client"

import { useState } from "react"
import {
  Sidebar,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"

import { User, Users, UserCog, Download, Trophy } from "lucide-react"

import DriversTab from "@/components/tabs/DriversTab"
import TeamsTab from "@/components/tabs/TeamsTab"
import UsersTab from "@/components/tabs/UsersTab"
import ExportTab from "@/components/tabs/ExportTab"
import LeaderboardTab from "@/components/tabs/LeaderboardTab"

type AdminTab = "drivers" | "teams" | "users" | "config" | "export" | "leaderboard"

export function AppSidebar({ children }: { children?: React.ReactNode }) {
  const [open, setOpen] = useState(false)

  return <SidebarProvider open={open} onOpenChange={setOpen}>{children}</SidebarProvider>
}

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState<AdminTab>("drivers")
  const [isAddDriverOpen, setIsAddDriverOpen] = useState(false)
  const [isAddTeamOpen, setIsAddTeamOpen] = useState(false)
  const [isAddUserOpen, setIsAddUserOpen] = useState(false)
  const [editingDriver, setEditingDriver] = useState<any | null>(null)
  const [editingTeam, setEditingTeam] = useState<any | null>(null)
  const [editingUser, setEditingUser] = useState<any | null>(null)
  const [drivers, setDrivers] = useState<any[]>([])
  const [visibleTeams, setVisibleTeams] = useState<any[]>([])
  const [users, setUsers] = useState<any[]>([])
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
  const getTeamName = (id: string | number | undefined): string => {
    const team = visibleTeams.find((team) => team.id === id)
    return team ? team.name : "N/A"
  }

  return (
    <AppSidebar>
      <div className="flex min-h-screen">
        <Sidebar className="w-64 border-r">
          <SidebarHeader className="px-4 py-3 text-xl font-semibold">ZEC-Timing</SidebarHeader>
          <SidebarMenu>

            <SidebarMenuItem>
              <SidebarMenuButton
                isActive={activeTab === "leaderboard"}
                onClick={() => setActiveTab("leaderboard")}
                icon={<Trophy className="h-4 w-4" />}
              >
                Leaderboard
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton
                isActive={activeTab === "teams"}
                onClick={() => setActiveTab("teams")}
                icon={<Users className="h-4 w-4" />}
              >
                Teams
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton
                isActive={activeTab === "drivers"}
                onClick={() => setActiveTab("drivers")}
                icon={<User className="h-4 w-4" />}
              >
                Drivers
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton
                isActive={activeTab === "users"}
                onClick={() => setActiveTab("users")}
                icon={<UserCog className="h-4 w-4" />}
              >
                Users
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton
                isActive={activeTab === "export"}
                onClick={() => setActiveTab("export")}
                icon={<Download className="h-4 w-4" />}
              >
                Export
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </Sidebar>

        <main className="flex-1 p-6">
          <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <SidebarTrigger />
            </div>
          </div>

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
        </main>
      </div>
    </AppSidebar>
  )
}
