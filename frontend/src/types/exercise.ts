export type Difficulty = "basic" | "intermediate" | "advanced";

export interface Level {
  id: number;
  name: string;
  slug: string;
  difficulty: Difficulty;
  description: string;
  cover_image: string | null;
  order: number;
  exercise_count: number;
}

export interface Exercise {
  id: number;
  title: string;
  text: string;
  max_score: number;
  order: number;
  level: number;
  level_name: string;
  created_at: string;
}

export interface WordAnalysis {
  expected: string;
  transcribed: string;
  is_correct: boolean;
  similarity: number;
}

export interface SessionFeedback {
  overall_comment: string;
  suggestions: string[];
  correct_words: string[];
  incorrect_words: Array<{ expected: string; got: string; similarity: number }>;
  missing_words: string[];
  word_analysis: WordAnalysis[];
}

export interface ReadingSession {
  id: number;
  exercise: number;
  exercise_title: string;
  level_name: string;
  level_slug: string;
  score: number;
  accuracy: number;
  transcription: string;
  feedback: SessionFeedback;
  duration_seconds: number;
  created_at: string;
}

export interface LevelStats {
  level_name: string;
  level_slug: string;
  difficulty: Difficulty;
  total_sessions: number;
  avg_score: number;
  avg_accuracy: number;
  best_score: number;
  total_score: number;
}

export interface UserProgress {
  stats_by_level: LevelStats[];
  recent_sessions: ReadingSession[];
}
