import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import TranscriptProcessor from './components/TranscriptProcessor';

function App() {
  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Perspectives Dashboard
        </Typography>
        <TranscriptProcessor />
      </Box>
    </Container>
  );
}

export default App;