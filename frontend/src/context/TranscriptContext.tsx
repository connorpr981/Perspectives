import React, { createContext, useState, useContext, ReactNode } from 'react';
import { Transcript } from '../services/firestoreService';
import { useEffect } from 'react';
import { fetchTranscripts } from '../services/firestoreService';

interface TranscriptContextType {
  selectedTranscriptId: string | null;
  setSelectedTranscriptId: (id: string | null) => void;
  transcripts: Transcript[];
  setTranscripts: (transcripts: Transcript[]) => void;
}

const TranscriptContext = createContext<TranscriptContextType | undefined>(undefined);

export const TranscriptProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [selectedTranscriptId, setSelectedTranscriptId] = useState<string | null>(null);
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTranscripts = async () => {
      try {
        const fetchedTranscripts = await fetchTranscripts();
        setTranscripts(fetchedTranscripts);
      } catch (err) {
        setError('Failed to load transcripts');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadTranscripts();
  }, []);

  return (
    <TranscriptContext.Provider value={{ 
      selectedTranscriptId, 
      setSelectedTranscriptId, 
      transcripts, 
      setTranscripts,
    }}>
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