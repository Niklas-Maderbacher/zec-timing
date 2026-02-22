"use client"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
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
import { Badge } from "@/components/ui/badge"
import { Plus, Edit, Trash2, Loader2, Users, Trophy, Zap, Weight } from "lucide-react"
import { ConfirmDialog } from "@/components/dialogs/confirm-dialog"
import { teamsApi, type Team, type TeamUpdate, TeamCategory } from "@/lib/api/teams"
import { driversApi, type Driver } from "@/lib/api/drivers"
import { usersApi } from "@/lib/api/users"
import { toast } from "sonner"

const CATEGORY_LABELS: Record<TeamCategory, string> = {
  [TeamCategory.CLOSE_TO_SERIES]: "Close to Series",
  [TeamCategory.ADVANCED_CLASS]: "Advanced Class",
  [TeamCategory.PROFESSIONAL_CLASS]: "Professional Class",
}

export default function TeamLeadView() {
  const [team, setTeam] = useState<Team | null>(null)
  const [drivers, setDrivers] = useState<Driver[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isEditTeamOpen, setIsEditTeamOpen] = useState(false)
  const [isAddDriverOpen, setIsAddDriverOpen] = useState(false)
  const [isEditDriverOpen, setIsEditDriverOpen] = useState(false)
  const [editingDriver, setEditingDriver] = useState<Driver | null>(null)
  const [driverToDelete, setDriverToDelete] = useState<Driver | null>(null)
  const [isDeleting, setIsDeleting] = useState(false)

  const [teamForm, setTeamForm] = useState<TeamUpdate>({
    name: "",
    vehicle_weight: 0,
    mean_power: 0,
    rfid_identifier: "",
  })

  const [driverForm, setDriverForm] = useState({
    name: "",
    weight: 0,
  })

  useEffect(() => {
    loadTeamData()
  }, [])

  const loadTeamData = async () => {
    setIsLoading(true)
    try {
      const currentUser = await usersApi.getCurrentUser()
      if (!currentUser?.team_id) {
        setTeam(null)
        setIsLoading(false)
        return
      }

      const teamData = await teamsApi.getTeamById(parseInt(currentUser.team_id))
      setTeam(teamData)
      
      const driversData = await driversApi.getDriversByTeam(teamData.id)
      setDrivers(driversData)
    } catch (error: any) {
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  const openEditTeam = () => {
    if (!team) return
    setTeamForm({
      name: team.name,
      vehicle_weight: team.vehicle_weight,
      mean_power: team.mean_power,
      rfid_identifier: team.rfid_identifier,
    })
    setIsEditTeamOpen(true)
  }

  const handleUpdateTeam = async () => {
    if (!team) return

    setIsLoading(true)
    try {
      await teamsApi.updateTeam(team.id, teamForm)
      toast.success("Team updated successfully")
      setIsEditTeamOpen(false)
      loadTeamData()
    } catch (error: any) {
      toast.error("Failed to update team")
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddDriver = async () => {
    if (!team || !driverForm.name) {
      toast.error("Driver name is required")
      return
    }

    setIsLoading(true)
    try {
      await driversApi.createDriver({
        name: driverForm.name,
        weight: driverForm.weight,
        team_id: team.id,
      })
      toast.success("Driver added successfully")
      setIsAddDriverOpen(false)
      setDriverForm({ name: "", weight: 0 })
      loadTeamData()
    } catch (error: any) {
      toast.error(error.message || "Failed to add driver")
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpdateDriver = async () => {
    if (!editingDriver) return

    setIsLoading(true)
    try {
      await driversApi.updateDriver(editingDriver.id, {
        name: driverForm.name,
        weight: driverForm.weight,
      })
      toast.success("Driver updated successfully")
      setIsEditDriverOpen(false)
      setEditingDriver(null)
      setDriverForm({ name: "", weight: 0 })
      loadTeamData()
    } catch (error: any) {
      toast.error(error.message || "Failed to update driver")
    } finally {
      setIsLoading(false)
    }
  }

  const confirmDeleteDriver = async () => {
    if (!driverToDelete) return

    setIsDeleting(true)
    try {
      await driversApi.deleteDriver(driverToDelete.id)
      toast.success("Driver removed successfully")
      setDriverToDelete(null)
      loadTeamData()
    } catch (error: any) {
      toast.error("Driver has attemps made")
    } finally {
      setIsDeleting(false)
    }
  }

  const openEditDriver = (driver: Driver) => {
    setEditingDriver(driver)
    setDriverForm({
      name: driver.name,
      weight: driver.weight,
    })
    setIsEditDriverOpen(true)
  }

  if (isLoading && !team) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    )
  }

  if (!team) {
    return (
      <div className="flex items-center justify-center h-96">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>No Team Assigned</CardTitle>
            <CardDescription>
              You are not currently assigned to any team. Please contact an administrator to assign you to a team.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold">{team.name}</h2>
      </div>

      <Card className="border-2">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
          <div>
            <CardTitle className="text-2xl">Team Details</CardTitle>
          </div>
          <Button onClick={openEditTeam}>
            <Edit className="h-4 w-4 mr-2" />
            Edit Team
          </Button>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Trophy className="h-4 w-4" />
                <span className="text-sm font-medium">Category</span>
              </div>
              <Badge className="text-base px-3 py-1">
                {CATEGORY_LABELS[team.category]}
              </Badge>
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Weight className="h-4 w-4" />
                <span className="text-sm font-medium">Vehicle Weight</span>
              </div>
              <p className="text-2xl font-bold">{team.vehicle_weight} kg</p>
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Zap className="h-4 w-4" />
                <span className="text-sm font-medium">Mean Power</span>
              </div>
              <p className="text-2xl font-bold">{team.mean_power} W</p>
            </div>

            <div className="space-y-2">
              <div className="text-sm font-medium text-muted-foreground">RFID Identifier</div>
              <p className="text-lg font-mono font-semibold">{team.rfid_identifier}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="border-2">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
          <div>
            <CardTitle className="text-2xl flex items-center gap-2">
              <Users className="h-6 w-6" />
              Team Drivers
            </CardTitle>
          </div>
          <Button onClick={() => setIsAddDriverOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Add Driver
          </Button>
        </CardHeader>
        <CardContent>
          {drivers.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              <Users className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p className="text-lg font-medium">No drivers yet</p>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {drivers.map((driver) => (
                <Card key={driver.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="pt-6">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h3 className="font-bold text-lg">{driver.name}</h3>
                        <p className="text-sm text-muted-foreground">
                          Weight: {driver.weight} kg
                        </p>
                      </div>
                      <div className="flex gap-1">
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => openEditDriver(driver)}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => setDriverToDelete(driver)}
                        >
                          <Trash2 className="h-4 w-4 text-destructive" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <Dialog open={isEditTeamOpen} onOpenChange={setIsEditTeamOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Team Details</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="team-name">Team Name</Label>
              <Input
                id="team-name"
                value={teamForm.name}
                onChange={(e) => setTeamForm({ ...teamForm, name: e.target.value })}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="weight">Vehicle Weight (kg)</Label>
                <Input
                  id="weight"
                  type="number"
                  step="0.1"
                  value={teamForm.vehicle_weight}
                  onChange={(e) =>
                    setTeamForm({ ...teamForm, vehicle_weight: parseFloat(e.target.value) || 0 })
                  }
                />
              </div>
              <div>
                <Label htmlFor="power">Mean Power (W)</Label>
                <Input
                  id="power"
                  type="number"
                  step="0.1"
                  value={teamForm.mean_power}
                  onChange={(e) =>
                    setTeamForm({ ...teamForm, mean_power: parseFloat(e.target.value) || 0 })
                  }
                />
              </div>
            </div>
            <div>
              <Label htmlFor="rfid">RFID Identifier</Label>
              <Input
                id="rfid"
                value={teamForm.rfid_identifier}
                onChange={(e) => setTeamForm({ ...teamForm, rfid_identifier: e.target.value })}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsEditTeamOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleUpdateTeam} disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Save Changes
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={isAddDriverOpen} onOpenChange={setIsAddDriverOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New Driver</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="driver-name">Driver Name</Label>
              <Input
                id="driver-name"
                value={driverForm.name}
                onChange={(e) => setDriverForm({ ...driverForm, name: e.target.value })}
                placeholder="Enter driver name"
              />
            </div>
            <div>
              <Label htmlFor="driver-weight">Weight (kg)</Label>
              <Input
                id="driver-weight"
                type="number"
                step="0.1"
                value={driverForm.weight}
                onChange={(e) =>
                  setDriverForm({ ...driverForm, weight: parseFloat(e.target.value) || 0 })
                }
                placeholder="Enter driver weight"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsAddDriverOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleAddDriver} disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Add Driver
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={isEditDriverOpen} onOpenChange={setIsEditDriverOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Driver</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="edit-driver-name">Driver Name</Label>
              <Input
                id="edit-driver-name"
                value={driverForm.name}
                onChange={(e) => setDriverForm({ ...driverForm, name: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="edit-driver-weight">Weight (kg)</Label>
              <Input
                id="edit-driver-weight"
                type="number"
                step="0.1"
                value={driverForm.weight}
                onChange={(e) =>
                  setDriverForm({ ...driverForm, weight: parseFloat(e.target.value) || 0 })
                }
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsEditDriverOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleUpdateDriver} disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Save Changes
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={!!driverToDelete}
        onOpenChange={() => setDriverToDelete(null)}
        title="Delete Driver"
        description={`Are you sure you want to remove ${driverToDelete?.name} from the team?`}
        confirmLabel="Delete"
        destructive
        loading={isDeleting}
        onConfirm={confirmDeleteDriver}
      />
    </div>
  )
}