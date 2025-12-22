"use client"

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
import { Edit, Trash2, Plus } from "lucide-react"

interface Team {
  id: string | number
  name: string
  country?: string
  drivers?: number
  bestLapTime?: string
  points?: number
  podiums?: number
}

interface Props {
  visibleTeams: Team[]
  setIsAddTeamOpen: (open: boolean) => void
  setEditingTeam: (t: Team | null) => void
  handleDeleteTeam: (id: string | number) => void
}

export default function TeamsTab({
  visibleTeams,
  setIsAddTeamOpen,
  setEditingTeam,
  handleDeleteTeam,
}: Props) {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Race Teams</h2>

        <Button
          onClick={() => setIsAddTeamOpen(true)}
          className="flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          <span>Add Team</span>
        </Button>
      </div>

      {/* Teams Table */}
      <Card>
        <CardHeader>
          <CardTitle>All Teams</CardTitle>
        </CardHeader>

        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Team Name</TableHead>
                <TableHead>Country</TableHead>
                <TableHead>Drivers</TableHead>
                <TableHead>Points</TableHead>
                <TableHead className="text-right">
                  Actions
                </TableHead>
              </TableRow>
            </TableHeader>

            <TableBody>
              {visibleTeams.length === 0 && (
                <TableRow>
                  <TableCell
                    colSpan={5}
                    className="text-center text-muted-foreground"
                  >
                    No teams found.
                  </TableCell>
                </TableRow>
              )}

              {visibleTeams.map((team) => (
                <TableRow key={team.id}>
                  <TableCell className="font-medium">
                    {team.name}
                  </TableCell>

                  <TableCell>{team.country ?? "—"}</TableCell>

                  <TableCell>{team.drivers ?? 0}</TableCell>

                  <TableCell>{team.points ?? 0}</TableCell>

                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => setEditingTeam(team)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>

                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => handleDeleteTeam(team.id)}
                        className="text-red-600 hover:text-red-700"
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
    </div>
  )
}
