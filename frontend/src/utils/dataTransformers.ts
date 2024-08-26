import { ItemType, ContentSection } from '../types/pathBased';

interface Turn {
  index: number;
  speaker: string;
  content: string;
  action: string;
  tag_contexts?: TagContext[];
}

interface TagContext {
  term: string;
  context: string;
}

interface Section {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  turn_indices: number[];
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
    section: section.id,
    turn_indices: section.turn_indices
  };
};

const transformTurn = (turn: Turn): ItemType => {
  return {
    title: turn.speaker,
    subtitle: turn.action,
    content: [
      { type: 'markdown', label: 'Content', value: turn.content }
    ],
    children: turn.tag_contexts ? turn.tag_contexts.map(transformTagContext) : [],
  };
};

const transformTagContext = (tagContext: TagContext): ItemType => {
  return {
    title: tagContext.term,
    subtitle: '',
    content: [
      { type: 'markdown', label: 'Context', value: tagContext.context }
    ],
    children: []
  };
};