import { useState } from 'react';
import './NameInputModal.css';

const NameInputModal = ({ onSubmit }) => {
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = () => {
    if (!username.trim()) {
      setError('Please enter a username');
      return;
    }
    
    if (username.trim().length < 3) {
      setError('Username must be at least 3 characters');
      return;
    }

    onSubmit(username.trim());
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="name-modal-overlay">
      <div className="name-input-modal">
        <div className="modal-label">Enter your username</div>
        
        <div className="username-input-wrapper">
          <input
            type="text"
            className="username-input"
            placeholder="UserName"
            value={username}
            onChange={(e) => {
              setUsername(e.target.value);
              setError('');
            }}
            onKeyPress={handleKeyPress}
            autoFocus
          />
        </div>

        {error && (
          <div className="username-error">{error}</div>
        )}

        <button 
          className="ok-button"
          onClick={handleSubmit}
        >
          OK
        </button>
      </div>
    </div>
  );
};

export default NameInputModal;
