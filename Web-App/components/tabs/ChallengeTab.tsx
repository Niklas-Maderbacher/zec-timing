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
import { Edit, Loader2 } from "lucide-react"
import { challengesApi, type Challenge, type ChallengeUpdate } from "@/lib/api/challenges"
import { toast } from "sonner"

export default function ChallengeTab() {
  const [challenges, setChallenges] = useState<Challenge[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isEditChallengeOpen, setIsEditChallengeOpen] = useState(false)
  const [editingChallenge, setEditingChallenge] = useState<Challenge | null>(null)

  const [formData, setFormData] = useState<ChallengeUpdate>({
    name: undefined,
    max_attempts: null,
    esp_mac_start1: null,
    esp_mac_start2: null,
    esp_mac_finish1: null,
    esp_mac_finish2: null,
  })

  useEffect(() => {
    loadChallenges()
  }, [])

  const loadChallenges = async () => {
    setIsLoading(true)
    try {
      const data = await challengesApi.listChallenges()
      setChallenges(data)
    } catch (error: any) {
      toast.error(error.message || "Failed to load challenges")
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpdateChallenge = async () => {
    if (!editingChallenge) return

    setIsLoading(true)
    try {
      await challengesApi.updateChallenge(editingChallenge.id, formData)
      toast.success("Challenge updated successfully")
      setIsEditChallengeOpen(false)
      setEditingChallenge(null)
      loadChallenges()
    } catch (error: any) {
      toast.error(error.message || "Failed to update challenge")
    } finally {
      setIsLoading(false)
    }
  }

  const openEditDialog = (challenge: Challenge) => {
    setEditingChallenge(challenge)
    setFormData({
      name: challenge.name,
      max_attempts: challenge.max_attempts,
      esp_mac_start1: challenge.esp_mac_start1,
      esp_mac_start2: challenge.esp_mac_start2,
      esp_mac_finish1: challenge.esp_mac_finish1,
      esp_mac_finish2: challenge.esp_mac_finish2,
    })
    setIsEditChallengeOpen(true)
  }

  const formatDate = (d?: string | null) => 
    d ? new Date(d).toLocaleString() : "—"

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Challenge Management</h2>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Challenges</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Max Attempts</TableHead>
                <TableHead>Start MACs</TableHead>
                <TableHead>Finish MACs</TableHead>
                <TableHead>Created</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {challenges.length === 0 && (
                <TableRow>
                  <TableCell
                    colSpan={6}
                    className="text-center text-muted-foreground"
                  >
                    No challenges found.
                  </TableCell>
                </TableRow>
              )}
              {challenges.map((c) => (
                <TableRow key={c.id}>
                  <TableCell className="font-medium">{c.name}</TableCell>
                  <TableCell>{c.max_attempts ?? "—"}</TableCell>
                  <TableCell>
                    {[c.esp_mac_start1, c.esp_mac_start2]
                      .filter(Boolean)
                      .join(", ") || "—"}
                  </TableCell>
                  <TableCell>
                    {[c.esp_mac_finish1, c.esp_mac_finish2]
                      .filter(Boolean)
                      .join(", ") || "—"}
                  </TableCell>
                  <TableCell>{formatDate(c.created_at)}</TableCell>
                  <TableCell className="text-right">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => openEditDialog(c)}
                    >
                      <Edit className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Dialog open={isEditChallengeOpen} onOpenChange={setIsEditChallengeOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Edit Challenge</DialogTitle>
            <DialogDescription>
              Update challenge information
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="edit-name">Challenge Name</Label>
              <Input
                id="edit-name"
                value={formData.name || ""}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
                placeholder="Enter challenge name"
              />
            </div>
            <div>
              <Label htmlFor="edit-max_attempts">Max Attempts</Label>
              <Input
                id="edit-max_attempts"
                type="number"
                value={formData.max_attempts || ""}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    max_attempts: e.target.value ? parseInt(e.target.value) : null,
                  })
                }
                placeholder="Leave empty for unlimited"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="edit-esp_mac_start1">Start MAC 1</Label>
                <Input
                  id="edit-esp_mac_start1"
                  value={formData.esp_mac_start1 || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      esp_mac_start1: e.target.value || null,
                    })
                  }
                  placeholder="AA:BB:CC:DD:EE:FF"
                />
              </div>
              <div>
                <Label htmlFor="edit-esp_mac_start2">Start MAC 2</Label>
                <Input
                  id="edit-esp_mac_start2"
                  value={formData.esp_mac_start2 || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      esp_mac_start2: e.target.value || null,
                    })
                  }
                  placeholder="AA:BB:CC:DD:EE:FF"
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="edit-esp_mac_finish1">Finish MAC 1</Label>
                <Input
                  id="edit-esp_mac_finish1"
                  value={formData.esp_mac_finish1 || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      esp_mac_finish1: e.target.value || null,
                    })
                  }
                  placeholder="AA:BB:CC:DD:EE:FF"
                />
              </div>
              <div>
                <Label htmlFor="edit-esp_mac_finish2">Finish MAC 2</Label>
                <Input
                  id="edit-esp_mac_finish2"
                  value={formData.esp_mac_finish2 || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      esp_mac_finish2: e.target.value || null,
                    })
                  }
                  placeholder="AA:BB:CC:DD:EE:FF"
                />
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setIsEditChallengeOpen(false)}
            >
              Cancel
            </Button>
            <Button onClick={handleUpdateChallenge} disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Update Challenge
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
