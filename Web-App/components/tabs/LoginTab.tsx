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
import { User } from "lucide-react"
import { AuthService } from "@/lib/auth"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface User {
  id: string
  username: string
  role: string
}

interface Props {
  isLoggedIn: boolean
  user: User | null
  onLoginSuccess: (user: User) => void
  onLogout: () => void
}

export default function LoginTab({ isLoggedIn, user, onLoginSuccess, onLogout }: Props) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setIsLoading(true)
    try {
      const tokenData = await AuthService.login(username, password)
      const role = AuthService.getUserRole(tokenData.access_token)
      const userUsername = AuthService.getUsername(tokenData.access_token)
      const userData: User = {
        id: userUsername || username,
        username: userUsername || username,
        role: role || "no role",
      }
      onLoginSuccess(userData)
      setUsername("")
      setPassword("")
    } catch (err: any) {
      setError(err.message || "Login failed. Please check your credentials.")
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoggedIn && user) {
    return (
      <div className="container mx-auto p-6 max-w-2xl">
        <Card>
          <CardHeader>
            <CardTitle>Account Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <Label className="text-sm font-medium">Username</Label>
              <p className="text-lg">{user.username}</p>
            </div>
            <div>
              <Label className="text-sm font-medium">Role</Label>
              <p className="text-lg capitalize">{user.role}</p>
            </div>
            <Button onClick={onLogout} variant="destructive" className="w-full">
              Logout
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6 max-w-md">
      <Card>
        <CardHeader>
          <CardTitle>Login</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
            
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                required
                disabled={isLoading}
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
                disabled={isLoading}
              />
            </div>
            
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? "Logging in..." : "Login"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
