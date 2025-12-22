"use client"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select"
import { Download } from "lucide-react"

interface Props {
  exportFormat: string
  setExportFormat: (f: string) => void
  exportDateRange: { from: string; to: string }
  setExportDateRange: (r: { from: string; to: string }) => void
  handleExport: () => void
}

export default function ExportTab({
  exportFormat,
  setExportFormat,
  exportDateRange,
  setExportDateRange,
  handleExport,
}: Props) {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Data Export</h2>

      <div className="grid gap-4 md:grid-cols-2">
        {/* Leaderboard Export */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">
              Leaderboard Export
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label>Format</Label>
              <Select
                value={exportFormat}
                onValueChange={setExportFormat}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="csv">CSV</SelectItem>
                  <SelectItem value="pdf">PDF</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <Button className="w-full" onClick={handleExport}>
              <Download className="mr-2 h-4 w-4" />
              Export Leaderboard
            </Button>
          </CardContent>
        </Card>

        {/* Race Data Export */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">
              Race Data Export
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label>Date Range</Label>
              <Select
                defaultValue="today"
                onValueChange={(value) =>
                  setExportDateRange({
                    from:
                      value === "today"
                        ? new Date().toISOString()
                        : "",
                    to:
                      value === "today"
                        ? new Date().toISOString()
                        : "",
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

            <Button className="w-full" onClick={handleExport}>
              <Download className="mr-2 h-4 w-4" />
              Export Race Data
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
