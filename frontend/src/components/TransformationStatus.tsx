import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Clock, CheckCircle, AlertCircle, Download, Play, Pause } from 'lucide-react'
import toast from 'react-hot-toast'

interface TransformationStatusProps {
  jobId: string
  onComplete?: (outputUrl: string) => void
  onError?: (error: string) => void
}

interface JobStatus {
  job_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  progress: number
  message: string
  output_url?: string
  created_at: string
  updated_at: string
}

const TransformationStatus = ({ jobId, onComplete, onError }: TransformationStatusProps) => {
  const [status, setStatus] = useState<JobStatus | null>(null)
  const [polling, setPolling] = useState(true)

  const statusMessages = {
    pending: 'Waiting to start...',
    processing: 'Processing your video...',
    completed: 'Transformation completed!',
    failed: 'Transformation failed'
  }

  const statusIcons = {
    pending: Clock,
    processing: Clock,
    completed: CheckCircle,
    failed: AlertCircle
  }

  const statusColors = {
    pending: 'text-yellow-400',
    processing: 'text-blue-400',
    completed: 'text-green-400',
    failed: 'text-red-400'
  }

  useEffect(() => {
    if (!jobId) return

    const pollStatus = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/video/status/${jobId}`)
        if (!response.ok) throw new Error('Failed to fetch status')
        
        const data: JobStatus = await response.json()
        setStatus(data)

        if (data.status === 'completed') {
          setPolling(false)
          toast.success('Video transformation completed!')
          onComplete?.(data.output_url || '')
        } else if (data.status === 'failed') {
          setPolling(false)
          toast.error('Video transformation failed')
          onError?.(data.message)
        }
      } catch (error) {
        console.error('Error polling status:', error)
        toast.error('Failed to check transformation status')
      }
    }

    // Initial poll
    pollStatus()

    // Set up polling interval
    const interval = setInterval(() => {
      if (polling) {
        pollStatus()
      }
    }, 2000) // Poll every 2 seconds

    return () => clearInterval(interval)
  }, [jobId, polling, onComplete, onError])

  const downloadVideo = async () => {
    if (!status?.output_url) return

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/video/download/${jobId}`)
      if (!response.ok) throw new Error('Download failed')

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `aura_transformed_${jobId}.mp4`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)

      toast.success('Video downloaded successfully!')
    } catch (error) {
      console.error('Download error:', error)
      toast.error('Failed to download video')
    }
  }

  if (!status) {
    return (
      <div className="card">
        <div className="flex items-center justify-center space-x-2">
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-400"></div>
          <span className="text-dark-300">Loading status...</span>
        </div>
      </div>
    )
  }

  const StatusIcon = statusIcons[status.status]

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        className="card"
      >
        <div className="flex items-center space-x-4 mb-4">
          <div className={`p-3 rounded-full ${statusColors[status.status]}/20`}>
            <StatusIcon className={`h-6 w-6 ${statusColors[status.status]}`} />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-dark-100">
              {statusMessages[status.status]}
            </h3>
            <p className="text-sm text-dark-400">{status.message}</p>
          </div>
          {status.status === 'processing' && (
            <button
              onClick={() => setPolling(!polling)}
              className="p-2 hover:bg-dark-700 rounded transition-colors"
              title={polling ? 'Pause updates' : 'Resume updates'}
            >
              {polling ? (
                <Pause className="h-4 w-4 text-dark-400" />
              ) : (
                <Play className="h-4 w-4 text-dark-400" />
              )}
            </button>
          )}
        </div>

        {/* Progress Bar */}
        {status.status === 'processing' && (
          <div className="mb-4">
            <div className="flex justify-between text-sm text-dark-400 mb-2">
              <span>Progress</span>
              <span>{Math.round(status.progress)}%</span>
            </div>
            <div className="bg-dark-700 rounded-full h-2">
              <motion.div
                className="bg-primary-400 h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${status.progress}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          </div>
        )}

        {/* Job Info */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-dark-400 mb-4">
          <div>
            <span className="font-medium">Job ID:</span> {status.job_id}
          </div>
          <div>
            <span className="font-medium">Created:</span> {new Date(status.created_at).toLocaleString()}
          </div>
        </div>

        {/* Actions */}
        {status.status === 'completed' && status.output_url && (
          <div className="flex space-x-3">
            <button
              onClick={downloadVideo}
              className="btn-primary flex items-center space-x-2"
            >
              <Download className="h-4 w-4" />
              <span>Download Video</span>
            </button>
            <a
              href={status.output_url}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-outline flex items-center space-x-2"
            >
              <Play className="h-4 w-4" />
              <span>Preview</span>
            </a>
          </div>
        )}

        {status.status === 'failed' && (
          <div className="bg-red-400/10 border border-red-400/20 rounded-lg p-4">
            <div className="flex items-center space-x-2 text-red-400 mb-2">
              <AlertCircle className="h-4 w-4" />
              <span className="font-medium">Transformation Failed</span>
            </div>
            <p className="text-sm text-red-300">{status.message}</p>
          </div>
        )}
      </motion.div>
    </AnimatePresence>
  )
}

export default TransformationStatus 