++import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
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
  Languages,
  MapPin,
  Calendar,
  BookMarked,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  Info,
  X,
  Sparkles
} from 'lucide-react';
import { EntityHighlight, EntityLegend, EntitySummary } from './components/EntityHighlight';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [text, setText] = useState('');
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [error, setError] = useState(null);
  const [expandedConcept, setExpandedConcept] = useState(null);
  const [showTimeline, setShowTimeline] = useState(false);
  const [showMap, setShowMap] = useState(false);

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
                {/* Entity Highlights Section */}
                {result.detected_entities && result.detected_entities.length > 0 && (
                  <>
                    <EntitySummary entities={result.detected_entities} />

                    <div className="section-card">
                      <div className="flex items-start gap-3">
                        <div className="bg-gradient-to-br from-purple-100 to-pink-100 p-3 rounded-lg">
                          <Sparkles className="w-6 h-6 text-purple-600" />
                        </div>
                        <div className="flex-1">
                          <h3 className="text-xl font-bold text-gray-800 mb-3">
                            ✨ Interactive Cultural Context
                          </h3>
                          <EntityLegend />
                          <div className="bg-white p-4 rounded-lg border-2 border-purple-200">
                            <EntityHighlight
                              text={result.input_text}
                              entities={result.detected_entities}
                            />
                          </div>
                          <p className="text-xs text-gray-500 mt-2 italic">
                            💡 Hover over highlighted terms to see cultural background from Wikipedia
                          </p>
                        </div>
                      </div>
                    </div>
                  </>
                )}

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
                      <div className="text-gray-700 leading-relaxed prose prose-sm max-w-none">
                        <ReactMarkdown>{result.cultural_origin}</ReactMarkdown>
                      </div>
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
                      <div className="text-gray-700 leading-relaxed prose prose-sm max-w-none">
                        <ReactMarkdown>{result.cross_cultural_connections}</ReactMarkdown>
                      </div>
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
                      <div className="text-gray-700 leading-relaxed prose prose-sm max-w-none">
                        <ReactMarkdown>{result.modern_analogy}</ReactMarkdown>
                      </div>
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
                      <div className="text-gray-700 leading-relaxed mb-3 prose prose-sm max-w-none">
                        <ReactMarkdown>{result.visualization_description}</ReactMarkdown>
                      </div>
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

                {/* Interactive Timeline */}
                {result.timeline_events && result.timeline_events.length > 0 && (
                  <div className="section-card">
                    <div className="flex items-start gap-3">
                      <div className="bg-indigo-100 p-3 rounded-lg">
                        <Calendar className="w-6 h-6 text-indigo-600" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-3">
                          <h3 className="text-xl font-bold text-gray-800">
                            📅 Historical Timeline
                          </h3>
                          <button
                            onClick={() => setShowTimeline(!showTimeline)}
                            className="text-sm text-indigo-600 hover:text-indigo-700 flex items-center gap-1"
                          >
                            {showTimeline ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                            {showTimeline ? 'Collapse' : 'Expand'}
                          </button>
                        </div>

                        {showTimeline && (
                          <div className="relative pl-6 border-l-2 border-indigo-300 space-y-4">
                            {result.timeline_events.map((event, idx) => (
                              <div key={idx} className="relative">
                                <div className="absolute -left-[25px] w-4 h-4 rounded-full bg-indigo-600 border-4 border-white"></div>
                                <div className="bg-indigo-50 p-4 rounded-lg">
                                  <div className="flex items-start justify-between gap-2 mb-2">
                                    <span className="font-bold text-indigo-900">{event.year}</span>
                                    <span className="text-xs bg-indigo-200 text-indigo-800 px-2 py-1 rounded-full">
                                      Event {idx + 1}
                                    </span>
                                  </div>
                                  <h4 className="font-semibold text-gray-800 mb-1">{event.title}</h4>
                                  <p className="text-sm text-gray-700 mb-2">{event.description}</p>
                                  <div className="text-xs text-indigo-700 bg-white p-2 rounded border border-indigo-200">
                                    <strong>Significance:</strong> {event.significance}
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Interactive Map Locations */}
                {result.geographic_locations && result.geographic_locations.length > 0 && (
                  <div className="section-card">
                    <div className="flex items-start gap-3">
                      <div className="bg-teal-100 p-3 rounded-lg">
                        <MapPin className="w-6 h-6 text-teal-600" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-3">
                          <h3 className="text-xl font-bold text-gray-800">
                            🗺️ Geographic Context
                          </h3>
                          <button
                            onClick={() => setShowMap(!showMap)}
                            className="text-sm text-teal-600 hover:text-teal-700 flex items-center gap-1"
                          >
                            {showMap ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                            {showMap ? 'Collapse' : 'Expand'}
                          </button>
                        </div>

                        {showMap && (
                          <div className="space-y-3">
                            {result.geographic_locations.map((location, idx) => (
                              <div key={idx} className="bg-teal-50 p-4 rounded-lg border border-teal-200">
                                <div className="flex items-start justify-between gap-2 mb-2">
                                  <h4 className="font-bold text-teal-900">{location.name}</h4>
                                  <MapPin className="w-4 h-4 text-teal-600" />
                                </div>
                                {location.modern_name && location.modern_name !== location.name && (
                                  <p className="text-xs text-teal-700 mb-2">
                                    Modern name: <span className="font-semibold">{location.modern_name}</span>
                                  </p>
                                )}
                                <p className="text-sm text-gray-700 mb-2">{location.significance}</p>
                                {location.coordinates && (
                                  <div className="flex gap-2 mt-2">
                                    <a
                                      href={`https://www.google.com/maps/search/?api=1&query=${location.coordinates.lat},${location.coordinates.lng}`}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="text-xs bg-teal-600 text-white px-3 py-1 rounded-full hover:bg-teal-700 flex items-center gap-1"
                                    >
                                      <ExternalLink className="w-3 h-3" />
                                      View on Google Maps
                                    </a>
                                    <span className="text-xs text-gray-500">
                                      {location.coordinates.lat.toFixed(4)}, {location.coordinates.lng.toFixed(4)}
                                    </span>
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Key Concepts (Pop-out Explainers) */}
                {result.key_concepts && result.key_concepts.length > 0 && (
                  <div className="section-card">
                    <div className="flex items-start gap-3">
                      <div className="bg-pink-100 p-3 rounded-lg">
                        <BookMarked className="w-6 h-6 text-pink-600" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-800 mb-3">
                          📖 Key Concepts Explained
                        </h3>
                        <p className="text-sm text-gray-600 mb-3">
                          Click on any concept to learn more
                        </p>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {result.key_concepts.map((concept, idx) => (
                            <div key={idx}>
                              <button
                                onClick={() => setExpandedConcept(expandedConcept === idx ? null : idx)}
                                className="w-full text-left bg-pink-50 hover:bg-pink-100 p-3 rounded-lg border-2 border-pink-200 transition-all"
                              >
                                <div className="flex items-center justify-between">
                                  <span className="font-semibold text-pink-900">{concept.term}</span>
                                  <Info className={`w-4 h-4 text-pink-600 transition-transform ${expandedConcept === idx ? 'rotate-180' : ''}`} />
                                </div>
                              </button>

                              {/* Pop-out Explainer */}
                              {expandedConcept === idx && (
                                <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 animate-fade-in">
                                  <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto">
                                    <div className="bg-gradient-to-r from-pink-600 to-rose-600 text-white p-6 rounded-t-xl">
                                      <div className="flex items-start justify-between">
                                        <div>
                                          <h4 className="text-2xl font-bold mb-1">{concept.term}</h4>
                                          <p className="text-pink-100 text-sm">Cultural Context Explainer</p>
                                        </div>
                                        <button
                                          onClick={() => setExpandedConcept(null)}
                                          className="text-white hover:text-pink-200"
                                        >
                                          <X className="w-6 h-6" />
                                        </button>
                                      </div>
                                    </div>

                                    <div className="p-6 space-y-4">
                                      <div>
                                        <h5 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
                                          <BookMarked className="w-5 h-5 text-pink-600" />
                                          Definition
                                        </h5>
                                        <p className="text-gray-700 leading-relaxed bg-gray-50 p-3 rounded-lg">
                                          {concept.definition}
                                        </p>
                                      </div>

                                      <div>
                                        <h5 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
                                          <Globe className="w-5 h-5 text-blue-600" />
                                          Cultural Context
                                        </h5>
                                        <p className="text-gray-700 leading-relaxed bg-blue-50 p-3 rounded-lg">
                                          {concept.context}
                                        </p>
                                      </div>

                                      <div>
                                        <h5 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
                                          <Lightbulb className="w-5 h-5 text-green-600" />
                                          Modern Connection
                                        </h5>
                                        <p className="text-gray-700 leading-relaxed bg-green-50 p-3 rounded-lg">
                                          {concept.modern_parallel}
                                        </p>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* External Resources */}
                {result.external_resources && Object.keys(result.external_resources).some(key => result.external_resources[key]?.length > 0) && (
                  <div className="section-card">
                    <div className="flex items-start gap-3">
                      <div className="bg-cyan-100 p-3 rounded-lg">
                        <ExternalLink className="w-6 h-6 text-cyan-600" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-800 mb-3">
                          🔗 Learn More
                        </h3>
                        <div className="space-y-3">
                          {result.external_resources.timeline_links?.length > 0 && (
                            <div>
                              <h4 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
                                <Calendar className="w-4 h-4" />
                                Interactive Timelines
                              </h4>
                              <div className="space-y-1">
                                {result.external_resources.timeline_links.map((link, idx) => (
                                  <a
                                    key={idx}
                                    href={link}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="block text-sm text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1"
                                  >
                                    <ExternalLink className="w-3 h-3" />
                                    {link}
                                  </a>
                                ))}
                              </div>
                            </div>
                          )}

                          {result.external_resources.map_links?.length > 0 && (
                            <div>
                              <h4 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
                                <MapPin className="w-4 h-4" />
                                Interactive Maps
                              </h4>
                              <div className="space-y-1">
                                {result.external_resources.map_links.map((link, idx) => (
                                  <a
                                    key={idx}
                                    href={link}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="block text-sm text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1"
                                  >
                                    <ExternalLink className="w-3 h-3" />
                                    {link}
                                  </a>
                                ))}
                              </div>
                            </div>
                          )}

                          {result.external_resources.further_reading?.length > 0 && (
                            <div>
                              <h4 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
                                📚 Further Reading
                              </h4>
                              <div className="space-y-1">
                                {result.external_resources.further_reading.map((link, idx) => (
                                  <a
                                    key={idx}
                                    href={link}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="block text-sm text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1"
                                  >
                                    <ExternalLink className="w-3 h-3" />
                                    {link}
                                  </a>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                )}
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
