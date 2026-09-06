import { createContext, useContext, useState, ReactNode } from 'react';
import { ProductionRecord } from './types';
import { initialProductionData } from './data';

interface ProductionContextType {
  records: ProductionRecord[];
  addRecord: (record: ProductionRecord) => void;
  updateRecord: (id: string, updates: Partial<ProductionRecord>) => void;
}

const ProductionContext = createContext<ProductionContextType | undefined>(undefined);

export function ProductionProvider({ children }: { children: ReactNode }) {
  const [records, setRecords] = useState<ProductionRecord[]>(initialProductionData);

  const addRecord = (record: ProductionRecord) => {
    setRecords((prev) => [...prev, record]);
  };

  const updateRecord = (id: string, updates: Partial<ProductionRecord>) => {
    setRecords((prev) => 
      prev.map(r => r.id === id ? { ...r, ...updates } : r)
    );
  };

  return (
    <ProductionContext.Provider value={{ records, addRecord, updateRecord }}>
      {children}
    </ProductionContext.Provider>
  );
}

export function useProduction() {
  const context = useContext(ProductionContext);
  if (context === undefined) {
    throw new Error('useProduction must be used within a ProductionProvider');
  }
  return context;
}
