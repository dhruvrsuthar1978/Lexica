export interface QueryResult {
  success: true;
  sql: string;
  columns: string[];
  rows: Record<string, unknown>[];
  rowCount: number;
  executionTime: number;
}

export interface QueryError {
  success: false;
  error: {
    type: string;
    message: string;
  };
}

export interface HistoryItem {
  id: string;
  question: string;
  timestamp: number;
  success: boolean;
  sql?: string;
}

export interface TableSchema {
  name: string;
  columns: string[];
}

export interface BackendSchemaColumn {
  name: string;
  type: string;
  nullable: boolean;
  default: string | null;
}

export interface BackendSchemaTable {
  name: string;
  columns: BackendSchemaColumn[];
  primaryKeys: string[];
  foreignKeys: {
    constrainedColumns: string[];
    referredTable: string;
    referredColumns: string[];
  }[];
}

export interface SchemaResponse {
  success: true;
  tables: BackendSchemaTable[];
  loadedAt: string;
}
