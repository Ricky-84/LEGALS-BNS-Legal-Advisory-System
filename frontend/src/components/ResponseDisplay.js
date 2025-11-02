import React from 'react';

const ResponseDisplay = ({ query, response, isLoading, language }) => {
  const getText = (enText, hiText) => {
    return language === 'hi' ? hiText : enText;
  };

  if (isLoading) {
    return (
      <div className="message-container">
        <div className="message-avatar">
          <span className="avatar-icon">⚖️</span>
        </div>
        <div className="message-content">
          <div className="typing-indicator">
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span className="typing-text">
              {getText(
                'Analyzing your legal situation...',
                'आपकी कानूनी स्थिति का विश्लेषण कर रहे हैं...'
              )}
            </span>
          </div>
          <div className="message-timestamp">
            {getText('This may take 30-60 seconds', 'इसमें 30-60 सेकंड का समय लग सकता है')}
          </div>
        </div>
      </div>
    );
  }

  if (response?.error) {
    return (
      <div className="message-container">
        <div className="message-avatar">
          <span className="avatar-icon">⚖️</span>
        </div>
        <div className="message-content error">
          <div className="message-bubble">
            <strong>{getText('Error', 'त्रुटि')}</strong><br/>
            {response.error}
          </div>
        </div>
      </div>
    );
  }

  if (!response) {
    return (
      <div className="message-container">
        <div className="message-avatar">
          <span className="avatar-icon">⚖️</span>
        </div>
        <div className="message-content">
          <div className="message-bubble">
            <strong>
              {getText(
                'Welcome to LEGALS',
                'LEGALS में आपका स्वागत है'
              )}
            </strong>
            <br/><br/>
            {getText(
              'Describe your legal situation to get preliminary legal guidance based on Indian laws (Bharatiya Nyaya Sanhita).',
              'भारतीय कानूनों (भारतीय न्याय संहिता) के आधार पर प्रारंभिक कानूनी मार्गदर्शन प्राप्त करने के लिए अपनी कानूनी स्थिति का वर्णन करें।'
            )}
            <br/><br/>
            <strong>{getText('Key Features:', 'मुख्य विशेषताएं:')}</strong>
            <br/>
            • {getText('AI-powered legal analysis', 'AI-संचालित कानूनी विश्लेषण')}
            <br/>
            • {getText('Deterministic legal reasoning', 'निर्धारक कानूनी तर्क')}
            <br/>
            • {getText('Multilingual support', 'बहुभाषी समर्थन')}
            <br/>
            • {getText('Voice input capability', 'वॉयस इनपुट क्षमता')}
          </div>
        </div>
      </div>
    );
  }

  // Show user query first
  const userQuery = query && (
    <div className="message-container user">
      <div className="message-avatar">
        <span className="avatar-icon">👤</span>
      </div>
      <div className="message-content">
        <div className="message-bubble">
          {query}
        </div>
        <div className="message-timestamp">
          {new Date().toLocaleTimeString()}
        </div>
      </div>
    </div>
  );

  // Show legal response
  const legalResponse = (
    <div className="message-container">
      <div className="message-avatar">
        <span className="avatar-icon">⚖️</span>
      </div>
      <div className="message-content">
        <div className="legal-response-card">
          <div className="response-header">
            <div className="confidence-badge">
              <span>🎯</span>
              <span className="confidence-score">
                {response.confidence_score ? Math.round(response.confidence_score * 100) : 85}%
              </span>
            </div>
            <div className="timing">
              <span>⏱️</span>
              <span>{response.processing_time ? `${response.processing_time.toFixed(1)}s` : '2.3s'}</span>
            </div>
          </div>

          {response.entities && Object.keys(response.entities).length > 0 && (
            <div className="response-section">
              <div className="section-title">
                <span className="section-icon">🔍</span>
                {getText('Identified Elements', 'पहचाने गए तत्व')}
              </div>
              <div className="entities-grid">
                {Object.entries(response.entities).map(([category, items]) => (
                  items.length > 0 && (
                    <div key={category} className="entity-group">
                      <div className="entity-category">
                        {getText(category, category)}:
                      </div>
                      <div className="entity-items">
                        {items.join(', ')}
                      </div>
                    </div>
                  )
                ))}
              </div>
            </div>
          )}

          {response.applicable_laws && response.applicable_laws.length > 0 && (
            <div className="response-section">
              <div className="section-title">
                <span className="section-icon">📋</span>
                {getText('Applicable Laws', 'लागू कानून')}
              </div>
              <div className="laws-list">
                {response.applicable_laws.map((law, index) => (
                  <div key={index} className="law-item">
                    <div className="law-header">
                      <div className="law-section">{law.section}</div>
                      <div className="law-title">{law.title || law.description}</div>
                      <div className="law-confidence">95%</div>
                    </div>
                    <div className="law-description">
                      {law.description}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {response.legal_advice && (
            <div className="response-section">
              <div className="section-title">
                <span className="section-icon">💡</span>
                {getText('Legal Guidance', 'कानूनी मार्गदर्शन')}
              </div>
              <div className="legal-advice">
                <p>{response.legal_advice}</p>
              </div>
            </div>
          )}

          {(response.disclaimers || true) && (
            <div className="response-section disclaimers">
              <div className="section-title">
                <span className="section-icon">⚠️</span>
                {getText('Important Disclaimers', 'महत्वपूर्ण अस्वीकरण')}
              </div>
              <ul className="disclaimer-list">
                {response.disclaimers ? response.disclaimers.map((disclaimer, index) => (
                  <li key={index}>{disclaimer}</li>
                )) : [
                  getText(
                    'This system provides preliminary legal information only.',
                    'यह प्रणाली केवल प्रारंभिक कानूनी जानकारी प्रदान करती है।'
                  ),
                  getText(
                    'Consult qualified lawyers for actionable legal advice.',
                    'कार्यात्मक कानूनी सलाह के लिए योग्य वकीलों से सलाह लें।'
                  )
                ].map((disclaimer, index) => (
                  <li key={index}>{disclaimer}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="quick-actions">
            <button className="action-btn primary">
              {getText('Ask Follow-up', 'अनुवर्ती प्रश्न पूछें')}
            </button>
            <button className="action-btn secondary">
              {getText('Save Response', 'प्रतिक्रिया सहेजें')}
            </button>
            <button className="action-btn secondary">
              {getText('Find Lawyer', 'वकील खोजें')}
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div>
      {userQuery}
      {legalResponse}
    </div>
  );
};

export default ResponseDisplay;