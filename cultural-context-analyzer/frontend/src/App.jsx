import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  BookOpen, 
  Globe, 
  Lightbulb, 
  Image as ImageIcon, 
  History, 
  Loader2,
  Send,
  Trash2,
  Clock,
  Languages
} from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [text, setText] = useState('');
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [error, setError] = useState(null);

  // Fetch history on mount
  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/history?limit=10`);
      setHistory(response.data);
    } catch (err) {
      console.error('Error fetching history:', err);
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    
    if (!text.trim() || text.trim().length < 10) {
      setError('Please enter at least 10 characters of text to analyze.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/api/analyze`, {
        text: text.trim(),
        language: language
      });

      setResult(response.data);
      fetchHistory(); // Refresh history
      
    } catch (err) {
      console.error('Error analyzing text:', err);
      setError(err.response?.data?.detail || 'Failed to analyze text. Please check your API connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleHistoryClick = (item) => {
    setText(item.input_text);
    setLanguage(item.language);
    setResult(item);
    setShowHistory(false);
  };

  const handleDeleteHistory = async (id, e) => {
    e.stopPropagation();
    try {
      await axios.delete(`${API_URL}/api/analysis/${id}`);
      fetchHistory();
      if (result?.id === id) {
        setResult(null);
      }
    } catch (err) {
      console.error('Error deleting analysis:', err);
    }
  };

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'Hindi (हिंदी)' },
    { code: 'es', name: 'Spanish (Español)' },
    { code: 'fr', name: 'French (Français)' },
    { code: 'de', name: 'German (Deutsch)' },
    { code: 'zh', name: 'Chinese (中文)' },
    { code: 'ja', name: 'Japanese (日本語)' },
    { code: 'ar', name: 'Arabic (العربية)' },
    { code: 'bn', name: 'Bengali (বাংলা)' },
    { code: 'ta', name: 'Tamil (தமிழ்)' },
    { code: 'te', name: 'Telugu (తెలుగు)' },
    { code: 'mr', name: 'Marathi (मराठी)' },
  ];

  const exampleTexts = [
    "The Ramayana is an ancient Indian epic that tells the story of Prince Rama's quest to rescue his wife Sita from the demon king Ravana.",
    "Haiku is a traditional form of Japanese poetry consisting of three lines with a 5-7-5 syllable pattern, often focusing on nature and seasons.",
    "The Renaissance was a period of cultural rebirth in Europe, marked by renewed interest in classical art, literature, and learning.",
  ];

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="text-center mb-12 animate-fade-in">
          <div className="flex items-center justify-center gap-3 mb-4">
            <BookOpen className="w-12 h-12 text-blue-600" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Cultural Context Analyzer
            </h1>
          </div>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Discover the rich cultural heritage behind literature and historical texts. 
            Get insights on cultural origins, cross-cultural connections, modern analogies, and visual context.
          </p>
        </header>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Input Section */}
          <div className="lg:col-span-2">
            <div className="card animate-fade-in">
              <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Send className="w-6 h-6 text-blue-600" />
                Enter Text to Analyze
              </h2>
              
              <form onSubmit={handleAnalyze} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Language
                  </label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="input-field"
                  >
                    {languages.map(lang => (
                      <option key={lang.code} value={lang.code}>
                        {lang.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Text or Passage
                  </label>
                  <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Enter a poem, historical text, cultural reference, or any passage you'd like to understand better..."
                    className="input-field min-h-[200px] resize-y"
                    disabled={loading}
                  />
                </div>

                {/* Example Texts */}
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-2">Try an example:</p>
                  <div className="flex flex-wrap gap-2">
                    {exampleTexts.map((example, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => setText(example)}
                        className="text-xs bg-blue-50 text-blue-700 px-3 py-1 rounded-full hover:bg-blue-100 transition-colors"
                        disabled={loading}
                      >
                        Example {idx + 1}
                      </button>
                    ))}
                  </div>
                </div>

                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                    {error}
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading || !text.trim()}
                  className="btn-primary w-full flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Send className="w-5 h-5" />
                      Analyze Cultural Context
                    </>
                  )}
                </button>
              </form>
            </div>

            {/* Results Section */}
            {result && (
              <div className="mt-6 space-y-4 animate-fade-in">
                {/* Cultural Origin */}
                <div className="section-card">
                  <div className="flex items-start gap-3">
                    <div className="bg-blue-100 p-3 rounded-lg">
                      <Globe className="w-6 h-6 text-blue-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-gray-800 mb-2">
                        1. Cultural Origin
                      </h3>
                      <p className="text-gray-700 leading-relaxed">
                        {result.cultural_origin}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Cross-Cultural Connections */}
                <div className="section-card">
                  <div className="flex items-start gap-3">
                    <div className="bg-purple-100 p-3 rounded-lg">
                      <Languages className="w-6 h-6 text-purple-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-gray-800 mb-2">
                        2. Cross-Cultural Connections
                      </h3>
                      <p className="text-gray-700 leading-relaxed">
                        {result.cross_cultural_connections}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Modern Analogy */}
                <div className="section-card">
                  <div className="flex items-start gap-3">
                    <div className="bg-green-100 p-3 rounded-lg">
                      <Lightbulb className="w-6 h-6 text-green-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-gray-800 mb-2">
                        3. Modern Analogy
                      </h3>
                      <p className="text-gray-700 leading-relaxed">
                        {result.modern_analogy}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Visualization */}
                <div className="section-card">
                  <div className="flex items-start gap-3">
                    <div className="bg-orange-100 p-3 rounded-lg">
                      <ImageIcon className="w-6 h-6 text-orange-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-gray-800 mb-2">
                        4. Visualization Description
                      </h3>
                      <p className="text-gray-700 leading-relaxed mb-3">
                        {result.visualization_description}
                      </p>
                      {result.image_url && (
                        <div className="bg-gradient-to-r from-orange-50 to-yellow-50 p-4 rounded-lg border border-orange-200">
                          <p className="text-sm font-medium text-gray-700 mb-2">
                            Enhanced Image Generation Prompt:
                          </p>
                          <p className="text-sm text-gray-600 italic">
                            {result.image_url}
                          </p>
                          <p className="text-xs text-gray-500 mt-2">
                            Use this prompt with AI image generators like DALL-E, Midjourney, or Stable Diffusion
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar - History */}
          <div className="lg:col-span-1">
            <div className="card sticky top-8 animate-fade-in">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                  <History className="w-5 h-5 text-blue-600" />
                  Recent Analyses
                </h2>
                <button
                  onClick={() => setShowHistory(!showHistory)}
                  className="text-sm text-blue-600 hover:text-blue-700"
                >
                  {showHistory ? 'Hide' : 'Show'}
                </button>
              </div>

              {showHistory && (
                <div className="space-y-2 max-h-[600px] overflow-y-auto">
                  {history.length === 0 ? (
                    <p className="text-gray-500 text-sm text-center py-8">
                      No analyses yet. Start by analyzing some text!
                    </p>
                  ) : (
                    history.map((item) => (
                      <div
                        key={item.id}
                        onClick={() => handleHistoryClick(item)}
                        className="bg-gray-50 p-3 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors group"
                      >
                        <div className="flex items-start justify-between gap-2">
                          <div className="flex-1 min-w-0">
                            <p className="text-sm text-gray-700 line-clamp-2 mb-1">
                              {item.input_text}
                            </p>
                            <div className="flex items-center gap-2 text-xs text-gray-500">
                              <Clock className="w-3 h-3" />
                              {new Date(item.created_at).toLocaleDateString()}
                            </div>
                          </div>
                          <button
                            onClick={(e) => handleDeleteHistory(item.id, e)}
                            className="opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-700 transition-opacity"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-600 text-sm">
          <p>Powered by Google Gemini AI • Built for educational purposes</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
