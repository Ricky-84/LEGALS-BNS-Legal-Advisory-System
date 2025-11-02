import React, { useState, useRef, useEffect } from 'react';
import './AppModern.css';

function AppModern() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Welcome to LEGALS 🏛️\nYour AI Legal Assistant\n\nStart by describing your legal situation...\nExample: 'Someone damaged my property...'"
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState('en');
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = { sender: "user", text: input };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    const currentInput = input;
    setInput("");

    try {
      // API call to your trained SLM backend
      const response = await fetch('/api/v1/legal/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: currentInput,
          language: language
        }),
      });

      if (response.ok) {
        const result = await response.json();

        // Create structured bot response
        const botMessage = {
          sender: "bot",
          text: "",
          legalResponse: result,
          type: "legal_analysis"
        };

        setMessages(prev => [...prev, botMessage]);
      } else {
        const errorMessage = {
          sender: "bot",
          text: "I apologize, but I encountered an error processing your legal query. Please try again or consult with a qualified lawyer.",
          type: "error"
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = {
        sender: "bot",
        text: "Network error. Please check your connection and try again.",
        type: "error"
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'en' ? 'hi' : 'en');
  };

  const toggleDarkMode = () => {
    setDarkMode(prev => !prev);
  };

  const formatConfidenceScore = (score) => {
    const percentage = Math.round(score * 100);
    let color = '#e53e3e'; // Red for low
    if (percentage >= 70) color = '#f6ad55'; // Amber for medium
    if (percentage >= 85) color = '#48bb78'; // Green for high

    return { percentage, color };
  };

  const renderLegalResponse = (legalData) => {
    const { entities, applicable_laws, legal_advice, confidence_score, processing_time, disclaimers } = legalData;
    const confidence = formatConfidenceScore(confidence_score);

    return (
      <div className="legal-response-card">
        {/* Header with confidence and timing */}
        <div className="response-header">
          <div className="confidence-badge">
            <span className="confidence-icon">●</span>
            <span>Confidence: </span>
            <span
              className="confidence-score"
              style={{ color: confidence.color }}
            >
              {confidence.percentage}%
            </span>
          </div>
          <div className="timing">
            <span className="time-icon">●</span>
            <span>{processing_time?.toFixed(1)}s</span>
          </div>
        </div>

        {/* Entities Section */}
        {entities && Object.keys(entities).some(key => entities[key].length > 0) && (
          <div className="response-section">
            <h4 className="section-title">
              <span className="section-icon">●</span>
              Entities Detected
            </h4>
            <div className="entities-grid">
              {Object.entries(entities).map(([category, items]) =>
                items.length > 0 && (
                  <div key={category} className="entity-group">
                    <span className="entity-category">
                      {getCategoryIcon(category)} {formatCategory(category)}:
                    </span>
                    <span className="entity-items">{items.join(', ')}</span>
                  </div>
                )
              )}
            </div>
          </div>
        )}

        {/* Applicable Laws Section */}
        {applicable_laws && applicable_laws.length > 0 && (
          <div className="response-section">
            <h4 className="section-title">
              <span className="section-icon">●</span>
              Applicable Laws
            </h4>
            <div className="laws-list">
              {applicable_laws.map((law, index) => (
                <div key={index} className="law-item">
                  <div className="law-header">
                    <span className="law-section">{law.section}</span>
                    <span className="law-title">{law.title}</span>
                    {law.confidence && (
                      <span
                        className="law-confidence"
                        style={{ color: formatConfidenceScore(law.confidence).color }}
                      >
                        {formatConfidenceScore(law.confidence).percentage}%
                      </span>
                    )}
                  </div>
                  {law.description && (
                    <p className="law-description">{law.description}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Legal Guidance Section */}
        {legal_advice && (
          <div className="response-section">
            <h4 className="section-title">
              <span className="section-icon">●</span>
              Legal Guidance
            </h4>
            <div className="legal-advice">
              {legal_advice.split('\n').map((paragraph, index) => (
                paragraph.trim() && <p key={index}>{paragraph}</p>
              ))}
            </div>
          </div>
        )}

        {/* Disclaimers Section */}
        {disclaimers && disclaimers.length > 0 && (
          <div className="response-section disclaimers">
            <h4 className="section-title">
              <span className="section-icon">●</span>
              Important Disclaimers
            </h4>
            <ul className="disclaimer-list">
              {disclaimers.map((disclaimer, index) => (
                <li key={index}>{disclaimer}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Quick Actions */}
        <div className="quick-actions">
          <button className="action-btn primary">Find Lawyer</button>
          <button className="action-btn secondary">Report to Police</button>
          <button className="action-btn secondary">Copy Analysis</button>
        </div>
      </div>
    );
  };

  const getCategoryIcon = (category) => {
    const icons = {
      persons: '●',
      objects: '●',
      locations: '●',
      actions: '●',
      intentions: '●',
      circumstances: '●',
      relationships: '●'
    };
    return icons[category] || '●';
  };

  const formatCategory = (category) => {
    return category.charAt(0).toUpperCase() + category.slice(1);
  };

  const renderMessage = (msg, index) => {
    if (msg.type === "legal_analysis") {
      return (
        <div key={index} className="message-container bot">
          <div className="message-avatar">
            <span className="avatar-icon">⚖</span>
          </div>
          <div className="message-content legal">
            {renderLegalResponse(msg.legalResponse)}
          </div>
        </div>
      );
    }

    return (
      <div key={index} className={`message-container ${msg.sender}`}>
        <div className="message-avatar">
          <span className="avatar-icon">
            {msg.sender === 'user' ? '●' : '⚖'}
          </span>
        </div>
        <div className={`message-content ${msg.type === 'error' ? 'error' : ''}`}>
          <div className="message-bubble">
            {msg.text.split('\n').map((line, i) => (
              <div key={i}>{line}</div>
            ))}
          </div>
          {msg.sender === 'bot' && (
            <div className="message-timestamp">
              {new Date().toLocaleTimeString()}
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className={`app-modern ${darkMode ? 'dark-mode' : ''}`}>
      {/* Header */}
      <header className="modern-header">
        <div className="header-left">
          <button
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            ☰
          </button>
          <div className="logo">
            <span className="logo-icon">⚖</span>
            <div className="logo-text">
              <h1>LEGALS</h1>
              <span>Legal AI Assistant</span>
            </div>
          </div>
        </div>

        <div className="header-right">
          <button
            className={`lang-toggle ${language === 'hi' ? 'hi' : ''}`}
            onClick={toggleLanguage}
          >
            <span className="flag">●</span>
            {language === 'en' ? 'EN' : 'हि'}
          </button>
          <button
            className="theme-toggle"
            onClick={toggleDarkMode}
          >
            {darkMode ? '◐' : '◑'}
          </button>
          <div className="profile">
            <span className="profile-icon">●</span>
          </div>
        </div>
      </header>

      <div className="main-container">
        {/* Sidebar */}
        <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
          <nav className="sidebar-nav">
            <div className="nav-section">
              <h3>RECENT QUERIES</h3>
              <ul>
                <li className="nav-item active">
                  <span className="nav-icon">●</span>
                  <span className="nav-text">Property Theft</span>
                </li>
                <li className="nav-item">
                  <span className="nav-icon">●</span>
                  <span className="nav-text">Contract Dispute</span>
                </li>
              </ul>
            </div>

            <div className="nav-section">
              <h3>LEGAL DATABASE</h3>
              <ul>
                <li className="nav-item">
                  <span className="nav-icon">●</span>
                  <span className="nav-text">BNS Sections</span>
                </li>
                <li className="nav-item">
                  <span className="nav-icon">●</span>
                  <span className="nav-text">Case Studies</span>
                </li>
              </ul>
            </div>

            <div className="nav-section">
              <h3>SETTINGS</h3>
              <ul>
                <li className="nav-item">
                  <span className="nav-icon">●</span>
                  <span className="nav-text">Profile</span>
                </li>
                <li className="nav-item">
                  <span className="nav-icon">●</span>
                  <span className="nav-text">Help</span>
                </li>
              </ul>
            </div>
          </nav>

          <div className="sidebar-footer">
            <div className="copyright">
              © 2025 LEGALS
            </div>
          </div>
        </aside>

        {/* Main Chat Area */}
        <main className="chat-container">
          <div className="chat-header">
            <h2>Legal AI Assistant</h2>
            <div className="chat-status">
              <span className="status-indicator online"></span>
              <span>Online</span>
            </div>
          </div>

          <div className="messages-container">
            {messages.map((msg, index) => renderMessage(msg, index))}

            {isLoading && (
              <div className="message-container bot">
                <div className="message-avatar">
                  <span className="avatar-icon">⚖</span>
                </div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <div className="typing-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    <span className="typing-text">Analyzing legal situation...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className="input-container">
            <div className="input-wrapper">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                  }
                }}
                placeholder="Describe your legal situation in detail..."
                className="message-input"
                rows="1"
                disabled={isLoading}
              />
              <div className="input-actions">
                <button
                  className="voice-btn"
                  title="Voice input"
                >
                  🎤
                </button>
                <button
                  onClick={sendMessage}
                  className={`send-btn ${input.trim() ? 'active' : ''}`}
                  disabled={isLoading || !input.trim()}
                >
                  {isLoading ? '⏳' : '📤'}
                </button>
              </div>
            </div>
            <div className="input-footer">
              <span className="disclaimer-text">
AI-generated legal information. Always consult a qualified lawyer.
              </span>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default AppModern;