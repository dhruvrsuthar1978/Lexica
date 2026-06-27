import { Moon, Sun, Settings, DatabaseZap } from 'lucide-react';
import { useTheme } from '../theme-provider';
import { useStore } from '@/store/useStore';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { cn } from '@/lib/utils';

export function Navbar() {
  const { setTheme } = useTheme();
  const dbStatus = useStore((state) => state.dbStatus);

  return (
    <header className="sticky top-0 z-40 w-full bg-white/30 dark:bg-black/40 backdrop-blur-xl border-b border-white/50 dark:border-white/10">
      <div className="container flex h-16 items-center justify-between px-4 sm:px-8 max-w-7xl mx-auto">
        <div className="flex items-center gap-3 group cursor-pointer">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary text-primary-foreground shadow-lg shadow-primary/20 transition-transform group-hover:scale-110 group-hover:rotate-3 duration-300">
            <DatabaseZap className="h-6 w-6" />
          </div>
          <span className="text-xl font-black tracking-tighter text-gradient hidden sm:inline-block">
            Lexica
          </span>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Badge
              variant="outline"
              className={cn(
                "flex items-center gap-2 px-3 py-1.5 font-bold transition-all rounded-full border-white/40 dark:border-white/10 shadow-sm crystal neon-glow-primary",
                dbStatus === 'connected'
                  ? "text-primary"
                  : "text-destructive"
              )}
            >
              <div className={cn(
                "h-2 w-2 rounded-full",
                dbStatus === 'connected'
                  ? "bg-primary shadow-[0_0_8px_rgba(167,139,250,0.8)] animate-pulse"
                  : "bg-destructive shadow-[0_0_8px_rgba(239,68,68,0.5)]"
              )} />
              {dbStatus === 'connected' ? 'CORE ACTIVE' : 'SYSTEM OFFLINE'}
            </Badge>
          </div>

          <Separator orientation="vertical" className="h-8 bg-slate-200/50 dark:bg-white/10 mx-1" />

          <div className="flex items-center gap-2">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="h-10 w-10 rounded-2xl hover:bg-white/50 dark:hover:bg-white/5 transition-colors">
                  <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                  <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100 text-primary" />
                  <span className="sr-only">Toggle theme</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="crystal rounded-2xl p-1 border-white/10">
                <DropdownMenuItem onClick={() => setTheme("light")} className="gap-2 rounded-xl focus:bg-primary/10 focus:text-primary">
                  <Sun className="h-4 w-4" /> Light
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setTheme("dark")} className="gap-2 rounded-xl focus:bg-primary/10 focus:text-primary">
                  <Moon className="h-4 w-4" /> Dark
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setTheme("system")} className="gap-2 rounded-xl focus:bg-primary/10 focus:text-primary">
                  <Settings className="h-4 w-4" /> System
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            <Button variant="ghost" size="icon" className="h-10 w-10 rounded-2xl hover:bg-white/50 dark:hover:bg-white/5">
              <Settings className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}
