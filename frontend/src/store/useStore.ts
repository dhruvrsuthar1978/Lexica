import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { HistoryItem, QueryResult, TableSchema } from '../types';

interface AppState {
  question: string;
  isLoading: boolean;
  sql: string | null;
  results: QueryResult | null;
  error: string | null;
  history: HistoryItem[];
  dbStatus: 'connected' | 'error';
  schema: TableSchema[];
  
  setQuestion: (q: string) => void;
  setLoading: (l: boolean) => void;
  setQueryResult: (res: QueryResult | null) => void;
  setError: (e: string | null) => void;
  addHistory: (item: HistoryItem) => void;
  setDbStatus: (status: 'connected' | 'error') => void;
  setSchema: (schema: TableSchema[]) => void;
  clearResults: () => void;
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      question: '',
      isLoading: false,
      sql: null,
      results: null,
      error: null,
      history: [],
      dbStatus: 'connected',
      schema: [
        { name: 'Employees', columns: ['id', 'name', 'salary', 'department', 'join_date'] },
        { name: 'Departments', columns: ['id', 'name', 'manager_id'] },
        { name: 'Customers', columns: ['customer_id', 'name', 'city', 'email'] },
        { name: 'Orders', columns: ['order_id', 'customer_id', 'amount', 'order_date'] },
        { name: 'Products', columns: ['id', 'category', 'price', 'stock'] },
      ],

      setQuestion: (question) => set({ question }),
      setLoading: (isLoading) => set({ isLoading }),
      setQueryResult: (results) => set({ 
        results, 
        sql: results?.sql || null, 
        error: null,
        isLoading: false 
      }),
      setError: (error) => set({ 
        error, 
        results: null, 
        sql: null,
        isLoading: false 
      }),
      addHistory: (item) => set((state) => ({ 
        history: [item, ...state.history].slice(0, 50) 
      })),
      setDbStatus: (dbStatus) => set({ dbStatus }),
      setSchema: (schema) => set({ schema }),
      clearResults: () => set({ results: null, sql: null, error: null }),
    }),
    {
      name: 'text-to-sql-storage',
      partialize: (state) => ({ history: state.history, schema: state.schema }),
    }
  )
);
