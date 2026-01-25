"use client"
import { useState, useEffect } from "react"
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
import { Plus, Trash2, UserCog, Loader2 } from "lucide-react"
import { usersApi } from "@/lib/api/users"
import { toast } from "sonner"

interface User {
  id: string
  username: string
  email?: string
  enabled: boolean
  roles?: string[]
}

const AVAILABLE_ROLES = ["ADMIN", "TEAM_LEAD", "VIEWER"]

export default function UsersTab() {
  const [users, setUsers] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isAddUserOpen, setIsAddUserOpen] = useState(false)
  const [isEditUserOpen, setIsEditUserOpen] = useState(false)
  const [isManageRolesOpen, setIsManageRolesOpen] = useState(false)
  const [selectedUser, setSelectedUser] = useState<User | null>(null)
  const [isDeleting, setIsDeleting] = useState(false)

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  })
  const [selectedRoles, setSelectedRoles] = useState<string[]>([])
  useEffect(() => {
    loadUsers()
  }, [])

  const loadUsers = async () => {
    setIsLoading(true)
    try {
      const data = await usersApi.listUsers()
      setUsers(data)
    } catch (error: any) {
      toast.error(error.message || "Failed to load users")
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateUser = async () => {
    if (!formData.username || !formData.password) {
      toast.error("Username and password are required")
      return
    }

    setIsLoading(true)
    try {
      const newUser = await usersApi.createUser({
        username: formData.username,
        password: formData.password,
      })
      
      toast.success("User created successfully")
      
      setIsAddUserOpen(false)
      setFormData({ username: "", password: "" })
      
      loadUsers()
    } catch (error: any) {
      toast.error(error.message || "Failed to create user")
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpdateUser = async () => {
    if (!selectedUser) return

    setIsLoading(true)
    try {
      await usersApi.updateUser(selectedUser.id, {
        username: formData.username || undefined,
        password: formData.password || undefined,
      })
      
      toast.success("User updated successfully")
      
      setIsEditUserOpen(false)
      setFormData({ username: "", password: "" })
      loadUsers()
    } catch (error: any) {
      toast.error(error.message || "Failed to update user")
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteUser = async (userId: string) => {
    if (!confirm("Are you sure you want to delete this user?")) return

    setIsDeleting(true)
    try {
      await usersApi.deleteUser(userId)
      toast.success("User deleted successfully")
      loadUsers()
    } catch (error: any) {
      toast.error(error.message || "Failed to delete user")
    } finally {
      setIsDeleting(false)
    }
  }

  const handleManageRoles = (user: User) => {
    setSelectedUser(user)
    setSelectedRoles(user.roles || [])
    setIsManageRolesOpen(true)
  }

  const handleUpdateRoles = async () => {
    if (!selectedUser) return

    setIsLoading(true)
    try {
      const currentRoles = selectedUser.roles || []
      const rolesToAdd = selectedRoles.filter(r => !currentRoles.includes(r))
      const rolesToRemove = currentRoles.filter(r => !selectedRoles.includes(r))

      if (rolesToAdd.length > 0) {
        await usersApi.assignRoles(selectedUser.id, rolesToAdd)
      }
      if (rolesToRemove.length > 0) {
        await usersApi.removeRoles(selectedUser.id, rolesToRemove)
      }

      toast.success("Roles updated successfully")
      
      setIsManageRolesOpen(false)
    
      loadUsers()
    } catch (error: any) {
      toast.error(error.message || "Failed to update roles")
    } finally {
      setIsLoading(false)
    }
  }

  const openEditDialog = (user: User) => {
    setSelectedUser(user)
    setFormData({ username: user.username, password: "" })
    setIsEditUserOpen(true)
  }

  const toggleRole = (role: string) => {
    setSelectedRoles(prev =>
      prev.includes(role)
        ? prev.filter(r => r !== role)
        : [...prev, role]
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">User Management</h2>
        <Button
          onClick={() => {
            setFormData({ username: "", password: "" })
            setIsAddUserOpen(true)
          }}
          className="flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          <span>Add User</span>
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Users</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Username</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Roles</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {users.length === 0 && (
                <TableRow>
                  <TableCell
                    colSpan={5}
                    className="text-center text-muted-foreground"
                  >
                    No users found. Add a user to get started.
                  </TableCell>
                </TableRow>
              )}
              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell className="font-medium">{user.username}</TableCell>
                  <TableCell>{user.email || "N/A"}</TableCell>
                  <TableCell>
                    <div className="flex gap-1 flex-wrap">
                      {user.roles && user.roles.length > 0 ? (
                        user.roles.map((role) => (
                          <Badge key={role} variant="outline" className="capitalize">
                            {role}
                          </Badge>
                        ))
                      ) : (
                        <span className="text-sm text-muted-foreground">No roles</span>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant={user.enabled ? "secondary" : "destructive"}>
                      {user.enabled ? "Active" : "Disabled"}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => openEditDialog(user)}
                      >
                        Edit
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleManageRoles(user)}
                      >
                        <UserCog className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDeleteUser(user.id)}
                        disabled={isDeleting}
                      >
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Dialog open={isAddUserOpen} onOpenChange={setIsAddUserOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New User</DialogTitle>
            <DialogDescription>
              Create a new user account in Keycloak
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                value={formData.username}
                onChange={(e) =>
                  setFormData({ ...formData, username: e.target.value })
                }
                placeholder="Enter username"
              />
            </div>
            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
                placeholder="Enter password"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsAddUserOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleCreateUser} disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Create User
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={isEditUserOpen} onOpenChange={setIsEditUserOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit User</DialogTitle>
            <DialogDescription>
              Update user information
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="edit-username">Username</Label>
              <Input
                id="edit-username"
                value={formData.username}
                onChange={(e) =>
                  setFormData({ ...formData, username: e.target.value })
                }
                placeholder="Enter username"
              />
            </div>
            <div>
              <Label htmlFor="edit-password">Password (leave empty to keep current)</Label>
              <Input
                id="edit-password"
                type="password"
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
                placeholder="Enter new password"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsEditUserOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleUpdateUser} disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Update User
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={isManageRolesOpen} onOpenChange={setIsManageRolesOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Manage User Roles</DialogTitle>
            <DialogDescription>
              Assign or remove roles for {selectedUser?.username}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            {AVAILABLE_ROLES.map((role) => (
              <div key={role} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id={`role-${role}`}
                  checked={selectedRoles.includes(role)}
                  onChange={() => toggleRole(role)}
                  className="h-4 w-4"
                />
                <Label htmlFor={`role-${role}`} className="capitalize">
                  {role}
                </Label>
              </div>
            ))}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsManageRolesOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleUpdateRoles} disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Update Roles
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}