import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API_URL = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000'

const TextToImagePage = () => {
  const [prompt, setPrompt] = useState('')
  const [negativePrompt, setNegativePrompt] = useState('')
  const [image, setImage] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setImage(null)
    try {
      const response = await fetch(`${API_URL}/api/v1/image/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          negative_prompt: negativePrompt,
          width: 512,
          height: 512,
          num_inference_steps: 30,
          guidance_scale: 7.5
        })
      })
      if (!response.ok) throw new Error('Failed to generate image')
      const blob = await response.blob()
      setImage(URL.createObjectURL(blob))
    } catch (err: any) {
      setError(err.message || 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary via-secondary to-primary">
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="relative max-w-4xl mx-auto py-16 px-4">
        {/* Header */}
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <motion.h1
            className="text-5xl md:text-6xl font-bold mb-4 gradient-text"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            Text-to-Image
          </motion.h1>
          <motion.p
            className="text-xl text-secondary max-w-2xl mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            Transform your imagination into stunning visuals with Stable Diffusion
          </motion.p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8 items-start">
          {/* Form Section */}
          <motion.div
            className="card backdrop-blur-sm"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <form onSubmit={handleGenerate} className="space-y-6">
              <div>
                <label className="block text-primary font-semibold mb-3 text-lg">
                  ✨ Describe Your Vision
                </label>
                <textarea
                  className="input-field w-full h-24 resize-none"
                  value={prompt}
                  onChange={e => setPrompt(e.target.value)}
                  placeholder="A majestic dragon soaring over a mystical forest at sunset..."
                  required
                />
              </div>
              
              <div>
                <label className="block text-primary font-semibold mb-3 text-lg">
                  🚫 What to Avoid (Optional)
                </label>
                <textarea
                  className="input-field w-full h-20 resize-none"
                  value={negativePrompt}
                  onChange={e => setNegativePrompt(e.target.value)}
                  placeholder="blurry, low quality, distorted..."
                />
              </div>

              <motion.button
                type="submit"
                className="w-full py-4 px-6 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold text-lg rounded-xl transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-500/50 shadow-lg"
                disabled={loading}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {loading ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Creating Magic...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center space-x-2">
                    <span>🎨 Generate Image</span>
                  </div>
                )}
              </motion.button>
            </form>

            {error && (
              <motion.div
                className="mt-6 p-4 bg-red-500/20 border border-red-500/30 rounded-lg text-red-300"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <div className="flex items-center space-x-2">
                  <span>⚠️</span>
                  <span>{error}</span>
                </div>
              </motion.div>
            )}
          </motion.div>

          {/* Image Display Section */}
          <motion.div
            className="card backdrop-blur-sm min-h-[400px] flex items-center justify-center"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <AnimatePresence mode="wait">
              {loading ? (
                <motion.div
                  key="loading"
                  className="text-center"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                  <p className="text-secondary text-lg">Crafting your masterpiece...</p>
                  <div className="mt-4 space-y-2">
                    <div className="w-32 h-2 bg-tertiary rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 animate-pulse"></div>
                    </div>
                  </div>
                </motion.div>
              ) : image ? (
                <motion.div
                  key="image"
                  className="w-full"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ duration: 0.5 }}
                >
                  <div className="relative group">
                    <img
                      src={image}
                      alt="Generated"
                      className="w-full h-auto rounded-xl shadow-2xl border border-primary"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-primary/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl"></div>
                    <motion.button
                      className="absolute top-4 right-4 bg-card/80 hover:bg-tertiary/80 text-primary p-2 rounded-lg opacity-0 group-hover:opacity-100 transition-all duration-300"
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => {
                        const link = document.createElement('a')
                        link.href = image
                        link.download = 'generated-image.png'
                        link.click()
                      }}
                    >
                      💾
                    </motion.button>
                  </div>
                  <p className="text-center text-secondary mt-4 text-sm">
                    Click the download button to save your image
                  </p>
                </motion.div>
              ) : (
                <motion.div
                  key="placeholder"
                  className="text-center text-tertiary"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <div className="w-24 h-24 mx-auto mb-4 text-6xl">🎨</div>
                  <p className="text-lg">Your generated image will appear here</p>
                  <p className="text-sm mt-2">Describe what you want to see and click generate</p>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>

        {/* Tips Section */}
        <motion.div
          className="mt-12 card backdrop-blur-sm"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <h3 className="text-xl font-semibold text-primary mb-4 flex items-center">
            💡 Pro Tips
          </h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm text-secondary">
            <div className="flex items-start space-x-2">
              <span className="text-blue-500">•</span>
              <span>Be specific with details like lighting, style, and mood</span>
            </div>
            <div className="flex items-start space-x-2">
              <span className="text-blue-500">•</span>
              <span>Use negative prompts to avoid unwanted elements</span>
            </div>
            <div className="flex items-start space-x-2">
              <span className="text-blue-500">•</span>
              <span>Try different art styles: "oil painting", "digital art", "photorealistic"</span>
            </div>
            <div className="flex items-start space-x-2">
              <span className="text-blue-500">•</span>
              <span>Add quality modifiers: "high quality", "detailed", "sharp focus"</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default TextToImagePage 