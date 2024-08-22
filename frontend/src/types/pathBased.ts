export type ContentSection = {
  type: 'text' | 'longText';
  label: string;
  value: string;
};

export type ItemType = {
  title: string;
  subtitle: string;
  content: ContentSection[];
  children?: ItemType[];
  section?: string;
};

export type PathType = number[];

export type ColumnConfig = {
  title: string;
};

export type LayoutConfig = {
  columns: ColumnConfig[];
};

export type SavedPath = {
  id: string;
  path: PathType;
};
