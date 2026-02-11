"use client"
import Image from "next/image"
import { useState, type ReactNode } from "react"
import {
  Sidebar,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"
import { FolderClosed, Users, UserCog, Download, Trophy, Swords, CircleUser } from "lucide-react"
import Footer from "@/components/footer/footer"
import { canAccessTab } from "@/lib/permissions"

export type Tabs =
  | "leaderboard"
  | "attempts"
  | "teams"
  | "drivers"
  | "challenges"
  | "users"
  | "export"
  | "login"

interface TabConfig {
  id: Tabs
  label: string
  icon: any
  tooltip: string
}

const allTabs: TabConfig[] = [
  { id: "leaderboard", label: "Leaderboard", icon: Trophy, tooltip: "Leaderboard" },
  { id: "attempts", label: "Attempts", icon: FolderClosed, tooltip: "Attempts" },
  { id: "teams", label: "Teams", icon: Users, tooltip: "Teams" },
  { id: "challenges", label: "Challenges", icon: Swords, tooltip: "Challenges" },
  { id: "users", label: "Users", icon: UserCog, tooltip: "Users" },
  { id: "export", label: "Export", icon: Download, tooltip: "Export" },
  { id: "login", label: "Account", icon: CircleUser, tooltip: "Account" },
]

interface MainLayoutProps {
  activeTab: Tabs
  setActiveTab: (tab: Tabs) => void
  children: ReactNode
  userRole?: string | null
}

export function SideBarLayout({ activeTab, setActiveTab, children, userRole }: MainLayoutProps) {
  const [open, setOpen] = useState(false)
  const visibleTabs = allTabs.filter(tab => canAccessTab(userRole ?? null, tab.id))

  return (
    <SidebarProvider open={open} onOpenChange={setOpen}>
      <div className="flex min-h-screen w-full flex-col">
        <div className="flex flex-1 w-full">
          <Sidebar collapsible="icon" className="border-r">
            <SidebarHeader className="px-4 py-3 group-data-[collapsible=icon]:pl-2">
              <div className="flex items-center gap-2 group-data-[collapsible=icon]:pl-1">
                <span className="size-4 shrink-0 hidden group-data-[collapsible=icon]:block">
                  <Image src="/ZEC-icon.png" alt="ZEC Icon" width={16} height={16} className="object-contain" priority />
                </span>
                <span className="text-xl font-semibold group-data-[collapsible=icon]:hidden">ZEC-Timing</span>
              </div>
            </SidebarHeader>
            <SidebarMenu>
              {visibleTabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <SidebarMenuItem key={tab.id}>
                    <SidebarMenuButton
                      tooltip={tab.tooltip}
                      isActive={activeTab === tab.id}
                      onClick={() => setActiveTab(tab.id)}
                    >
                      <Icon />
                      <span>{tab.label}</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                )
              })}
            </SidebarMenu>
          </Sidebar>

          <div className="flex flex-col flex-1">
            <main className="flex-1 p-6">
              <div className="mb-4 flex items-center justify-between">
                <SidebarTrigger />
                <div className="flex items-center gap-4">
                  <div className="relative h-12 w-[100px]">
                    <Image
                      src="/Logo_HTL_100.png"
                      alt="Logo HTL"
                      fill
                      className="object-contain"
                      priority
                    />
                  </div>

                  <div className="relative h-14 w-[140px]">
                    <Image
                      src="/ZEC-Logo.png"
                      alt="ZEC Logo"
                      fill
                      className="object-contain"
                      priority
                    />
                  </div>
                </div>
              </div>

              {children}
            </main>
          </div>
        </div>
        <Footer />
      </div>
    </SidebarProvider>
  )
}
