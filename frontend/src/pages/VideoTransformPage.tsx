import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Video, Sparkles, ArrowLeft } from 'lucide-react'
import VideoUpload from '../components/VideoUpload'
import TransformationForm, { TransformationData } from '../components/TransformationForm'
import TransformationStatus from '../components/TransformationStatus'
import toast from 'react-hot-toast'

type Step = 'upload' | 'transform' | 'status'

const VideoTransformPage = () => {
  const [currentStep, setCurrentStep] = useState<Step>('upload')
  const [jobId, setJobId] = useState<string>('')
  const [filename, setFilename] = useState<string>('')
  const [transforming, setTransforming] = useState(false)

  const handleVideoUploaded = (jobId: string, filename: string) => {
    setJobId(jobId)
    setFilename(filename)
    setCurrentStep('transform')
  }

  const handleTransformationSubmit = async (data: TransformationData) => {
    setTransforming(true)
    
    try {
      const response = await fetch(`${(import.meta as any).env.VITE_API_URL}/api/v1/video/transform?job_id=${jobId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: data.prompt,
          conditions: data.conditions,
          style_preset: data.stylePreset,
          quality: data.quality
        })
      })

      if (!response.ok) {
        throw new Error('Failed to start transformation')
      }

      const result = await response.json()
      setCurrentStep('status')
      toast.success('Transformation started successfully!')
      
    } catch (error) {
      console.error('Transformation error:', error)
      toast.error('Failed to start transformation. Please try again.')
    } finally {
      setTransforming(false)
    }
  }

  const handleTransformationComplete = (outputUrl: string) => {
    toast.success('Video transformation completed! You can now download your video.')
  }

  const handleTransformationError = (error: string) => {
    toast.error(`Transformation failed: ${error}`)
  }

  const resetProcess = () => {
    setCurrentStep('upload')
    setJobId('')
    setFilename('')
    setTransforming(false)
  }

  return (
    <div className="min-h-screen py-12 bg-primary">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Video className="h-8 w-8 text-blue-500" />
            <h1 className="text-4xl font-bold text-primary">Video Transformation</h1>
          </div>
          <p className="text-xl text-secondary">
            Upload your video and transform it with AI-powered cinematic effects
          </p>
        </motion.div>

        {/* Progress Steps */}
        <div className="flex items-center justify-center mb-8">
          <div className="flex items-center space-x-4">
            {[
              { step: 'upload', label: 'Upload Video', icon: Video },
              { step: 'transform', label: 'Configure', icon: Sparkles },
              { step: 'status', label: 'Processing', icon: Sparkles }
            ].map((item, index) => {
              const Icon = item.icon
              const isActive = currentStep === item.step
              const isCompleted = ['transform', 'status'].includes(currentStep) && index === 0 ||
                                currentStep === 'status' && index === 1
              
              return (
                <div key={item.step} className="flex items-center">
                  <div className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                    isActive 
                      ? 'bg-blue-500/20 text-blue-500' 
                      : isCompleted
                      ? 'bg-green-500/20 text-green-500'
                      : 'bg-tertiary text-tertiary'
                  }`}>
                    <Icon className="h-4 w-4" />
                    <span className="text-sm font-medium">{item.label}</span>
                  </div>
                  {index < 2 && (
                    <div className={`w-8 h-0.5 mx-2 ${
                      isCompleted ? 'bg-green-500' : 'bg-tertiary'
                    }`} />
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* Content */}
        <AnimatePresence mode="wait">
          {currentStep === 'upload' && (
            <motion.div
              key="upload"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="card">
                <h2 className="text-2xl font-semibold text-primary mb-6">
                  Upload Your Video
                </h2>
                <VideoUpload onVideoUploaded={handleVideoUploaded} />
              </div>
            </motion.div>
          )}

          {currentStep === 'transform' && (
            <motion.div
              key="transform"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="card">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-semibold text-primary">
                    Configure Transformation
                  </h2>
                  <button
                    onClick={resetProcess}
                    className="btn-outline flex items-center space-x-2"
                  >
                    <ArrowLeft className="h-4 w-4" />
                    <span>Upload New Video</span>
                  </button>
                </div>
                
                <div className="mb-6 p-4 bg-tertiary rounded-lg">
                  <div className="flex items-center space-x-3">
                    <Video className="h-5 w-5 text-blue-500" />
                    <div>
                      <p className="text-primary font-medium">{filename}</p>
                      <p className="text-sm text-secondary">Job ID: {jobId}</p>
                    </div>
                  </div>
                </div>

                <TransformationForm 
                  onSubmit={handleTransformationSubmit}
                  loading={transforming}
                />
              </div>
            </motion.div>
          )}

          {currentStep === 'status' && (
            <motion.div
              key="status"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="card">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-semibold text-primary">
                    Transformation Status
                  </h2>
                  <button
                    onClick={resetProcess}
                    className="btn-outline flex items-center space-x-2"
                  >
                    <ArrowLeft className="h-4 w-4" />
                    <span>Start New</span>
                  </button>
                </div>

                <TransformationStatus
                  jobId={jobId}
                  onComplete={handleTransformationComplete}
                  onError={handleTransformationError}
                />
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Help Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-12"
        >
          <div className="card">
            <h3 className="text-lg font-semibold text-primary mb-4">
              How It Works
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Video className="h-6 w-6 text-blue-500" />
                </div>
                <h4 className="font-medium text-primary mb-2">1. Upload Video</h4>
                <p className="text-sm text-secondary">
                  Upload any video file up to 100MB in MP4, AVI, MOV, MKV, or WebM format
                </p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Sparkles className="h-6 w-6 text-blue-500" />
                </div>
                <h4 className="font-medium text-primary mb-2">2. Configure</h4>
                <p className="text-sm text-secondary">
                  Describe the atmosphere you want and select style presets and conditions
                </p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Video className="h-6 w-6 text-blue-500" />
                </div>
                <h4 className="font-medium text-primary mb-2">3. Download</h4>
                <p className="text-sm text-secondary">
                  Wait for AI processing and download your transformed video
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default VideoTransformPage 