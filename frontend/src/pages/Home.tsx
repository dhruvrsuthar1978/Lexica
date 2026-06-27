import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';
import { Navbar } from '@/components/layout/Navbar';
import { AppSidebar } from '@/components/query/AppSidebar';
import { QuestionInput } from '@/components/query/QuestionInput';
import { SqlPreview } from '@/components/query/SqlPreview';
import { ResultTable } from '@/components/query/ResultTable';
import { LoadingOverlay } from '@/components/shared/LoadingOverlay';
import { useStore } from '@/store/useStore';
import { motion } from 'motion/react';

export function Home() {
  const { isLoading } = useStore();

  return (
    <SidebarProvider>
      <AppSidebar variant="inset" />
      <SidebarInset className="flex flex-col overflow-hidden">
        {/* Grid Background */}
        <div className="absolute inset-0 grid-background opacity-40 dark:opacity-20 pointer-events-none z-0" />

        {/* Spider web accent */}
        <div className="absolute inset-0 spider-web-background pointer-events-none z-0" style={{ mixBlendMode: 'screen' }}>
          <svg viewBox="0 0 1200 1200" className="w-full h-full" preserveAspectRatio="xMidYMid slice">
            <defs>
              <linearGradient id="spider-web-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="rgba(167, 139, 250, 0.30)" />
                <stop offset="100%" stopColor="rgba(167, 139, 250, 0.04)" />
              </linearGradient>
            </defs>
            <g stroke="url(#spider-web-gradient)" strokeWidth="1" fill="none">
              <circle cx="600" cy="600" r="220" />
              <circle cx="600" cy="600" r="320" />
              <circle cx="600" cy="600" r="420" />
              <circle cx="600" cy="600" r="520" />
              <path d="M600 0 L600 1200" />
              <path d="M0 600 L1200 600" />
              <path d="M0 0 L1200 1200" />
              <path d="M1200 0 L0 1200" />
              <path d="M150 0 L600 600 L1050 0" />
              <path d="M150 1200 L600 600 L1050 1200" />
            </g>
          </svg>
        </div>

        {/* Ambient Background Orbs */}
        <div className="orb bg-primary/20 w-[600px] h-[600px] -top-40 -right-40 animate-pulse-slow z-0" />
        <div className="orb bg-accent/15 w-[500px] h-[500px] -bottom-40 -left-40 animate-pulse-slow [animation-delay:2s] z-0" />
        <div className="orb bg-primary/5 w-[800px] h-[800px] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-pulse-slow [animation-delay:4s] z-0" />

        <Navbar />
        <main className="flex-1 overflow-y-auto relative z-10">
          <div className="container max-w-6xl mx-auto py-16 px-6 sm:px-12">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
              className="space-y-16"
            >
              <section className="relative">
                <div className="flex items-center gap-4 mb-8">
                  <span className="section-header min-w-fit">Query Interface</span>
                  <div className="h-px flex-1 bg-linear-to-r from-primary/20 to-transparent" />
                </div>
                <QuestionInput />
              </section>

              <section className="space-y-12">
                <div className="flex items-center gap-4 mb-8">
                  <span className="section-header min-w-fit">Analysis Workspace</span>
                  <div className="h-px flex-1 bg-linear-to-r from-primary/20 to-transparent" />
                </div>
                <div className="flex flex-col gap-10">
                  <SqlPreview />
                  <ResultTable />
                </div>
              </section>
            </motion.div>
          </div>
        </main>
      </SidebarInset>
      <LoadingOverlay isVisible={isLoading} message="Synthesizing intelligence..." />
    </SidebarProvider>
  );
}
