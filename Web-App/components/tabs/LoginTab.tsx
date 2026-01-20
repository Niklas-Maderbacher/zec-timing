"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

interface User {
  id: string | number
  username: string
  role: string
}

interface Props {
  isLoggedIn: boolean
  user: User | null
  onLogin: (username: string, password: string) => void
  onLogout: () => void
}

export default function LoginTab({
  isLoggedIn,
  user,
  onLogin,
  onLogout,
}: Props) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  if (!isLoggedIn) {
    return (
      <div className="flex justify-center pt-12">
        <Card className="w-full max-w-sm">
          <CardHeader>
            <CardTitle>Login</CardTitle>
          </CardHeader>

          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <Button
              className="w-full"
              onClick={() => onLogin(username, password)}
            >
              Sign In
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6 pt-6">
      <Card>
        <CardHeader>
          <CardTitle>Account</CardTitle>
        </CardHeader>

        <CardContent className="space-y-3">
          <div className="flex justify-between">
            <span className="text-muted-foreground">
              Username
            </span>
            <span>{user?.username}</span>
          </div>

          <div className="flex justify-between">
            <span className="text-muted-foreground">
              Role
            </span>
            <span>{user?.role}</span>
          </div>

          <Button
            variant="outline"
            className="w-full"
            onClick={onLogout}
          >
            Logout
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
