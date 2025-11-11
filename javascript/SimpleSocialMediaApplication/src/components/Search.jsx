import { useState } from 'react';
import apiService from '../services/api';
import './Search.css';

const Search = ({ onViewPost, username }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [connectionError, setConnectionError] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      return;
    }

    try {
      setLoading(true);
      setConnectionError(false);
      setHasSearched(true);
      
      // Get all posts and filter by search query
      const allPosts = await apiService.getPosts();
      const filteredPosts = allPosts.filter(post => 
        post.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
        post.username.toLowerCase().includes(searchQuery.toLowerCase())
      );
      
      setPosts(filteredPosts);
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

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleLike = async (postId, username) => {
    try {
      await apiService.likePost(postId, username || 'Anonymous');
      await handleSearch();
    } catch (err) {
      setError(err.message);
    }
  };

  if (connectionError) {
    return (
      <div className="search">
        <div className="connection-error">
          <div className="error-icon">⚠️</div>
          <h2>Unable to Connect to Backend</h2>
          <p>The backend API is not available. Please check if the server is running at http://localhost:8000</p>
          <button onClick={handleSearch} className="retry-button">Retry Connection</button>
        </div>
      </div>
    );
  }

  return (
    <div className="search">
      <div className="sidebar-left"></div>
      
      <div className="search-container">
        <div className="search-box-wrapper">
          <div className="search-input-container">
            <input
              type="text"
              className="search-input"
              placeholder="Enter keywords to search..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
            />
          </div>
          <button 
            className="search-button"
            onClick={handleSearch}
            aria-label="Search"
          >
            <svg width="35" height="35" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
          </button>
        </div>
        
        <div className="search-divider-top"></div>
        
        {loading && (
          <div className="loading-search">Searching...</div>
        )}
        
        {error && !connectionError && (
          <div className="error-message">{error}</div>
        )}
        
        {!loading && hasSearched && posts.length === 0 && (
          <div className="no-results">No posts found matching your search</div>
        )}
        
        {!loading && posts.length > 0 && (
          <>
            {posts.map((post, index) => (
              <div key={post.id}>
                <div className="post-simple" onClick={() => onViewPost(post.id)} style={{ cursor: 'pointer' }}>
                  <div className="post-header">
                    <div className="user-avatar"></div>
                    <div className="username-bold">{post.username}</div>
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
                </div>
                
                {index < posts.length - 1 && <div className="search-divider"></div>}
              </div>
            ))}
          </>
        )}
      </div>
      
      <div className="sidebar-right"></div>
    </div>
  );
};

export default Search;
