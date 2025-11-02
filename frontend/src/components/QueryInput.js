import React, { useState, useEffect } from 'react';

const QueryInput = ({ onQuerySubmit, isLoading, language }) => {
  const [query, setQuery] = useState('');
  const [isListening, setIsListening] = useState(false);

  const handleTextChange = (e) => {
    setQuery(e.target.value);
    // Auto-resize textarea
    e.target.style.height = 'auto';
    e.target.style.height = e.target.scrollHeight + 'px';
  };

  const getText = (enText, hiText) => {
    return language === 'hi' ? hiText : enText;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onQuerySubmit(query.trim());
    }
  };

  const handleVoiceInput = () => {
    // Placeholder for voice input - will be implemented with Web Speech API
    setIsListening(true);
    setTimeout(() => {
      setIsListening(false);
      alert(getText(
        'Voice input will be implemented in the next phase',
        'वॉयस इनपुट अगले चरण में लागू किया जाएगा'
      ));
    }, 1000);
  };

  const placeholderText = getText(
    'Describe your legal situation in detail. For example: "Someone stole my mobile phone from my bag while I was in a public bus. What legal action can I take?"',
    'अपनी कानूनी स्थिति का विस्तार से वर्णन करें। उदाहरण: "किसी ने सार्वजनिक बस में मेरे बैग से मेरा मोबाइल फोन चुराया। मैं क्या कानूनी कार्रवाई कर सकता हूं?"'
  );

  return (
    <div className="input-container">
      <div className="input-wrapper">
        <textarea
          className="message-input"
          value={query}
          onChange={handleTextChange}
          placeholder={placeholderText}
          maxLength={1000}
          disabled={isLoading}
          rows={1}
          style={{
            minHeight: '20px',
            height: 'auto',
            resize: 'none'
          }}
        />

        <div className="input-actions">
          <button
            type="button"
            className={`voice-btn ${isListening ? 'listening' : ''}`}
            onClick={handleVoiceInput}
            disabled={isLoading}
            title={getText('Voice Input', 'वॉयस इनपुट')}
          >
            🎤
          </button>

          <button
            type="submit"
            className={`send-btn ${query.trim() ? 'active' : ''}`}
            onClick={handleSubmit}
            disabled={isLoading || !query.trim()}
          >
            {isLoading ? '⏳' : '➤'}
          </button>
        </div>
      </div>

      <div className="input-footer">
        <div className="disclaimer-text">
          {getText(
            '⚠️ Preliminary legal information only. Consult qualified lawyers for actionable advice.',
            '⚠️ केवल प्रारंभिक कानूनी जानकारी। कार्यात्मक सलाह के लिए योग्य वकीलों से सलाह लें।'
          )}
        </div>
      </div>
    </div>
  );
};

export default QueryInput;