import { useMemo, useState } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  flexRender,
  ColumnDef,
  SortingState,
} from '@tanstack/react-table';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { useStore } from '@/store/useStore';
import {
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
  Download,
  ArrowUpDown,
  Table as TableIcon
} from 'lucide-react';
import { EmptyState } from '../shared/EmptyState';

export function ResultTable() {
  const { results, isLoading } = useStore();
  const [sorting, setSorting] = useState<SortingState>([]);

  const columns = useMemo<ColumnDef<Record<string, unknown>>[]>(() => {
    if (!results) return [];
    return results.columns.map((col) => ({
      accessorKey: col,
      header: ({ column }) => (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="-ml-4 h-8 gap-2 text-xs font-bold uppercase tracking-wider"
        >
          {col}
          <ArrowUpDown className="h-3 w-3" />
        </Button>
      ),
      cell: ({ row }) => <div className="text-sm">{String(row.getValue(col) ?? '')}</div>,
    }));
  }, [results]);

  const data = useMemo(() => results?.rows || [], [results]);

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    initialState: { pagination: { pageSize: 10 } },
  });

  const handleDownloadCSV = () => {
    if (!results) return;
    const headers = results.columns.join(',');
    const rows = results.rows.map(row =>
      results.columns.map(col => {
        const value = row[col] === null || row[col] === undefined ? '' : String(row[col]);
        return `"${value.replace(/"/g, '""')}"`;
      }).join(',')
    ).join('\n');
    const blob = new Blob([`${headers}\n${rows}`], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", "query_results.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  if (isLoading) {
    return (
      <Card className="w-full mt-6">
        <CardHeader className="py-4 border-b">
          <Skeleton className="h-6 w-48" />
        </CardHeader>
        <CardContent className="p-0">
          <div className="space-y-2 p-4">
            {[...Array(5)].map((_, i) => (
              <Skeleton key={i} className="h-10 w-full" />
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!results) {
    return (
      <Card className="w-full mt-6 border-dashed bg-muted/20">
        <CardContent className="flex items-center justify-center p-0">
          <EmptyState />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full cyber-panel border-white/20 dark:border-white/10 shadow-2xl overflow-hidden animate-in fade-in slide-in-from-bottom-6 duration-700">
      <CardHeader className="flex flex-row items-center justify-between py-6 px-8 border-b border-white/5 bg-primary/5 dark:bg-white/5">
        <div className="flex items-center gap-4">
          <div className="p-2.5 rounded-2xl bg-primary/10 dark:bg-white/5 shadow-sm text-primary neon-glow-primary">
            <TableIcon className="h-6 w-6" />
          </div>
          <CardTitle className="section-header">
            INTELLIGENCE OUTPUT
            <span className="lowercase text-[10px] font-black bg-primary text-primary-foreground px-3 py-1 rounded-full shadow-lg shadow-primary/20 ml-2">
              {results.rowCount} records
            </span>
          </CardTitle>
        </div>
        <Button variant="outline" size="sm" onClick={handleDownloadCSV} className="h-11 px-6 gap-2 rounded-full border-white/40 dark:border-white/10 bg-white/40 dark:bg-white/5 hover:bg-white dark:hover:bg-white/10 transition-all shadow-sm font-black text-[10px] tracking-widest uppercase text-muted-foreground">
          <Download className="h-4 w-4" />
          EXPORT DATASET
        </Button>
      </CardHeader>
      <CardContent className="p-0">
        <div className="relative overflow-x-auto">
          <Table>
            <TableHeader className="bg-primary/5 dark:bg-black/40">
              {table.getHeaderGroups().map((headerGroup) => (
                <TableRow key={headerGroup.id} className="hover:bg-transparent border-b border-white/5">
                  {headerGroup.headers.map((header) => (
                    <TableHead key={header.id} className="px-8 py-5 whitespace-nowrap">
                      {header.isPlaceholder
                        ? null
                        : flexRender(header.column.columnDef.header, header.getContext())}
                    </TableHead>
                  ))}
                </TableRow>
              ))}
            </TableHeader>
            <TableBody>
              {table.getRowModel().rows?.length ? (
                table.getRowModel().rows.map((row) => (
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() && "selected"}
                    className="hover:bg-primary/5 transition-colors border-b border-white/5 last:border-0 group/row"
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id} className="px-8 py-5 font-bold text-foreground/80 dark:text-slate-300 text-sm tracking-tight group-hover/row:text-primary transition-colors">
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={columns.length} className="h-40 text-center text-muted-foreground font-black italic tracking-[0.2em] uppercase text-[10px]">
                    The engine is ready. Feed it a query to begin.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>

        <div className="flex items-center justify-between px-8 py-6 border-t border-white/5 bg-primary/5 dark:bg-white/5">
          <div className="flex-1 text-[10px] font-black text-muted-foreground uppercase tracking-[0.3em]">
            BLOCK {table.getState().pagination.pageIndex + 1} OF {table.getPageCount()}
          </div>
          <div className="flex items-center space-x-3">
            {[
              { icon: ChevronsLeft, action: () => table.setPageIndex(0), disabled: !table.getCanPreviousPage() },
              { icon: ChevronLeft, action: () => table.previousPage(), disabled: !table.getCanPreviousPage() },
              { icon: ChevronRight, action: () => table.nextPage(), disabled: !table.getCanNextPage() },
              { icon: ChevronsRight, action: () => table.setPageIndex(table.getPageCount() - 1), disabled: !table.getCanNextPage() },
            ].map(({ icon: Icon, action, disabled }, i) => (
              <Button
                key={i}
                variant="outline"
                size="icon"
                className="h-10 w-10 rounded-xl border-white/40 dark:border-white/10 bg-white/40 dark:bg-white/5 hover:bg-white dark:hover:bg-white/10 text-muted-foreground hover:text-primary"
                onClick={action}
                disabled={disabled}
              >
                <Icon className="h-4 w-4" />
              </Button>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
