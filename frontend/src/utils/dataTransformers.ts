import { ItemType, ContentSection } from '../types/pathBased';

interface Turn {
  index: number;
  speaker: string;
  content: string;
  action: string;
  tag_contexts?: TagContext[];
  questions?: Question[];
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

interface Question {
  type: 'enrichment' | 'reflective';
  question: string;
  information_type?: string;
  action?: string;
  perspectives?: Perspective[];
}

interface Perspective {
  name: string;
  // Add any other fields that perspectives might have
}

export const transformTranscriptData = (data: any): ItemType => {
  const sections = data.sections.map((section: Section) => transformSection(section));
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
  const children: ItemType[] = [];

  if (turn.questions) {
    turn.questions.forEach((question) => {
      const questionItem: ItemType = {
        title: question.question,
        subtitle: question.type === 'enrichment' ? question.information_type || '' : question.action || '',
        content: [],
        section: question.type === 'enrichment' ? 'Enrichment Questions' : 'Reflective Questions',
      };

      if (question.type === 'reflective' && question.perspectives) {
        questionItem.children = question.perspectives.map(transformPerspective);
      }

      children.push(questionItem);
    });
  }

  if (turn.tag_contexts) {
    children.push(...turn.tag_contexts.map(transformTagContext));
  }

  return {
    title: turn.speaker,
    subtitle: turn.action,
    content: [
      { type: 'markdown', label: 'Content', value: turn.content }
    ],
    children,
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

const transformPerspective = (perspective: Perspective): ItemType => {
  return {
    title: perspective.name,
    subtitle: '',
    content: [],
    children: []
  };
};