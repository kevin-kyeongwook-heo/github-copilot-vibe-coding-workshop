const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
    this.isConnected = true;
  }

  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Resource not found');
        }
        if (response.status === 400) {
          throw new Error('Bad request');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      this.isConnected = true;
      
      // Handle 204 No Content
      if (response.status === 204) {
        return null;
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'TypeError' || error.message.includes('fetch')) {
        this.isConnected = false;
        throw new Error('Unable to connect to backend API. Please check if the server is running.');
      }
      throw error;
    }
  }

  // Posts endpoints
  async getPosts() {
    return this.request('/posts');
  }

  async getPostById(postId) {
    return this.request(`/posts/${postId}`);
  }

  async createPost(username, content) {
    return this.request('/posts', {
      method: 'POST',
      body: JSON.stringify({ username, content }),
    });
  }

  async updatePost(postId, username, content) {
    return this.request(`/posts/${postId}`, {
      method: 'PATCH',
      body: JSON.stringify({ username, content }),
    });
  }

  async deletePost(postId) {
    return this.request(`/posts/${postId}`, {
      method: 'DELETE',
    });
  }

  // Comments endpoints
  async getComments(postId) {
    return this.request(`/posts/${postId}/comments`);
  }

  async getCommentById(postId, commentId) {
    return this.request(`/posts/${postId}/comments/${commentId}`);
  }

  async createComment(postId, username, content) {
    return this.request(`/posts/${postId}/comments`, {
      method: 'POST',
      body: JSON.stringify({ username, content }),
    });
  }

  async updateComment(postId, commentId, username, content) {
    return this.request(`/posts/${postId}/comments/${commentId}`, {
      method: 'PATCH',
      body: JSON.stringify({ username, content }),
    });
  }

  async deleteComment(postId, commentId) {
    return this.request(`/posts/${postId}/comments/${commentId}`, {
      method: 'DELETE',
    });
  }

  // Likes endpoints
  async likePost(postId, username) {
    return this.request(`/posts/${postId}/likes`, {
      method: 'POST',
      body: JSON.stringify({ username }),
    });
  }

  async unlikePost(postId, username) {
    return this.request(`/posts/${postId}/likes?username=${encodeURIComponent(username)}`, {
      method: 'DELETE',
    });
  }

  checkConnection() {
    return this.isConnected;
  }
}

export default new ApiService();
