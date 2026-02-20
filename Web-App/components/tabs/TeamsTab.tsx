"use client"
import React, { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ConfirmDialog } from "@/components/dialogs/confirm-dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Plus, Trash2, Edit, Users, Loader2, X } from "lucide-react"
import { teamsApi, type Team, type TeamCreate, type TeamUpdate, TeamCategory } from "@/lib/api/teams"
import { driversApi, type Driver, type DriverCreate } from "@/lib/api/drivers"
import { toast } from "sonner"

const CATEGORY_LABELS: Record<TeamCategory, string> = {
  [TeamCategory.CLOSE_TO_SERIES]: "Close to Series",
  [TeamCategory.ADVANCED_CLASS]: "Advanced Class",
  [TeamCategory.PROFESSIONAL_CLASS]: "Professional Class",
}

interface DriverFormData {
  name: string
  weight: number
}

export default function TeamsTab() {
  const [teams, setTeams] = useState<Team[]>([])
  const [drivers, setDrivers] = useState<Record<number, Driver[]>>({})
  const [isLoading, setIsLoading] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)

  const [teamToDelete, setTeamToDelete] = useState<number | null>(null)
  const [driverToDelete, setDriverToDelete] = useState<{ id: number; teamId: number } | null>(null)

  const [isTeamDialogOpen, setIsTeamDialogOpen] = useState(false)
  const [editingTeam, setEditingTeam] = useState<Team | null>(null)
  const [expandedTeams, setExpandedTeams] = useState<Set<number>>(new Set())

  const [teamForm, setTeamForm] = useState<TeamCreate>({
    category: TeamCategory.CLOSE_TO_SERIES,
    name: "",
    mean_power: 0,
    vehicle_weight: 0,
    rfid_identifier: "",
  })

  const [newDrivers, setNewDrivers] = useState<DriverFormData[]>([])

  useEffect(() => {
    loadTeams()
  }, [])

  const loadTeams = async () => {
    setIsLoading(true)
    try {
      const data = await teamsApi.listTeams()
      setTeams(data)
    } catch (error: any) {
      console.error("Failed to load teams:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const loadDriversForTeam = async (teamId: number) => {
    try {
      const data = await driversApi.getDriversByTeam(teamId)
      setDrivers(prev => ({ ...prev, [teamId]: data }))
    } catch (error: any) {
      setDrivers(prev => ({ ...prev, [teamId]: [] }))
    }
  }

  const toggleTeamExpansion = (teamId: number) => {
    const newExpanded = new Set(expandedTeams)
    if (newExpanded.has(teamId)) {
      newExpanded.delete(teamId)
    } else {
      newExpanded.add(teamId)
      if (!drivers[teamId]) {
        loadDriversForTeam(teamId)
      }
    }
    setExpandedTeams(newExpanded)
  }

  const handleCreateTeam = async () => {
    if (!teamForm.name || !teamForm.rfid_identifier) {
      toast.error("Team name and RFID identifier are required")
      return
    }

    setIsLoading(true)
    try {
      const newTeam = await teamsApi.createTeam(teamForm)
      toast.success("Team created successfully")
      if (newDrivers.length > 0) {
        await Promise.all(
          newDrivers.map(driver =>
            driversApi.createDriver({
              name: driver.name,
              weight: driver.weight,
              team_id: newTeam.id,
            })
          )
        )
        toast.success(`${newDrivers.length} driver(s) added to team`)
      }

      setIsTeamDialogOpen(false)
      resetForm()
      loadTeams()
    } catch (error: any) {
      toast.error(error.message || "Failed to create team")
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpdateTeam = async () => {
    if (!editingTeam) return

    setIsLoading(true)
    try {
      const updateData: TeamUpdate = {
        name: teamForm.name,
        vehicle_weight: teamForm.vehicle_weight,
        mean_power: teamForm.mean_power,
        rfid_identifier: teamForm.rfid_identifier,
        category: teamForm.category,
      }

      await teamsApi.updateTeam(editingTeam.id, updateData)
      toast.success("Team updated successfully")

      setIsTeamDialogOpen(false)
      setEditingTeam(null)
      resetForm()
      loadTeams()
    } catch (error: any) {
      toast.error(error.message || "Failed to update team")
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteTeam = async () => {
    if (!teamToDelete) return

    setIsDeleting(true)
    try {
      await teamsApi.deleteTeam(teamToDelete)
      toast.success("Team deleted successfully")
      loadTeams()
    } catch (error: any) {
      toast.error(error.message || "Failed to delete team")
    } finally {
      setIsDeleting(false)
      setTeamToDelete(null)
    }
  }

  const handleDeleteDriver = async () => {
    if (!driverToDelete) return
    setIsDeleting(true)
    try {
      await driversApi.deleteDriver(driverToDelete.id)
      toast.success("Driver deleted successfully")
      loadDriversForTeam(driverToDelete.teamId)
    } catch (error: any) {
      toast.error(error.message || "Failed to delete driver")
    } finally {
      setIsDeleting(false)
      setDriverToDelete(null)
    }
  }

  const openEditDialog = (team: Team) => {
    setEditingTeam(team)
    setTeamForm({
      category: team.category,
      name: team.name,
      mean_power: team.mean_power,
      vehicle_weight: team.vehicle_weight,
      rfid_identifier: team.rfid_identifier,
    })
    setIsTeamDialogOpen(true)
  }

  const addDriverField = () => {
    setNewDrivers([...newDrivers, { name: "", weight: 0 }])
  }

  const removeDriverField = (index: number) => {
    setNewDrivers(newDrivers.filter((_, i) => i !== index))
  }

  const updateDriverField = (index: number, field: keyof DriverFormData, value: string | number) => {
    const updated = [...newDrivers]
    updated[index] = { ...updated[index], [field]: value }
    setNewDrivers(updated)
  }

  const resetForm = () => {
    setTeamForm({
      category: TeamCategory.CLOSE_TO_SERIES,
      name: "",
      mean_power: 0,
      vehicle_weight: 0,
      rfid_identifier: "",
    })
    setNewDrivers([])
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Teams & Drivers Management</h2>
        <Button
          onClick={() => {
            resetForm()
            setIsTeamDialogOpen(true)
          }}
          className="flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          <span>Add Team</span>
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Teams</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Team Name</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Weight (kg)</TableHead>
                <TableHead>Power (W)</TableHead>
                <TableHead>RFID</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {teams.length === 0 && (
                <TableRow>
                  <TableCell colSpan={6} className="text-center text-muted-foreground">
                    No teams found. Add a team to get started.
                  </TableCell>
                </TableRow>
              )}
              {teams.map((team) => (
                <React.Fragment key={team.id}>
                  <TableRow>
                    <TableCell className="font-medium">{team.name}</TableCell>
                    <TableCell>
                      <Badge variant="outline">{CATEGORY_LABELS[team.category]}</Badge>
                    </TableCell>
                    <TableCell>{team.vehicle_weight}</TableCell>
                    <TableCell>{team.mean_power}</TableCell>
                    <TableCell className="font-mono text-sm">{team.rfid_identifier}</TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => toggleTeamExpansion(team.id)}
                        >
                          <Users className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => openEditDialog(team)}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setTeamToDelete(team.id)}
                          disabled={isLoading}
                        >
                          <Trash2 className="h-4 w-4 text-destructive" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                  {expandedTeams.has(team.id) && (
                    <TableRow>
                      <TableCell colSpan={6} className="bg-slate-50">
                        <div className="p-4">
                          <h4 className="font-semibold mb-3 flex items-center gap-2">
                            <Users className="h-4 w-4" />
                            Drivers
                          </h4>
                          {!drivers[team.id] ? (
                            <div className="flex justify-center py-4">
                              <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
                            </div>
                          ) : drivers[team.id].length === 0 ? (
                            <p className="text-sm text-muted-foreground">No drivers in this team</p>
                          ) : (
                            <div className="space-y-2">
                              {drivers[team.id].map((driver) => (
                                <div
                                  key={driver.id}
                                  className="flex items-center justify-between bg-white p-3 rounded-lg"
                                >
                                  <div>
                                    <span className="font-medium">{driver.name}</span>
                                    <span className="text-sm text-muted-foreground ml-3">
                                      Weight: {driver.weight}kg
                                    </span>
                                  </div>
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => setDriverToDelete({ id: driver.id, teamId: team.id })}
                                  >
                                    <Trash2 className="h-4 w-4 text-destructive" />
                                  </Button>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      </TableCell>
                    </TableRow>
                  )}
                </React.Fragment>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Dialog open={isTeamDialogOpen} onOpenChange={setIsTeamDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{editingTeam ? "Edit Team" : "Add New Team"}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="name">Team Name *</Label>
              <Input
                id="name"
                value={teamForm.name}
                onChange={(e) => setTeamForm({ ...teamForm, name: e.target.value })}
                placeholder="Enter team name"
              />
            </div>
            <div>
              <Label htmlFor="category">Category *</Label>
              <Select
                value={teamForm.category}
                onValueChange={(value) => setTeamForm({ ...teamForm, category: value as TeamCategory })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(CATEGORY_LABELS).map(([value, label]) => (
                    <SelectItem key={value} value={value}>
                      {label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="vehicle_weight">Vehicle Weight (kg) *</Label>
                <Input
                  id="vehicle_weight"
                  type="number"
                  step="0.1"
                  value={teamForm.vehicle_weight}
                  onChange={(e) => setTeamForm({ ...teamForm, vehicle_weight: parseFloat(e.target.value) || 0 })}
                />
              </div>
              <div>
                <Label htmlFor="mean_power">Mean Power (W) *</Label>
                <Input
                  id="mean_power"
                  type="number"
                  step="0.1"
                  value={teamForm.mean_power}
                  onChange={(e) => setTeamForm({ ...teamForm, mean_power: parseFloat(e.target.value) || 0 })}
                />
              </div>
            </div>
            <div>
              <Label htmlFor="rfid_identifier">RFID Identifier *</Label>
              <Input
                id="rfid_identifier"
                value={teamForm.rfid_identifier}
                onChange={(e) => setTeamForm({ ...teamForm, rfid_identifier: e.target.value })}
                placeholder="Enter RFID identifier"
              />
            </div>

            {!editingTeam && (
              <>
                <div className="border-t pt-4">
                  <div className="flex items-center justify-between mb-3">
                    <Label>Drivers (Optional)</Label>
                    <Button type="button" variant="outline" size="sm" onClick={addDriverField}>
                      <Plus className="h-4 w-4 mr-1" />
                      Add Driver
                    </Button>
                  </div>
                  <div className="space-y-3">
                    {newDrivers.map((driver, index) => (
                      <div key={index} className="flex gap-2 items-end">
                        <div className="flex-1">
                          <Label htmlFor={`driver-name-${index}`}>Driver Name</Label>
                          <Input
                            id={`driver-name-${index}`}
                            value={driver.name}
                            onChange={(e) => updateDriverField(index, 'name', e.target.value)}
                            placeholder="Driver name"
                          />
                        </div>
                        <div className="w-32">
                          <Label htmlFor={`driver-weight-${index}`}>Weight (kg)</Label>
                          <Input
                            id={`driver-weight-${index}`}
                            type="number"
                            step="0.1"
                            value={driver.weight}
                            onChange={(e) => updateDriverField(index, 'weight', parseFloat(e.target.value) || 0)}
                            placeholder="Weight"
                          />
                        </div>
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          onClick={() => removeDriverField(index)}
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsTeamDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={editingTeam ? handleUpdateTeam : handleCreateTeam} disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              {editingTeam ? "Update Team" : "Create Team"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      <ConfirmDialog
        open={!!teamToDelete}
        onOpenChange={() => setTeamToDelete(null)}
        title="Delete Team"
        description="Are you sure you want to delete this team? All associated drivers will also be deleted."
        confirmLabel="Delete"
        destructive
        loading={isDeleting}
        onConfirm={handleDeleteTeam}
      />

      <ConfirmDialog
        open={!!driverToDelete}
        onOpenChange={() => setDriverToDelete(null)}
        title="Delete Driver"
        description="Are you sure you want to delete this driver?"
        confirmLabel="Delete"
        destructive
        loading={isDeleting}
        onConfirm={handleDeleteDriver}
      />
    </div>
  )
}
