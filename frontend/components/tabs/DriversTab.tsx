"use client"

import { Dispatch, SetStateAction } from "react"
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
  CardHeader,
  CardContent,
  CardTitle,
} from "@/components/ui/card"
import { Edit, Trash2, Plus } from "lucide-react"

interface Props {
  drivers: any[]
  setDrivers: Dispatch<SetStateAction<any[]>>
  setIsAddDriverOpen: (open: boolean) => void
  setEditingDriver: (d: any) => void
}

export default function DriversTab({
  drivers,
  setDrivers,
  setIsAddDriverOpen,
  setEditingDriver,
}: Props) {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Driver Management</h2>
        <Button
          onClick={() => setIsAddDriverOpen(true)}
          className="flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          <span>Add Driver</span>
        </Button>
      </div>

      {/* Table */}
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
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>

            <TableBody>
              {drivers.length === 0 && (
                <TableRow>
                  <TableCell
                    colSpan={5}
                    className="text-center text-muted-foreground"
                  >
                    No drivers found.
                  </TableCell>
                </TableRow>
              )}

              {drivers.map((driver) => (
                <TableRow key={driver.id}>
                  <TableCell className="font-medium">
                    {driver.name}
                  </TableCell>

                  <TableCell>{driver.teamName}</TableCell>

                  <TableCell>{driver.bestLapTime}</TableCell>

                  <TableCell>
                    <span
                      className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${
                        driver.status === "Active"
                          ? "bg-green-100 text-green-800"
                          : "bg-red-100 text-red-800"
                      }`}
                    >
                      {driver.status}
                    </span>
                  </TableCell>

                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => setEditingDriver(driver)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>

                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() =>
                          setDrivers(
                            drivers.filter((d) => d.id !== driver.id)
                          )
                        }
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
