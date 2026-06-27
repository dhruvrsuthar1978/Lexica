import { History, CheckCircle2, XCircle, Clock } from 'lucide-react';
import { useStore } from '@/store/useStore';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';

export function QueryHistory() {
  const { history, setQuestion } = useStore();

  const formatTime = (ts: number) => {
    return new Intl.DateTimeFormat('en', {
      hour: '2-digit',
      minute: '2-digit',
    }).format(ts);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b flex items-center justify-between">
        <div className="flex items-center gap-2 font-medium">
          <History className="h-4 w-4 text-primary" />
          <span>Recent Queries</span>
        </div>
      </div>
      <ScrollArea className="flex-1">
        <div className="p-2 space-y-2">
          {history.length > 0 ? (
            history.map((item) => (
              <button
                key={item.id}
                onClick={() => setQuestion(item.question)}
                className="w-full text-left p-3 rounded-lg border bg-card hover:border-primary/50 hover:shadow-sm transition-all group"
              >
                <div className="flex items-start justify-between mb-1">
                  <span className="text-xs font-mono text-muted-foreground line-clamp-2 pr-4">
                    {item.question}
                  </span>
                  {item.success ? (
                    <CheckCircle2 className="h-3.5 w-3.5 text-green-500 shrink-0 mt-0.5" />
                  ) : (
                    <XCircle className="h-3.5 w-3.5 text-destructive shrink-0 mt-0.5" />
                  )}
                </div>
                <div className="flex items-center gap-1.5 text-[10px] text-muted-foreground uppercase tracking-tight">
                  <Clock className="h-3 w-3" />
                  {formatTime(item.timestamp)}
                </div>
              </button>
            ))
          ) : (
            <div className="p-8 text-center flex flex-col items-center gap-2">
              <History className="h-8 w-8 text-muted-foreground/30" />
              <span className="text-xs text-muted-foreground">No query history yet.</span>
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
