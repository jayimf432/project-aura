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

      const response = await fetch(`${(import.meta as any).env.VITE_API_URL}/api/v1/video/upload`, {
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
                  ? 'border-blue-500 bg-blue-500/10'
                  : 'border-primary hover:border-blue-500 hover:bg-tertiary/50'
              }`}
            >
              <input {...getInputProps()} />
              
              <div className="flex flex-col items-center space-y-4">
                <div className={`p-4 rounded-full ${
                  isDragActive ? 'bg-blue-500/20' : 'bg-tertiary'
                }`}>
                  {uploading ? (
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                  ) : (
                    <Upload className="h-8 w-8 text-blue-500" />
                  )}
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-primary mb-2">
                    {uploading ? 'Uploading...' : 'Upload Video'}
                  </h3>
                  <p className="text-secondary">
                    {isDragActive
                      ? 'Drop your video here'
                      : 'Drag & drop a video file, or click to browse'
                    }
                  </p>
                </div>

                {uploading && (
                  <div className="w-full max-w-xs">
                    <div className="bg-tertiary rounded-full h-2">
                      <motion.div
                        className="bg-blue-500 h-2 rounded-full"
                        initial={{ width: 0 }}
                        animate={{ width: `${uploadProgress}%` }}
                        transition={{ duration: 0.3 }}
                      />
                    </div>
                    <p className="text-sm text-secondary mt-2">
                      {uploadProgress}% complete
                    </p>
                  </div>
                )}

                <div className="text-sm text-tertiary">
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
            <div className="card border-blue-500/50">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-blue-500/20 rounded-lg">
                  <Video className="h-6 w-6 text-blue-500" />
                </div>
                
                <div className="flex-1 min-w-0">
                  <h3 className="text-lg font-semibold text-primary truncate">
                    {uploadedFile.name}
                  </h3>
                  <p className="text-sm text-secondary">
                    {formatFileSize(uploadedFile.size)}
                  </p>
                </div>

                <div className="flex items-center space-x-2">
                  {uploadProgress === 100 ? (
                    <div className="flex items-center space-x-1 text-green-500">
                      <CheckCircle className="h-5 w-5" />
                      <span className="text-sm font-medium">Uploaded</span>
                    </div>
                  ) : uploading ? (
                    <div className="flex items-center space-x-1 text-blue-500">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                      <span className="text-sm font-medium">Uploading...</span>
                    </div>
                  ) : (
                    <button
                      onClick={removeFile}
                      className="p-2 text-tertiary hover:text-primary hover:bg-tertiary rounded-lg transition-colors duration-200"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default VideoUpload 