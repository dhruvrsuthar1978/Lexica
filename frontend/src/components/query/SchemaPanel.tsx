import { useCallback, useEffect, useState } from 'react';
import {
  Search,
  ChevronRight,
  ChevronDown,
  Table as TableIcon,
  Copy,
  RefreshCw,
} from 'lucide-react';
import { useStore } from '@/store/useStore';
import { fetchDatabaseSchema, refreshDatabaseSchema } from '@/services/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Collapsible, 
  CollapsibleContent, 
  CollapsibleTrigger 
} from '@/components/ui/collapsible';
import { toast } from 'sonner';

export function SchemaPanel() {
  const { schema, setSchema, setDbStatus } = useStore();
  const [search, setSearch] = useState('');
  const [openTables, setOpenTables] = useState<string[]>([]);
  const [isSchemaLoading, setIsSchemaLoading] = useState(false);
  const [lastRefreshed, setLastRefreshed] = useState<string | null>(null);

  const loadSchema = useCallback(async () => {
    setIsSchemaLoading(true);
    try {
      const tables = await fetchDatabaseSchema();
      setSchema(tables);
      setDbStatus('connected');
      setLastRefreshed(new Date().toLocaleTimeString());
    } catch (error) {
      setDbStatus('error');
      toast.error(error instanceof Error ? error.message : 'Failed to load schema');
    } finally {
      setIsSchemaLoading(false);
    }
  }, [setDbStatus, setSchema]);

  const refreshSchema = useCallback(async () => {
    setIsSchemaLoading(true);

    try {
      const tables = await refreshDatabaseSchema();
      setSchema(tables);
      setDbStatus('connected');
      setLastRefreshed(new Date().toLocaleTimeString());
      toast.success('Schema refreshed successfully');
    } catch (error) {
      setDbStatus('error');
      toast.error(error instanceof Error ? error.message : 'Failed to refresh schema');
    } finally {
      setIsSchemaLoading(false);
    }
  }, [setDbStatus, setSchema]);

  useEffect(() => {
    loadSchema();
  }, [loadSchema]);

  const filteredSchema = schema.filter(table => 
    table.name.toLowerCase().includes(search.toLowerCase()) ||
    table.columns.some(col => col.toLowerCase().includes(search.toLowerCase()))
  );

  const toggleTable = (name: string) => {
    setOpenTables(prev => 
      prev.includes(name) ? prev.filter(n => n !== name) : [...prev, name]
    );
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success(`Copied ${text} to clipboard`);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-primary/5 bg-primary/5">
        <div className="flex gap-2">
          <div className="relative group flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground group-focus-within:text-primary transition-colors" />
            <Input
              placeholder="Search database..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10 h-10 rounded-xl bg-background/50 border-muted-foreground/10 focus-visible:ring-primary/20"
            />
          </div>
          <div className="flex items-center gap-2">
            {lastRefreshed && (
              <span className="text-[11px] text-muted-foreground">Last refresh: {lastRefreshed}</span>
            )}
            <Button
              variant="outline"
              size="icon"
              className="h-10 w-10 rounded-xl bg-background/50"
              onClick={refreshSchema}
              disabled={isSchemaLoading}
              title="Refresh schema"
              aria-label="Refresh schema"
            >
              <RefreshCw className={`h-4 w-4 ${isSchemaLoading ? 'animate-spin' : ''}`} />
            </Button>
          </div>
        </div>
      </div>
      <ScrollArea className="flex-1">
        <div className="p-4 space-y-3">
          {filteredSchema.map((table) => (
            <Collapsible
              key={table.name}
              open={openTables.includes(table.name)}
              onOpenChange={() => toggleTable(table.name)}
              className="rounded-xl border border-primary/5 bg-muted/20 hover:bg-muted/40 transition-all overflow-hidden"
            >
              <CollapsibleTrigger className="flex items-center justify-between w-full p-3 group">
                <div className="flex items-center gap-3">
                  <div className="p-1.5 rounded-lg bg-background shadow-sm text-primary/70 group-hover:text-primary transition-colors">
                    <TableIcon className="h-4 w-4" />
                  </div>
                  <span className="text-sm font-mono font-bold tracking-tight">{table.name}</span>
                </div>
                {openTables.includes(table.name) ? (
                  <ChevronDown className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <ChevronRight className="h-4 w-4 text-muted-foreground" />
                )}
              </CollapsibleTrigger>
              <CollapsibleContent className="px-3 pb-3">
                <div className="pt-2 space-y-1 pl-9">
                  {table.columns.map((col) => (
                    <div 
                      key={col} 
                      className="group/item flex items-center justify-between py-1.5 px-3 rounded-lg hover:bg-background/50 transition-colors"
                    >
                      <span className="text-xs font-mono text-muted-foreground group-hover/item:text-foreground transition-colors">{col}</span>
                      <button 
                        onClick={() => copyToClipboard(col)}
                        className="opacity-0 group-hover/item:opacity-100 p-1 rounded-md hover:bg-muted transition-all"
                      >
                        <Copy className="h-3 w-3 text-primary" />
                      </button>
                    </div>
                  ))}
                </div>
              </CollapsibleContent>
            </Collapsible>
          ))}
          {filteredSchema.length === 0 && (
            <div className="p-8 text-center flex flex-col items-center gap-2">
              <Search className="h-8 w-8 text-muted-foreground/30" />
              <span className="text-xs text-muted-foreground">
                {isSchemaLoading ? 'Loading schema...' : 'No tables found matching your search.'}
              </span>
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
