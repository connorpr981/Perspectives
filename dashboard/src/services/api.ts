import axios from 'axios';

const BASE_URL = 'https://your-firebase-function-url.com';

export const processTranscript = async (filename: string): Promise<string> => {
  const response = await axios.get(`${BASE_URL}/read_transcript_from_storage`, {
    params: { filename },
  });
  return response.data.split(': ')[1];
};

export const getTurnTags = async (transcriptId: string): Promise<void> => {
  await axios.get(`${BASE_URL}/get_turn_tags`, {
    params: { transcript_id: transcriptId },
  });
};

export const generateTranscriptSections = async (transcriptId: string): Promise<void> => {
  await axios.get(`${BASE_URL}/generate_transcript_sections`, {
    params: { transcript_id: transcriptId },
  });
};

export const generateTagContexts = async (transcriptId: string): Promise<void> => {
  await axios.get(`${BASE_URL}/generate_tag_contexts`, {
    params: { transcript_id: transcriptId },
  });
};

export const generateEnrichmentQuestions = async (transcriptId: string, testMode: boolean = false): Promise<void> => {
  await axios.get(`${BASE_URL}/generate_transcript_enrichment_questions`, {
    params: { transcript_id: transcriptId, test_mode: testMode },
  });
};

export const generateReflectiveQuestions = async (transcriptId: string, testMode: boolean = false): Promise<void> => {
  await axios.get(`${BASE_URL}/generate_transcript_reflective_questions`, {
    params: { transcript_id: transcriptId, test_mode: testMode },
  });
};

export const answerEnrichmentQuestions = async (transcriptId: string): Promise<void> => {
  await axios.get(`${BASE_URL}/answer_enrichment_questions`, {
    params: { transcript_id: transcriptId },
  });
};