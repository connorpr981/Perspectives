import React, { createContext, useContext, useState, ReactNode } from 'react';

interface TranscriptContextType {
  transcriptId: string;
  setTranscriptId: (id: string) => void;
}

const TranscriptContext = createContext<TranscriptContextType | undefined>(undefined);

export const TranscriptProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [transcriptId, setTranscriptId] = useState<string>('Y0ggv8C4vd4zyhinZYbu'); // Default ID for testing with emulator

  return (
    <TranscriptContext.Provider value={{ transcriptId, setTranscriptId }}>
      {children}
    </TranscriptContext.Provider>
  );
};

export const useTranscript = () => {
  const context = useContext(TranscriptContext);
  if (context === undefined) {
    throw new Error('useTranscript must be used within a TranscriptProvider');
  }
  return context;
};