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
import { User, Users, UserCog, Download, Trophy, Swords } from "lucide-react"
import Footer from "@/components/footer/footer"

export type Tabs =
  | "leaderboard"
  | "teams"
  | "drivers"
  | "challenges"
  | "users"
  | "export"
  | "config"

interface MainLayoutProps {
  activeTab: Tabs
  setActiveTab: (tab: Tabs) => void
  children: ReactNode
}

export function SideBarLayout({ activeTab, setActiveTab, children }: MainLayoutProps) {
  const [open, setOpen] = useState(false)
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
              <SidebarMenuItem>
                <SidebarMenuButton
                  tooltip="Leaderboard"
                  isActive={activeTab === "leaderboard"}
                  onClick={() => setActiveTab("leaderboard")}
                >
                  <Trophy />
                  <span>Leaderboard</span>
                </SidebarMenuButton>
              </SidebarMenuItem>

              <SidebarMenuItem>
                <SidebarMenuButton
                  tooltip="Teams"
                  isActive={activeTab === "teams"}
                  onClick={() => setActiveTab("teams")}
                >
                  <Users />
                  <span>Teams</span>
                </SidebarMenuButton>
              </SidebarMenuItem>

              <SidebarMenuItem>
                <SidebarMenuButton
                  tooltip="Drivers"
                  isActive={activeTab === "drivers"}
                  onClick={() => setActiveTab("drivers")}
                >
                  <User />
                  <span>Drivers</span>
                </SidebarMenuButton>
              </SidebarMenuItem>

              <SidebarMenuItem>
                <SidebarMenuButton
                  tooltip="Challenges"
                  isActive={activeTab === "challenges"}
                  onClick={() => setActiveTab("challenges")}
                >
                  <Swords />
                  <span>Challenges</span>
                </SidebarMenuButton>
              </SidebarMenuItem>

              <SidebarMenuItem>
                <SidebarMenuButton
                  tooltip="Users"
                  isActive={activeTab === "users"}
                  onClick={() => setActiveTab("users")}
                >
                  <UserCog />
                  <span>Users</span>
                </SidebarMenuButton>
              </SidebarMenuItem>

              <SidebarMenuItem>
                <SidebarMenuButton
                  tooltip="Export"
                  isActive={activeTab === "export"}
                  onClick={() => setActiveTab("export")}
                >
                  <Download />
                  <span>Export</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
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
