import React, { useState } from 'react';
import './AppModern.css';
import Header from './components/Header';
import QueryInput from './components/QueryInput';
import ResponseDisplay from './components/ResponseDisplay';

function App() {
  const [currentQuery, setCurrentQuery] = useState('');
  const [queryResponse, setQueryResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState('en');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isDarkMode, setIsDarkMode] = useState(false);

  const handleQuerySubmit = async (query) => {
    setCurrentQuery(query);
    setIsLoading(true);
    setQueryResponse(null);

    try {
      // Placeholder API call - will be implemented with actual backend
      const response = await fetch('/api/v1/legal/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          language: language
        }),
      });

      if (response.ok) {
        const result = await response.json();
        setQueryResponse(result);
      } else {
        setQueryResponse({
          error: 'Failed to process query. Please try again.'
        });
      }
    } catch (error) {
      setQueryResponse({
        error: 'Network error. Please check your connection and try again.'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div className={`app-modern ${isDarkMode ? 'dark-mode' : ''}`}>
      <Header
        language={language}
        onLanguageChange={handleLanguageChange}
        onToggleSidebar={toggleSidebar}
        onToggleTheme={toggleTheme}
        isDarkMode={isDarkMode}
      />
      <div className="main-container">
        <aside className={`sidebar ${!sidebarOpen ? 'closed' : ''}`}>
          <nav className="sidebar-nav">
            <div className="nav-section">
              <h3>{language === 'hi' ? 'कानूनी सहायक' : 'Legal Assistant'}</h3>
              <ul>
                <li className="nav-item active">
                  <span className="nav-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2L13.09 8.26L15 7L16.74 9.74L23 8L19.5 13.5L21 15L17.23 18.77L19 20L12 22L5 20L6.77 18.77L3 15L4.5 13.5L1 8L7.26 9.74L9 7L10.91 8.26L12 2Z"/>
                    </svg>
                  </span>
                  <span>{language === 'hi' ? 'नया प्रश्न' : 'New Query'}</span>
                </li>
                <li className="nav-item">
                  <span className="nav-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                    </svg>
                  </span>
                  <span>{language === 'hi' ? 'प्रश्न इतिहास' : 'Query History'}</span>
                </li>
                <li className="nav-item">
                  <span className="nav-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3M19,19H5V5H19V19Z"/>
                      <path d="M16.5,9.5L13,13L9.5,9.5H16.5Z"/>
                    </svg>
                  </span>
                  <span>{language === 'hi' ? 'कानूनी संसाधन' : 'Legal Resources'}</span>
                </li>
                <li className="nav-item">
                  <span className="nav-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22S19,14.25 19,9A7,7 0 0,0 12,2Z"/>
                    </svg>
                  </span>
                  <span>{language === 'hi' ? 'निकटतम वकील' : 'Find Lawyers'}</span>
                </li>
              </ul>
            </div>
            <div className="nav-section">
              <h3>{language === 'hi' ? 'सिस्टम' : 'System'}</h3>
              <ul>
                <li className="nav-item">
                  <span className="nav-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/>
                    </svg>
                  </span>
                  <span>{language === 'hi' ? 'सेटिंग्स' : 'Settings'}</span>
                </li>
                <li className="nav-item">
                  <span className="nav-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
                    </svg>
                  </span>
                  <span>{language === 'hi' ? 'परिचय' : 'About'}</span>
                </li>
                <li className="nav-item">
                  <span className="nav-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M21,16.5C21,16.88 20.79,17.21 20.47,17.38L12.57,21.82C12.41,21.94 12.21,22 12,22C11.79,22 11.59,21.94 11.43,21.82L3.53,17.38C3.21,17.21 3,16.88 3,16.5V7.5C3,7.12 3.21,6.79 3.53,6.62L11.43,2.18C11.59,2.06 11.79,2 12,2C12.21,2 12.41,2.06 12.57,2.18L20.47,6.62C20.79,6.79 21,7.12 21,7.5V16.5M12,4.15L5,8.09V15.91L12,19.85L19,15.91V8.09L12,4.15Z"/>
                    </svg>
                  </span>
                  <span>{language === 'hi' ? 'सहायता' : 'Help'}</span>
                </li>
              </ul>
            </div>
          </nav>
          <div className="sidebar-footer">
            <div className="copyright">
              © 2024 LEGALS<br/>
              Academic Project
            </div>
          </div>
        </aside>
        <main className="chat-container">
          <div className="chat-header">
            <h2>
              {language === 'hi' ? 'कानूनी सहायक' : 'Legal Assistant'}
            </h2>
            <div className="chat-status">
              <div className="status-indicator"></div>
              <span>{language === 'hi' ? 'तैयार है' : 'Ready'}</span>
            </div>
          </div>
          <div className="messages-container">
            <QueryInput
              onQuerySubmit={handleQuerySubmit}
              isLoading={isLoading}
              language={language}
            />
            <ResponseDisplay
              query={currentQuery}
              response={queryResponse}
              isLoading={isLoading}
              language={language}
            />
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;