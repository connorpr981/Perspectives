import React, { useState } from 'react';
import { Button, TextField, Box, Typography, CircularProgress } from '@mui/material';
import { processTranscript } from '../services/api';

const TranscriptProcessor: React.FC = () => {
  const [filename, setFilename] = useState('');
  const [transcriptId, setTranscriptId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleProcess = async () => {
    setLoading(true);
    setError('');
    try {
      const id = await processTranscript(filename);
      setTranscriptId(id);
    } catch (err) {
      setError('Error processing transcript');
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Process Transcript
      </Typography>
      <TextField
        fullWidth
        label="Filename"
        value={filename}
        onChange={(e) => setFilename(e.target.value)}
        margin="normal"
      />
      <Button
        variant="contained"
        onClick={handleProcess}
        disabled={!filename || loading}
      >
        Process Transcript
      </Button>
      {loading && <CircularProgress sx={{ ml: 2 }} />}
      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}
      {transcriptId && (
        <Typography sx={{ mt: 2 }}>
          Transcript processed with ID: {transcriptId}
        </Typography>
      )}
    </Box>
  );
};

export default TranscriptProcessor;