"use client"
import { useState } from "react"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Label } from "@/components/ui/label"
import { Plus, Edit, Trash2, Download, Trophy } from "lucide-react"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"

export default function AdminPage() {
  const [isAddDriverOpen, setIsAddDriverOpen] = useState(false)
  const [isAddTeamOpen, setIsAddTeamOpen] = useState(false)
  const [isAddUserOpen, setIsAddUserOpen] = useState(false)
  const [editingDriver, setEditingDriver] = useState(null)
  const [editingTeam, setEditingTeam] = useState(null)
  const [drivers, setDrivers] = useState([])
  const [visibleTeams, setVisibleTeams] = useState([])
  const [users, setUsers] = useState([])
  const [exportFormat, setExportFormat] = useState("csv")
  const [exportDateRange, setExportDateRange] = useState({
    from: new Date().toISOString(),
    to: new Date().toISOString(),
  })

  const [editingUser, setEditingUser] = useState(null)
  const raceCategories = ["test2", "test1"]
  const [selectedCategory, setSelectedCategory] = useState(raceCategories[0] ?? "test2")
  const mockLeaderboardData = {
    test1: [
      { position: 1, driver: "Pro One", team: "Gamma", bestTime: "1:11.999", points: 100 },
    ],
    test2: [
      { position: 1, driver: "Am One", team: "Delta", bestTime: "1:15.123", points: 80 },
    ],
  }

  const handleDeleteTeam = (id) => {
    // delete team logic
  }

  const handleSaveConfig = () => {
    // save config logic
  }

  const handleExport = () => {
    // export logic
  }

  const getTeamName = (id) => {
    const team = visibleTeams.find((team) => team.id === id)
    return team ? team.name : "N/A"
  }

  const toggleUserStatus = (id) => {
    // toggle user status logic
  }

  const handleEditUser = (user) => {
    setIsAddUserOpen(true)
    setEditingUser(user)
  }

  return (
    <Tabs defaultValue="drivers" className="w-full">
      <TabsList>
        <TabsTrigger value="drivers">Drivers</TabsTrigger>
        <TabsTrigger value="teams">Teams</TabsTrigger>
        <TabsTrigger value="users">Users</TabsTrigger>
        <TabsTrigger value="config">Config</TabsTrigger>
        <TabsTrigger value="export">Export</TabsTrigger>
        <TabsTrigger value="leaderboard">Leaderboards</TabsTrigger>
      </TabsList>

      {/* Leaderboard Tab */}
      <TabsContent value="leaderboard" className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Race Leaderboard</h2>
          </div>
          <Select value={selectedCategory} onValueChange={(value) => setSelectedCategory(value)}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Select category" />
            </SelectTrigger>
            <SelectContent>
              {raceCategories.map((category) => (
                <SelectItem key={category} value={category}>
                  {category}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Trophy className="h-5 w-5" />
              <span>{selectedCategory} Standings</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {(mockLeaderboardData[selectedCategory] || []).map((entry) => (
                <div
                  key={entry.position}
                  className="flex items-center justify-between p-3 bg-slate-50 rounded-lg"
                >
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center justify-center w-8 h-8 bg-blue-600 text-white rounded-full text-sm font-bold">
                      {entry.position}
                    </div>
                    <div>
                      <div className="font-medium">{entry.driver}</div>
                      <div className="text-sm text-muted-foreground">{entry.team}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-mono font-medium">{entry.bestTime}</div>
                    <div className="text-sm text-muted-foreground">{entry.points} pts</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      {/* Drivers Tab */}
      <TabsContent value="drivers" className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold">Driver Management</h2>
          </div>
          <Button onClick={() => setIsAddDriverOpen(true)} className="flex items-center space-x-2">
            <Plus className="h-4 w-4" />
            <span>Add Driver</span>
          </Button>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>All Drivers</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Driver Name</TableHead>
                  <TableHead>Team</TableHead>
                  <TableHead>Best Lap Time</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {drivers.map((driver) => (
                  <TableRow key={driver.id}>
                    <TableCell className="font-medium">{driver.name}</TableCell>
                    <TableCell>{driver.teamName}</TableCell>
                    <TableCell>{driver.licenseNumber}</TableCell>
                    <TableCell>{driver.bestLapTime}</TableCell>
                    <TableCell>
                      <span
                        className={`px-2 py-1 rounded-full text-xs ${
                          driver.status === "Active" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                        }`}
                      >
                        {driver.status}
                      </span>
                    </TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button variant="outline" size="sm" onClick={() => setEditingDriver(driver)}>
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setDrivers(drivers.filter((d) => d.id !== driver.id))}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </TabsContent>

      {/* Teams Tab */}
      <TabsContent value="teams" className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Race Teams</h2>
          </div>
          <Button onClick={() => setIsAddTeamOpen(true)} className="flex items-center space-x-2">
            <Plus className="h-4 w-4" />
            <span>Add Team</span>
          </Button>
        </div>
        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Team Name</TableHead>
                  <TableHead>Drivers</TableHead>
                  <TableHead>Points</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {visibleTeams.map((team) => (
                  <TableRow key={team.id}>
                    <TableCell className="font-medium">{team.name}</TableCell>
                    <TableCell>{team.country}</TableCell>
                    <TableCell>{team.drivers}</TableCell>
                    <TableCell className="font-mono">{team.bestLapTime}</TableCell>
                    <TableCell>{team.points}</TableCell>
                    <TableCell>{team.podiums}</TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setEditingTeam(team)}
                          className="flex items-center space-x-1"
                        >
                          <Edit className="h-3 w-3" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDeleteTeam(team.id)}
                          className="flex items-center space-x-1 text-red-600 hover:text-red-700"
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </TabsContent>

      {/* Users Tab */}
      <TabsContent value="users" className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-2xl font-bold text-slate-900">User Management</h3>
          </div>
          <Button onClick={() => setIsAddUserOpen(true)}>
            <Plus className="mr-2 h-4 w-4" />
            Add User
          </Button>
        </div>
        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Username</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell>{user.username}</TableCell>
                    <TableCell>{user.role}</TableCell>
                    <TableCell>{user.assignedTeam ? getTeamName(user.assignedTeam) : "N/A"}</TableCell>
                    <TableCell>
                      <Badge variant={user.status === "active" ? "secondary" : "destructive"}>
                        {user.status}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Button variant="ghost" size="sm" onClick={() => handleEditUser(user)}>
                        Edit
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => toggleUserStatus(user.id)}
                        className="ml-2"
                      >
                        {user.status === "active" ? "Deactivate" : "Activate"}
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </TabsContent>

      {/* Config Tab */}
      <TabsContent value="config" className="space-y-6">
        <div className="grid gap-6">
          <Card>
            <CardHeader>
              <CardTitle>System Configuration</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Auto Refresh</Label>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="space-y-2">
                <Label>Refresh Interval</Label>
                <Select defaultValue="5">
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">1 minute</SelectItem>
                    <SelectItem value="5">5 minutes</SelectItem>
                    <SelectItem value="10">10 minutes</SelectItem>
                    <SelectItem value="30">30 minutes</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button onClick={handleSaveConfig}>Save Configuration</Button>
            </CardContent>
          </Card>
        </div>
      </TabsContent>

      {/* Export Tab */}
      <TabsContent value="export" className="space-y-6">
        <div>
          <h3 className="text-2xl font-bold text-slate-900">Data Export</h3>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Leaderboard Export</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Format</Label>
                <Select defaultValue="csv" onValueChange={setExportFormat}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="csv">CSV</SelectItem>
                    <SelectItem value="pdf">PDF</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button className="w-full" onClick={() => handleExport()}>
                <Download className="mr-2 h-4 w-4" />
                Export Leaderboard
              </Button>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Race Data Export</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Date Range</Label>
                <Select
                  defaultValue="today"
                  onValueChange={(value) =>
                    setExportDateRange({
                      from: value === "today" ? new Date().toISOString() : "",
                      to: value === "today" ? new Date().toISOString() : "",
                    })
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="today">Today</SelectItem>
                    <SelectItem value="week">This Week</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button className="w-full" onClick={() => handleExport()}>
                <Download className="mr-2 h-4 w-4" />
                Export Race Data
              </Button>
            </CardContent>
          </Card>
        </div>
      </TabsContent>
    </Tabs>
  )
}