import { Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ThemeProvider } from './contexts/ThemeContext'
import Header from './components/Header'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
import VideoTransformPage from './pages/VideoTransformPage'
import AIDirectorPage from './pages/AIDirectorPage'
import AboutPage from './pages/AboutPage'
import TextToImagePage from './pages/TextToImagePage'

function App() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-primary flex flex-col">
        <Header />
        
        <main className="flex-1">
          <Routes>
            <Route 
              path="/" 
              element={
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <HomePage />
                </motion.div>
              } 
            />
            <Route 
              path="/transform" 
              element={
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <VideoTransformPage />
                </motion.div>
              } 
            />
            <Route 
              path="/ai-director" 
              element={
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <AIDirectorPage />
                </motion.div>
              } 
            />
            <Route 
              path="/about" 
              element={
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <AboutPage />
                </motion.div>
              } 
            />
            <Route 
              path="/text-to-image" 
              element={
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <TextToImagePage />
                </motion.div>
              } 
            />
          </Routes>
        </main>
        
        <Footer />
      </div>
    </ThemeProvider>
  )
}

export default App 