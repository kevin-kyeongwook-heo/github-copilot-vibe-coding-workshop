import { useState, useEffect } from 'react';
import apiService from '../services/api';
import PostModal from './PostModal';
import './Home.css';

const Home = ({ onViewPost, username }) => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [connectionError, setConnectionError] = useState(false);
  const [showPostModal, setShowPostModal] = useState(false);

  const loadPosts = async () => {
    try {
      setLoading(true);
      setConnectionError(false);
      const data = await apiService.getPosts();
      setPosts(data);
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
    loadPosts();
  }, []);

  const handleLike = async (postId, username) => {
    try {
      await apiService.likePost(postId, username || 'Anonymous');
      await loadPosts();
    } catch (err) {
      setError(err.message);
    }
  };

  if (connectionError) {
    return (
      <div className="home">
        <div className="connection-error">
          <div className="error-icon">⚠️</div>
          <h2>Unable to Connect to Backend</h2>
          <p>The backend API is not available. Please check if the server is running at http://localhost:8000</p>
          <button onClick={loadPosts} className="retry-button">Retry Connection</button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="home">
        <div className="loading">Loading posts...</div>
      </div>
    );
  }

  return (
    <div className="home">
      <div className="sidebar-left"></div>
      
      <div className="feed-container">
        <button className="create-post-button" onClick={() => setShowPostModal(true)}>
          ✏️ Create Post
        </button>
        
        {error && !connectionError && (
          <div className="error-message">{error}</div>
        )}
        
        {posts.length === 0 ? (
          <div className="no-posts">No posts yet</div>
        ) : (
          posts.map((post) => (
            <div key={post.id} className="post-simple" onClick={() => onViewPost(post.id)} style={{ cursor: 'pointer' }}>
              <div className="post-header">
                <div className="user-avatar"></div>
                <div className="username">{post.username}</div>
              </div>
              
              <div className="post-content">
                <div className="post-text">{post.content}</div>
              </div>
              
              <div className="post-actions">
                <button 
                  className="action-button like-button"
                  onClick={() => handleLike(post.id, username || 'Anonymous')}
                  aria-label="Like post"
                >
                  <svg width="58" height="43" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                  </svg>
                  <span className="like-count">{post.likes}</span>
                </button>
                
                <button className="action-button comment-button" aria-label="Comment on post">
                  <svg width="55" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </button>
              </div>
              
              <div className="post-divider"></div>
            </div>
          ))
        )}
      </div>
      
      <div className="sidebar-right"></div>
      
      {showPostModal && (
        <PostModal 
          onClose={() => setShowPostModal(false)} 
          onPostCreated={loadPosts}
          username={username}
        />
      )}
    </div>
  );
};

export default Home;
