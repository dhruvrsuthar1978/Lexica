import { KeyboardEvent } from 'react';
import { Play, RotateCcw, HelpCircle, Sparkles } from 'lucide-react';
import { useStore } from '@/store/useStore';
import { queryDatabase } from '@/services/api';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent } from '@/components/ui/card';
import { toast } from 'sonner';

const EXAMPLES = [
  "Show all employees with salary above 50000",
  "Which products generated the highest revenue?",
  "Display orders placed this month",
  "Count active users in Delhi",
  "Show top 10 employees by salary"
];

export function QuestionInput() {
  const {
    question,
    setQuestion,
    setLoading,
    setQueryResult,
    setError,
    addHistory,
    setDbStatus,
    isLoading
  } = useStore();

  const handleRunQuery = async () => {
    if (!question.trim()) {
      toast.error("Please enter a question.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await queryDatabase(question);
      setQueryResult(result);
      addHistory({
        id: crypto.randomUUID(),
        question,
        timestamp: Date.now(),
        success: true,
        sql: result.sql
      });
      setDbStatus('connected');
      toast.success(`Query executed in ${result.executionTime.toFixed(3)}s.`);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'An error occurred';
      setError(message);
      addHistory({
        id: crypto.randomUUID(),
        question,
        timestamp: Date.now(),
        success: false
      });
      setDbStatus('error');
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      handleRunQuery();
    }
  };

  const handleClear = () => {
    setQuestion('');
    setError(null);
    setQueryResult(null);
  };

  return (
    <Card className="w-full crystal-card border-white/20 dark:border-white/5 shadow-2xl relative overflow-hidden group transition-all duration-500 hover:shadow-primary/10">
      <div className="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-transparent via-primary/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
      <CardContent className="p-8">
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 text-primary font-black tracking-tight">
              <div className="p-2 rounded-2xl bg-primary/10 dark:bg-primary/20 shadow-sm transition-transform group-hover:rotate-12">
                <Sparkles className="h-5 w-5" />
              </div>
              <span className="text-[10px] uppercase tracking-[0.3em] opacity-90">NEURAL INTERFACE v4.0</span>
            </div>
            <span className="text-[10px] font-black text-muted-foreground bg-muted/50 dark:bg-white/5 px-2.5 py-1 rounded-full border border-border dark:border-white/10 shadow-xs">
              {question.length} / 1000
            </span>
          </div>

          <div className="relative group/input">
            <div className="absolute -inset-1 bg-linear-to-r from-primary/10 via-accent/10 to-primary/10 rounded-[2rem] blur-xl opacity-0 group-focus-within/input:opacity-100 transition duration-1000 pointer-events-none" />
            <div className="relative rounded-[1.5rem] recessed overflow-hidden border-border dark:border-white/5 transition-all duration-500 group-focus-within/input:bg-white dark:group-focus-within/input:bg-black">
              <Textarea
                placeholder="Describe the data you need... (e.g., 'Find top 10 customers by revenue last month')"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={handleKeyDown}
                className="relative min-h-[160px] resize-none text-xl p-6 font-sans font-medium bg-transparent border-none focus-visible:ring-0 placeholder:text-slate-300 dark:placeholder:text-slate-700 leading-relaxed transition-all"
                disabled={isLoading}
                maxLength={1000}
              />
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
            <div className="flex items-center gap-4">
              <Button
                onClick={handleRunQuery}
                disabled={isLoading || !question.trim()}
                className="btn-premium h-14 px-10 rounded-full text-lg font-black tracking-tighter"
              >
                <Play className="h-6 w-6 fill-current mr-2" />
                EXECUTE CORE
              </Button>
              <Button
                variant="ghost"
                onClick={handleClear}
                disabled={isLoading || !question}
                className="h-14 px-6 rounded-full text-primary font-black tracking-widest text-xs hover:bg-primary/10 dark:hover:bg-white/5"
              >
                <RotateCcw className="h-4 w-4 mr-2" />
                RESET
              </Button>
            </div>

            <div className="hidden md:flex items-center gap-2.5 text-[10px] font-black text-muted-foreground uppercase tracking-widest bg-white/50 dark:bg-white/5 px-4 py-2 rounded-full border border-border dark:border-white/10 shadow-sm">
              <kbd className="px-2 py-0.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xs text-slate-500">CTRL</kbd>
              <span>+</span>
              <kbd className="px-2 py-0.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xs text-slate-500">ENTER</kbd>
              <span className="ml-1 opacity-60">TO COMPILE</span>
            </div>
          </div>

          <div className="pt-6 border-t border-border/50 dark:border-white/5">
            <div className="flex items-center gap-2.5 mb-4 text-[10px] font-black text-muted-foreground uppercase tracking-[0.3em]">
              <HelpCircle className="h-3.5 w-3.5" />
              <span>CORE SUGGESTIONS</span>
            </div>
            <div className="flex flex-wrap gap-2.5">
              {EXAMPLES.map((example) => (
                <button
                  key={example}
                  onClick={() => setQuestion(example)}
                  className="text-[11px] font-black bg-white/40 dark:bg-white/5 hover:bg-primary/10 dark:hover:bg-primary/20 text-muted-foreground hover:text-primary py-2.5 px-5 rounded-full transition-all border border-border dark:border-white/10 hover:shadow-lg hover:shadow-primary/5 hover:-translate-y-0.5 uppercase tracking-wider"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
