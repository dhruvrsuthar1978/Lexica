import { Database } from 'lucide-react';
import { TypographyP, TypographyH3 } from '@/components/ui/typography';

interface EmptyStateProps {
  title?: string;
  description?: string;
  icon?: React.ReactNode;
}

export function EmptyState({ 
  title = "Awaiting Instructions", 
  description = "Connect to your data core and ask a question to generate intelligence.",
  icon = <Database className="h-16 w-16 text-primary" />
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-40 text-center animate-in fade-in zoom-in-95 duration-1000">
      <div className="relative mb-12">
        <div className="absolute inset-0 bg-primary/10 blur-[100px] rounded-full scale-[2] animate-pulse-slow" />
        <div className="relative z-10 p-10 rounded-[2.5rem] bg-white/40 dark:bg-slate-900/40 border border-white dark:border-slate-800 shadow-2xl backdrop-blur-3xl animate-float">
          {icon}
        </div>
      </div>
      <TypographyH3 className="mb-4 text-4xl font-black tracking-tighter text-gradient border-none">
        {title}
      </TypographyH3>
      <TypographyP className="text-slate-500 dark:text-slate-400 max-w-md text-lg leading-relaxed font-semibold mt-0 opacity-70">
        {description}
      </TypographyP>
    </div>
  );
}
