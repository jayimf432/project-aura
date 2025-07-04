import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, Video, X, CheckCircle, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'

interface VideoUploadProps {
  onVideoUploaded: (jobId: string, filename: string) => void
  onUploadProgress?: (progress: number) => void
}

const VideoUpload = ({ onVideoUploaded, onUploadProgress }: VideoUploadProps) => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (!file) return

    // Validate file type
    const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/webm']
    if (!allowedTypes.includes(file.type)) {
      toast.error('Please upload a valid video file (MP4, AVI, MOV, MKV, or WebM)')
      return
    }

    // Validate file size (100MB limit)
    const maxSize = 100 * 1024 * 1024 // 100MB
    if (file.size > maxSize) {
      toast.error('File size must be less than 100MB')
      return
    }

    setUploadedFile(file)
    await uploadVideo(file)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    },
    multiple: false
  })

  const uploadVideo = async (file: File) => {
    setUploading(true)
    setUploadProgress(0)

    try {
      const formData = new FormData()
      formData.append('file', file)

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 200)

      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/video/upload`, {
        method: 'POST',
        body: formData
      })

      clearInterval(progressInterval)
      setUploadProgress(100)

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      const data = await response.json()
      
      toast.success('Video uploaded successfully!')
      onVideoUploaded(data.job_id, data.filename)
      
      // Reset progress after a delay
      setTimeout(() => {
        setUploadProgress(0)
        setUploading(false)
      }, 1000)

    } catch (error) {
      console.error('Upload error:', error)
      toast.error('Failed to upload video. Please try again.')
      setUploading(false)
      setUploadProgress(0)
    }
  }

  const removeFile = () => {
    setUploadedFile(null)
    setUploadProgress(0)
    setUploading(false)
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="w-full">
      <AnimatePresence>
        {!uploadedFile ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="w-full"
          >
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200 ${
                isDragActive
                  ? 'border-primary-400 bg-primary-400/10'
                  : 'border-dark-600 hover:border-primary-400 hover:bg-dark-700/50'
              }`}
            >
              <input {...getInputProps()} />
              
              <div className="flex flex-col items-center space-y-4">
                <div className={`p-4 rounded-full ${
                  isDragActive ? 'bg-primary-400/20' : 'bg-dark-700'
                }`}>
                  {uploading ? (
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-400"></div>
                  ) : (
                    <Upload className="h-8 w-8 text-primary-400" />
                  )}
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-dark-100 mb-2">
                    {uploading ? 'Uploading...' : 'Upload Video'}
                  </h3>
                  <p className="text-dark-300">
                    {isDragActive
                      ? 'Drop your video here'
                      : 'Drag & drop a video file, or click to browse'
                    }
                  </p>
                </div>

                {uploading && (
                  <div className="w-full max-w-xs">
                    <div className="bg-dark-700 rounded-full h-2">
                      <motion.div
                        className="bg-primary-400 h-2 rounded-full"
                        initial={{ width: 0 }}
                        animate={{ width: `${uploadProgress}%` }}
                        transition={{ duration: 0.3 }}
                      />
                    </div>
                    <p className="text-sm text-dark-400 mt-2">
                      {uploadProgress}% complete
                    </p>
                  </div>
                )}

                <div className="text-sm text-dark-400">
                  <p>Supported formats: MP4, AVI, MOV, MKV, WebM</p>
                  <p>Maximum file size: 100MB</p>
                </div>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="w-full"
          >
            <div className="card border-primary-500/50">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-primary-400/20 rounded-lg">
                  <Video className="h-6 w-6 text-primary-400" />
                </div>
                
                <div className="flex-1 min-w-0">
                  <h3 className="text-lg font-semibold text-dark-100 truncate">
                    {uploadedFile.name}
                  </h3>
                  <p className="text-sm text-dark-400">
                    {formatFileSize(uploadedFile.size)}
                  </p>
                </div>

                <div className="flex items-center space-x-2">
                  {uploadProgress === 100 ? (
                    <CheckCircle className="h-5 w-5 text-green-400" />
                  ) : uploading ? (
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-400"></div>
                  ) : (
                    <button
                      onClick={removeFile}
                      className="p-1 hover:bg-dark-600 rounded transition-colors"
                    >
                      <X className="h-4 w-4 text-dark-400 hover:text-red-400" />
                    </button>
                  )}
                </div>
              </div>

              {uploading && (
                <div className="mt-4">
                  <div className="bg-dark-700 rounded-full h-2">
                    <motion.div
                      className="bg-primary-400 h-2 rounded-full"
                      initial={{ width: 0 }}
                      animate={{ width: `${uploadProgress}%` }}
                      transition={{ duration: 0.3 }}
                    />
                  </div>
                  <p className="text-sm text-dark-400 mt-2">
                    {uploadProgress}% complete
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default VideoUpload 