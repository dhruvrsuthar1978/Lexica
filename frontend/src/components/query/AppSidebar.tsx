import { useState } from "react"
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
} from "@/components/ui/sidebar"
import { Button } from "@/components/ui/button"
import { Database, History, DatabaseZap } from "lucide-react"
import { SchemaPanel } from "./SchemaPanel"
import { QueryHistory } from "./QueryHistory"
import { cn } from "@/lib/utils"

type AppSidebarProps = {
  variant?: 'sidebar' | 'floating' | 'inset'
}

export function AppSidebar({ variant }: AppSidebarProps) {
  const [activeTab, setActiveTab] = useState<'schema' | 'history'>('schema')

  return (
    <Sidebar variant={variant}>
      <SidebarHeader className="px-4 pt-5 pb-4 border-b border-border bg-sidebar">
        <div className="flex items-center gap-3 mb-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-lg shadow-primary/20">
            <DatabaseZap className="h-6 w-6" />
          </div>
          <div className="flex flex-col">
            <span className="font-black text-lg tracking-tighter text-gradient">EXPLORER</span>
            <span className="text-[10px] font-black text-primary uppercase tracking-[0.2em] opacity-80">v3.0 CORE</span>
          </div>
        </div>
        <div className="flex p-1 bg-muted rounded-xl gap-1 border border-border">
          <Button
            variant={activeTab === 'schema' ? 'secondary' : 'ghost'}
            size="sm"
            className={cn(
              "flex-1 gap-1.5 h-9 text-[10px] font-black uppercase tracking-wider transition-all rounded-lg",
              activeTab === 'schema'
                ? "bg-background dark:bg-secondary shadow-sm text-primary border border-primary/20"
                : "text-muted-foreground hover:text-foreground"
            )}
            onClick={() => setActiveTab('schema')}
          >
            <Database className="h-3.5 w-3.5 shrink-0" />
            Schema
          </Button>
          <Button
            variant={activeTab === 'history' ? 'secondary' : 'ghost'}
            size="sm"
            className={cn(
              "flex-1 gap-1.5 h-9 text-[10px] font-black uppercase tracking-wider transition-all rounded-lg",
              activeTab === 'history'
                ? "bg-background dark:bg-secondary shadow-sm text-primary border border-primary/20"
                : "text-muted-foreground hover:text-foreground"
            )}
            onClick={() => setActiveTab('history')}
          >
            <History className="h-3.5 w-3.5 shrink-0" />
            History
          </Button>
        </div>
      </SidebarHeader>
      <SidebarContent className="bg-sidebar">
        {activeTab === 'schema' ? <SchemaPanel /> : <QueryHistory />}
      </SidebarContent>
    </Sidebar>
  )
}
