import { useState } from 'react';
import apiService from '../services/api';
import './PostModal.css';

const PostModal = ({ onClose, onPostCreated, username }) => {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!content.trim()) {
      setError('Please enter some content for your post');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await apiService.createPost(username || 'Anonymous', content);
      setContent('');
      if (onPostCreated) {
        onPostCreated();
      }
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setContent('');
    setError(null);
    onClose();
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleSubmit();
    }
  };

  return (
    <div className="modal-overlay" onClick={handleCancel}>
      <div className="post-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-content-area">
          <textarea
            className="post-input"
            placeholder="How do you feel today?"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
          />
        </div>

        {error && (
          <div className="modal-error">{error}</div>
        )}

        <div className="modal-actions">
          <button 
            className="submit-button"
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? 'Submitting...' : 'Submit'}
          </button>
          <button 
            className="cancel-button"
            onClick={handleCancel}
            disabled={loading}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostModal;
