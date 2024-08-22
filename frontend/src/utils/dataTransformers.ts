import { ItemType, ContentSection } from '../types/pathBased';

interface Sentence {
  index: number;
  clean_text: string;
}

interface Turn {
  index: number;
  speaker: string;
  sentences: Sentence[];
}

interface Section {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  turns: Turn[];
}

export const transformTranscriptData = (data: any): ItemType => {
  console.log('Transforming data:', data);
  const sections = data.sections.map((section: Section) => transformSection(section));
  console.log('Transformed sections:', sections);
  return {
    title: data.transcript.title || 'Untitled Transcript',
    subtitle: '',
    content: [],
    children: sections
  };
};

const transformSection = (section: Section): ItemType => {
  return {
    title: section.title,
    subtitle: section.subtitle,
    content: [
      { type: 'longText', label: 'Description', value: section.description }
    ],
    children: section.turns.map(transformTurn),
    section: section.id
  };
};

const transformTurn = (turn: Turn): ItemType => {
  return {
    title: `Turn ${turn.index}`,
    subtitle: turn.speaker,
    content: turn.sentences.map((sentence: Sentence, index: number) => ({
      type: 'text',
      label: `Sentence ${index + 1}`,
      value: sentence.clean_text
    })),
    children: [placeholderQuestion()], // We'll keep this as a placeholder for now
  };
};

const placeholderQuestion = (): ItemType => {
  return {
    title: 'Placeholder Question',
    subtitle: '',
    content: [
      { type: 'text', label: 'Placeholder', value: 'This is a placeholder question' }
    ],
    children: [placeholderAssertion()]
  };
};

const placeholderAssertion = (): ItemType => {
  return {
    title: 'Placeholder Assertion',
    subtitle: 'Placeholder Category',
    content: [
      { type: 'longText', label: 'Content', value: 'This is a placeholder assertion' },
      { type: 'longText', label: 'Evidence', value: 'This is placeholder evidence' }
    ],
    children: []
  };
};