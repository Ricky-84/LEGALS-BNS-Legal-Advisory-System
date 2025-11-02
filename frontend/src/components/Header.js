import React from 'react';

const Header = ({ language, onLanguageChange, onToggleSidebar, onToggleTheme, isDarkMode }) => {
  const handleLanguageToggle = (lang) => {
    onLanguageChange(lang);
  };

  const getText = (enText, hiText) => {
    return language === 'hi' ? hiText : enText;
  };

  return (
    <header className="modern-header">
      <div className="header-left">
        <button className="sidebar-toggle" onClick={onToggleSidebar}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"/>
          </svg>
        </button>
        <div className="logo">
          <span className="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L13.09 8.26L15 7L16.74 9.74L23 8L19.5 13.5L21 15L17.23 18.77L19 20L12 22L5 20L6.77 18.77L3 15L4.5 13.5L1 8L7.26 9.74L9 7L10.91 8.26L12 2Z"/>
            </svg>
          </span>
          <div className="logo-text">
            <h1>
              {getText('LEGALS', 'कानूनी')}
            </h1>
            <span>
              {getText('Legal Assistant', 'कानूनी सहायक')}
            </span>
          </div>
        </div>
      </div>

      <div className="header-right">
        <div className={`lang-toggle ${language === 'hi' ? 'hi' : ''}`} onClick={() => onLanguageChange(language === 'en' ? 'hi' : 'en')}>
          <span className="flag">{language === 'en' ? '🇺🇸' : '🇮🇳'}</span>
          <span>{language === 'en' ? 'English' : 'हिन्दी'}</span>
        </div>
        <button className="theme-toggle" onClick={onToggleTheme}>
          {isDarkMode ? (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8M12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18M20,8.69V4H15.31L12,0.69L8.69,4H4V8.69L0.69,12L4,15.31V20H8.69L12,23.31L15.31,20H20V15.31L23.31,12L20,8.69Z"/>
            </svg>
          ) : (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17.75,4.09L15.22,6.03L16.13,9.09L13.5,7.28L10.87,9.09L11.78,6.03L9.25,4.09L12.44,4L13.5,1L14.56,4L17.75,4.09M21.25,11L19.61,12.25L20.2,14.23L18.5,13.06L16.8,14.23L17.39,12.25L15.75,11L17.81,10.95L18.5,9L19.19,10.95L21.25,11M18.97,15.95C19.8,15.87 20.69,17.05 20.16,17.8C19.84,18.25 19.5,18.67 19.08,19.07C15.17,23 8.84,23 4.94,19.07C1.03,15.17 1.03,8.83 4.94,4.93C5.34,4.53 5.76,4.17 6.21,3.85C6.96,3.32 8.14,4.21 8.06,5.04C7.79,7.9 8.75,10.87 10.95,13.06C13.14,15.26 16.1,16.22 18.97,15.95M17.33,17.97C14.5,17.81 11.7,16.64 9.53,14.5C7.36,12.31 6.2,9.5 6.04,6.68C3.23,9.82 3.34,14.4 6.35,17.41C9.37,20.43 14,20.54 17.33,17.97Z"/>
            </svg>
          )}
        </button>
        <div className="profile">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/>
          </svg>
        </div>
      </div>
    </header>
  );
};

export default Header;