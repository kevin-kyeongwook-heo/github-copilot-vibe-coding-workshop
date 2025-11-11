import { useState, useEffect } from 'react';
import apiService from '../services/api';
import './PostDetails.css';

const PostDetails = ({ postId, username }) => {
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [connectionError, setConnectionError] = useState(false);

  const loadPostAndComments = async () => {
    try {
      setLoading(true);
      setConnectionError(false);
      
      const [postData, commentsData] = await Promise.all([
        apiService.getPostById(postId),
        apiService.getComments(postId)
      ]);
      
      setPost(postData);
      setComments(commentsData);
      setError(null);
    } catch (err) {
      setError(err.message);
      if (err.message.includes('Unable to connect')) {
        setConnectionError(true);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (postId) {
      loadPostAndComments();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [postId]);

  const handleLike = async () => {
    try {
      await apiService.likePost(postId, username || 'Anonymous');
      await loadPostAndComments();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleAddComment = async () => {
    if (!newComment.trim()) {
      return;
    }

    try {
      await apiService.createComment(postId, username || 'Anonymous', newComment);
      setNewComment('');
      await loadPostAndComments();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAddComment();
    }
  };

  if (connectionError) {
    return (
      <div className="post-details">
        <div className="connection-error">
          <div className="error-icon">⚠️</div>
          <h2>Unable to Connect to Backend</h2>
          <p>The backend API is not available. Please check if the server is running at http://localhost:8000</p>
          <button onClick={loadPostAndComments} className="retry-button">Retry Connection</button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="post-details">
        <div className="loading">Loading post details...</div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="post-details">
        <div className="error-message">Post not found</div>
      </div>
    );
  }

  return (
    <div className="post-details">
      <div className="sidebar-left"></div>
      
      <div className="details-container">
        <div className="post-detail-card">
          <div className="post-header-detail">
            <div className="user-avatar"></div>
            <div className="username-bold">{post.username}</div>
          </div>
          
          <div className="post-content-detail">
            <div className="post-text-detail">{post.content}</div>
          </div>
          
          <div className="post-actions-detail">
            <button 
              className="action-button like-button"
              onClick={handleLike}
              aria-label="Like post"
            >
              <svg width="58" height="55" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
              </svg>
              <span className="like-count">{post.likes}</span>
            </button>
            
            <button className="action-button comment-button" aria-label="View comments">
              <svg width="55" height="61" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              </svg>
            </button>
          </div>
        </div>
        
        <div className="comments-section-scrollable">
          {comments.length === 0 ? (
            <div className="no-comments">No comments yet. Be the first to comment!</div>
          ) : (
            comments.map((comment) => (
              <div key={comment.id} className="comment-item">
                <div className="comment-avatar"></div>
                <div className="comment-content">
                  <div className="comment-username">{comment.username}</div>
                  <div className="comment-text">{comment.content}</div>
                </div>
              </div>
            ))
          )}
        </div>
        
        <div className="comment-input-section-fixed">
          <div className="comment-input-wrapper">
            <input
              type="text"
              className="comment-input"
              placeholder="Enter comment"
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              onKeyPress={handleKeyPress}
            />
          </div>
          <button 
            className="add-comment-button"
            onClick={handleAddComment}
            aria-label="Add comment"
          >
            <svg width="41" height="41" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </button>
        </div>
        
        {error && !connectionError && (
          <div className="error-message-inline">{error}</div>
        )}
      </div>
      
      <div className="sidebar-right"></div>
    </div>
  );
};

export default PostDetails;
