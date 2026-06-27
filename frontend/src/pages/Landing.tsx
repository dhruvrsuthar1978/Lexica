import { useNavigate } from 'react-router-dom';
import { SpiderWebCanvas } from '@/components/SpiderWebCanvas';
import { DatabaseZap, Zap, Shield, BarChart3, ArrowRight, Code2, Globe, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useTheme } from '@/components/theme-provider';
import { Moon, Sun, Settings } from 'lucide-react';
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

const FEATURES = [
  { icon: <Zap className="h-6 w-6" />, title: 'Instant SQL Generation', desc: 'Type a question in plain English and get production-ready SQL in milliseconds powered by state-of-the-art LLMs.' },
  { icon: <Shield className="h-6 w-6" />, title: 'Safe & Read-Only', desc: 'Every query runs in a read-only transaction. No accidental writes, no data corruption — ever.' },
  { icon: <BarChart3 className="h-6 w-6" />, title: 'Live Results', desc: 'See your query results rendered as a beautiful table instantly, with row counts and execution time.' },
  { icon: <Code2 className="h-6 w-6" />, title: 'SQL Preview', desc: 'Inspect the generated SQL before or after execution. Learn SQL while you work.' },
  { icon: <Globe className="h-6 w-6" />, title: 'Any SQL Dialect', desc: 'Supports SQLite, PostgreSQL, and more. Switch dialects with a single config change.' },
  { icon: <Sparkles className="h-6 w-6" />, title: 'Schema Aware', desc: 'Automatically introspects your database schema so the LLM always generates accurate, contextual queries.' },
];

const EXAMPLES = [
  'Show top 10 customers by total spend',
  'What is the total revenue by product category?',
  'Which employees earn more than $100,000?',
  'How many orders were placed each month in 2024?',
  'List products with stock below 50',
  'Which products have an average rating above 4?',
];

export function Landing() {
  const navigate = useNavigate();
  const { setTheme } = useTheme();

  return (
    <div className="min-h-screen bg-background overflow-x-hidden relative">

      {/* Full-page animated spider web */}
      <SpiderWebCanvas />

      {/* Navbar */}
      <header className="fixed top-0 left-0 right-0 z-40 w-full bg-transparent backdrop-blur-xl border-b border-white/20 dark:border-white/10">
        <div className="max-w-7xl mx-auto flex h-16 items-center justify-between px-4 sm:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary text-primary-foreground shadow-lg shadow-primary/20">
              <DatabaseZap className="h-6 w-6" />
            </div>
            <span className="text-xl font-black tracking-tighter text-gradient hidden sm:inline-block">
              Lexica
            </span>
          </div>
          <div className="flex items-center gap-3">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="h-10 w-10 rounded-2xl hover:bg-white/50 dark:hover:bg-white/5">
                  <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                  <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100 text-primary" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="crystal rounded-2xl p-1 border-white/10">
                <DropdownMenuItem onClick={() => setTheme('light')} className="gap-2 rounded-xl focus:bg-primary/10 focus:text-primary"><Sun className="h-4 w-4" /> Light</DropdownMenuItem>
                <DropdownMenuItem onClick={() => setTheme('dark')} className="gap-2 rounded-xl focus:bg-primary/10 focus:text-primary"><Moon className="h-4 w-4" /> Dark</DropdownMenuItem>
                <DropdownMenuItem onClick={() => setTheme('system')} className="gap-2 rounded-xl focus:bg-primary/10 focus:text-primary"><Settings className="h-4 w-4" /> System</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
            <Button onClick={() => navigate('/app')} className="btn-premium rounded-2xl gap-2 px-5">
              Launch App <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      {/* Spacer for fixed navbar */}
      <div className="h-16" />

      {/* Hero */}
      <section className="relative z-10">
        <div className="orb w-[600px] h-[600px] bg-primary/15 -top-40 -left-40 animate-pulse-slow" />
        <div className="orb w-[500px] h-[500px] bg-accent/10 top-20 -right-40 animate-pulse-slow" style={{ animationDelay: '2s' }} />

        <div className="relative max-w-5xl mx-auto px-4 sm:px-8 pt-28 pb-24 text-center">
          <Badge variant="outline" className="crystal neon-glow-primary mb-6 px-4 py-1.5 rounded-full font-bold text-primary border-primary/30 gap-2">
            <Sparkles className="h-3.5 w-3.5" /> Powered by Groq LLM
          </Badge>

          <h1 className="text-5xl sm:text-7xl font-black tracking-tighter mb-6 leading-[1.05]">
            Query your database
            <br />
            <span className="text-gradient">in plain English</span>
          </h1>

          <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed">
            Stop writing SQL by hand. Ask questions naturally and get instant,
            accurate results from your database — no SQL knowledge required.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" onClick={() => navigate('/app')} className="btn-premium rounded-2xl text-base px-8 h-14 gap-2 shadow-xl shadow-primary/25">
              Start Querying Free <ArrowRight className="h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" className="rounded-2xl text-base px-8 h-14 crystal border-border/50">
              View Demo
            </Button>
          </div>
        </div>
      </section>

      {/* Example queries */}
      <section className="relative z-10 border-y border-border/50 bg-muted/30 py-5">
        <div className="flex gap-3 flex-wrap justify-center px-4 max-w-5xl mx-auto">
          {EXAMPLES.map((ex) => (
            <button
              key={ex}
              onClick={() => navigate('/app')}
              className="crystal neon-glow-primary rounded-full px-4 py-2 text-sm font-medium text-foreground/80 hover:text-primary hover:border-primary/40 transition-colors border border-border/50 cursor-pointer"
            >
              "{ex}"
            </button>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="relative z-10 max-w-6xl mx-auto px-4 sm:px-8 py-24">
        <div className="text-center mb-16">
          <p className="section-header mb-3">Features</p>
          <h2 className="text-3xl sm:text-5xl font-black tracking-tighter">
            Everything you need to
            <span className="text-gradient"> explore your data</span>
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((f) => (
            <div key={f.title} className="crystal-card rounded-3xl p-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group">
              <div className="h-12 w-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-4 group-hover:bg-primary group-hover:text-primary-foreground transition-colors duration-300">
                {f.icon}
              </div>
              <h3 className="font-bold text-lg mb-2">{f.title}</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="relative z-10 overflow-hidden border-t border-border/50">
        <div className="orb w-[500px] h-[500px] bg-primary/15 -bottom-40 left-1/2 -translate-x-1/2" />
        <div className="relative max-w-3xl mx-auto px-4 sm:px-8 py-24 text-center">
          <h2 className="text-4xl sm:text-6xl font-black tracking-tighter mb-6">
            Ready to talk to
            <span className="text-gradient"> your database?</span>
          </h2>
          <p className="text-muted-foreground text-lg mb-10">
            No setup required. Your database is already connected.
          </p>
          <Button size="lg" onClick={() => navigate('/app')} className="btn-premium rounded-2xl text-base px-10 h-14 gap-2 shadow-xl shadow-primary/25">
            Launch App <ArrowRight className="h-5 w-5" />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-border/50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2 font-bold text-foreground">
            <DatabaseZap className="h-5 w-5 text-primary" />
            Lexica
          </div>
          <p>© {new Date().getFullYear()} Lexica. Built with FastAPI & React.</p>
        </div>
      </footer>
    </div>
  );
}
