export interface ResumeListItem {
  id: number;
  name: string;
  file: string;
  file_size: number;
  uploaded_at: string;
  updated_at: string;
  analysis_count: number;
}

export interface ResumeDetail extends ResumeListItem {
  extracted_text: string;
  extracted_skills: string[];
}
