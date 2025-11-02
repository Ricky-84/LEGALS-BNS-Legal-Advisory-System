import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="container">
        <p>
          © {currentYear} LEGALS - Legal Empowerment and Awareness System
        </p>
        <p>
          <small>
            Academic Project | Not for Production Legal Advice | 
            Always Consult Qualified Legal Professionals
          </small>
        </p>
      </div>
    </footer>
  );
};

export default Footer;