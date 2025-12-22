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
import { Badge } from "@/components/ui/badge"
import { Plus } from "lucide-react"

interface Props {
  users: any[]
  setIsAddUserOpen: (open: boolean) => void
  handleEditUser: (user: any) => void
  toggleUserStatus: (id: string | number) => void
  getTeamName: (id: string | number | undefined) => string
}

export default function UsersTab({
  users,
  setIsAddUserOpen,
  handleEditUser,
  toggleUserStatus,
  getTeamName,
}: Props) {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">User Management</h2>

        <Button
          onClick={() => setIsAddUserOpen(true)}
          className="flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          <span>Add User</span>
        </Button>
      </div>

      {/* Users Table */}
      <Card>
        <CardHeader>
          <CardTitle>All Users</CardTitle>
        </CardHeader>

        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Username</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Team</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">
                  Actions
                </TableHead>
              </TableRow>
            </TableHeader>

            <TableBody>
              {users.length === 0 && (
                <TableRow>
                  <TableCell
                    colSpan={5}
                    className="text-center text-muted-foreground"
                  >
                    No users found.
                  </TableCell>
                </TableRow>
              )}

              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>{user.username}</TableCell>

                  <TableCell>{user.role}</TableCell>

                  <TableCell>
                    {user.assignedTeam
                      ? getTeamName(user.assignedTeam)
                      : "N/A"}
                  </TableCell>

                  <TableCell>
                    <Badge
                      variant={
                        user.status === "active"
                          ? "secondary"
                          : "destructive"
                      }
                    >
                      {user.status}
                    </Badge>
                  </TableCell>

                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleEditUser(user)}
                      >
                        Edit
                      </Button>

                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() =>
                          toggleUserStatus(user.id)
                        }
                      >
                        {user.status === "active"
                          ? "Deactivate"
                          : "Activate"}
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
