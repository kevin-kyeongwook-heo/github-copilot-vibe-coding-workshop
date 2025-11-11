import { useState, useEffect } from 'react'
import Home from './components/Home'
import Search from './components/Search'
import PostDetails from './components/PostDetails'
import NameInputModal from './components/NameInputModal'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('home')
  const [selectedPostId, setSelectedPostId] = useState(null)
  const [username, setUsername] = useState(null)
  const [showNameModal, setShowNameModal] = useState(false)

  useEffect(() => {
    // Check if username exists in localStorage
    const savedUsername = localStorage.getItem('username')
    if (savedUsername) {
      setUsername(savedUsername)
    } else {
      setShowNameModal(true)
    }
  }, [])

  const handleUsernameSubmit = (newUsername) => {
    setUsername(newUsername)
    localStorage.setItem('username', newUsername)
    setShowNameModal(false)
  }

  const handleViewPost = (postId) => {
    setSelectedPostId(postId)
    setCurrentPage('postDetails')
  }

  const handleBackToHome = () => {
    setSelectedPostId(null)
    setCurrentPage('home')
  }

  const handleBackToSearch = () => {
    setSelectedPostId(null)
    setCurrentPage('search')
  }

  return (
    <div className="app">
      {showNameModal && <NameInputModal onSubmit={handleUsernameSubmit} />}
      
      {currentPage !== 'postDetails' && (
        <nav className="navigation">
          <button 
            className={currentPage === 'home' ? 'nav-button active' : 'nav-button'}
            onClick={() => setCurrentPage('home')}
          >
            Home
          </button>
          <button 
            className={currentPage === 'search' ? 'nav-button active' : 'nav-button'}
            onClick={() => setCurrentPage('search')}
          >
            Search
          </button>
        </nav>
      )}
      
      {currentPage === 'postDetails' && (
        <nav className="navigation">
          <button 
            className="nav-button"
            onClick={handleBackToHome}
          >
            ← Back to Home
          </button>
          <button 
            className="nav-button"
            onClick={handleBackToSearch}
          >
            ← Back to Search
          </button>
        </nav>
      )}
      
      {currentPage === 'home' && <Home onViewPost={handleViewPost} username={username} />}
      {currentPage === 'search' && <Search onViewPost={handleViewPost} username={username} />}
      {currentPage === 'postDetails' && selectedPostId && <PostDetails postId={selectedPostId} username={username} />}
    </div>
  )
}

export default App
