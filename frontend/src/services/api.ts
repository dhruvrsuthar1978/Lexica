import axios from 'axios';
import { QueryError, QueryResult, SchemaResponse, TableSchema } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000,
});

const apiKey = import.meta.env.VITE_API_KEY as string | undefined;
const getApiHeaders = () => ({
  ...(apiKey ? { 'x-api-key': apiKey } : {}),
});

export const queryDatabase = async (question: string): Promise<QueryResult> => {
  try {
    const response = await api.post<QueryResult | QueryError>(
      '/api/query',
      { question },
      { headers: getApiHeaders() }
    );
    
    if (!response.data.success) {
      throw new Error(response.data.error.message);
    }
    
    return response.data;
  } catch (error: unknown) {
    throw new Error(getApiErrorMessage(error, 'Failed to execute query'));
  }
};

export const fetchDatabaseSchema = async (): Promise<TableSchema[]> => {
  try {
    const response = await api.get<SchemaResponse | QueryError>('/api/schema', {
      headers: getApiHeaders(),
    });

    if (!response.data.success) {
      throw new Error(response.data.error.message);
    }

    return response.data.tables.map((table) => ({
      name: table.name,
      columns: table.columns.map((column) => `${column.name} (${column.type})`),
    }));
  } catch (error: unknown) {
    throw new Error(getApiErrorMessage(error, 'Failed to load database schema'));
  }
};

export const refreshDatabaseSchema = async (): Promise<TableSchema[]> => {
  try {
    const response = await api.post<SchemaResponse | QueryError>('/api/schema/refresh', undefined, {
      headers: getApiHeaders(),
    });

    if (!response.data.success) {
      throw new Error(response.data.error.message);
    }

    return response.data.tables.map((table) => ({
      name: table.name,
      columns: table.columns.map((column) => `${column.name} (${column.type})`),
    }));
  } catch (error: unknown) {
    throw new Error(getApiErrorMessage(error, 'Failed to refresh database schema'));
  }
};

const getApiErrorMessage = (error: unknown, fallback: string): string => {
  if (!axios.isAxiosError(error)) {
    return error instanceof Error ? error.message : fallback;
  }

  const payload = error.response?.data as
    | QueryError
    | { detail?: string }
    | string
    | undefined;

  if (typeof payload === 'string') {
    return payload;
  }

  if (payload && typeof payload === 'object' && 'error' in payload) {
    return payload.error.message;
  }

  if (
    payload &&
    typeof payload === 'object' &&
    'detail' in payload &&
    typeof payload.detail === 'string'
  ) {
    return payload.detail;
  }

  return error.message || fallback;
};
