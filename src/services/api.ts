
const API_BASE_URL = 'http://localhost:5000';

export interface AnalysisRequest {
  url: string;
}

export interface AnalysisResponse {
  document_info: {
    url: string;
    title: string;
    word_count: number;
    character_count: number;
    analyzed_at: string;
  };
  readability: {
    score: number;
    basic_metrics: any;
    readability_scores: any;
    suggestions: string[];
  };
  structure: {
    score: number;
    heading_analysis: any;
    paragraph_analysis: any;
    suggestions: string[];
  };
  completeness: {
    score: number;
    suggestions: string[];
  };
  style: {
    score: number;
    suggestions: string[];
  };
  overall_score: number;
  summary: {
    strengths: string[];
    weaknesses: string[];
    priority_improvements: string[];
    recommendation: string;
  };
}

export const analyzeDocumentation = async (url: string): Promise<AnalysisResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('API Error:', error);
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Failed to analyze documentation. Please check if the backend server is running.');
  }
};
