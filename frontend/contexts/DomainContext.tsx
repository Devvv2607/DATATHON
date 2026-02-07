'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface DomainContextType {
  selectedDomain: string;
  setSelectedDomain: (domain: string) => void;
  selectedTrend: string;
  setSelectedTrend: (trend: string) => void;
}

const DomainContext = createContext<DomainContextType | undefined>(undefined);

export function DomainProvider({ children }: { children: ReactNode }) {
  const [selectedDomain, setSelectedDomain] = useState<string>('technology');
  const [selectedTrend, setSelectedTrend] = useState<string>('trend_1');

  // Load from localStorage on mount
  useEffect(() => {
    const savedDomain = localStorage.getItem('selected_domain');
    const savedTrend = localStorage.getItem('selected_trend');
    if (savedDomain) setSelectedDomain(savedDomain);
    if (savedTrend) setSelectedTrend(savedTrend);
  }, []);

  // Save to localStorage when changed
  const handleSetDomain = (domain: string) => {
    setSelectedDomain(domain);
    localStorage.setItem('selected_domain', domain);
  };

  const handleSetTrend = (trend: string) => {
    setSelectedTrend(trend);
    localStorage.setItem('selected_trend', trend);
  };

  return (
    <DomainContext.Provider value={{
      selectedDomain,
      setSelectedDomain: handleSetDomain,
      selectedTrend,
      setSelectedTrend: handleSetTrend,
    }}>
      {children}
    </DomainContext.Provider>
  );
}

export function useDomain() {
  const context = useContext(DomainContext);
  if (context === undefined) {
    throw new Error('useDomain must be used within a DomainProvider');
  }
  return context;
}
