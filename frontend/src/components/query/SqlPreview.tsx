import { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus, prism } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check, Download, Code2 } from 'lucide-react';
import { useStore } from '@/store/useStore';
import { useTheme } from '../theme-provider';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';

export function SqlPreview() {
  const { sql, isLoading } = useStore();
  const { theme } = useTheme();
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (sql) {
      navigator.clipboard.writeText(sql);
      setCopied(true);
      toast.success("SQL copied to clipboard");
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    if (sql) {
      const blob = new Blob([sql], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'query.sql';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  if (isLoading) {
    return (
      <Card className="w-full mt-6">
        <CardHeader className="flex flex-row items-center justify-between py-4">
          <Skeleton className="h-6 w-32" />
          <Skeleton className="h-8 w-24" />
        </CardHeader>
        <CardContent>
          <Skeleton className="h-[100px] w-full" />
        </CardContent>
      </Card>
    );
  }

  if (!sql) return null;

  return (
    <Card className="w-full overflow-hidden cyber-panel border-white/20 dark:border-white/10 shadow-xl">
      <CardHeader className="flex flex-row items-center justify-between py-5 px-8 bg-primary/5 dark:bg-white/5 border-b border-white/5">
        <div className="flex items-center gap-4">
          <div className="p-2 rounded-xl bg-primary/10 text-primary shadow-[0_0_10px_rgba(167,139,250,0.2)]">
            <Code2 className="h-5 w-5" />
          </div>
          <CardTitle className="section-header">
            ENGINEERED SQL
          </CardTitle>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            className="h-10 px-6 gap-2 rounded-full hover:bg-primary/10 hover:text-primary transition-all font-black text-[10px] tracking-widest uppercase border border-white/10"
            onClick={handleCopy}
          >
            {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
            <span>{copied ? "COPIED" : "COPY"}</span>
          </Button>
          <Button
            variant="ghost"
            size="sm"
            className="h-10 px-6 gap-2 rounded-full hover:bg-primary/10 hover:text-primary transition-all font-black text-[10px] tracking-widest uppercase border border-white/10"
            onClick={handleDownload}
          >
            <Download className="h-3 w-3" />
            <span>EXPORT</span>
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <div className="relative group bg-black/40">
          <SyntaxHighlighter
            language="sql"
            style={theme === 'dark' ? vscDarkPlus : prism}
            customStyle={{
              margin: 0,
              padding: '2.5rem',
              fontSize: '1rem',
              lineHeight: '1.8',
              background: 'transparent',
            }}
            codeTagProps={{
              className: "font-mono font-medium"
            }}
          >
            {sql}
          </SyntaxHighlighter>
        </div>
      </CardContent>
    </Card>
  );
}
