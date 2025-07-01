import { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Palette, Settings, Wand2 } from 'lucide-react'

interface TransformationFormProps {
  onSubmit: (data: TransformationData) => void
  loading?: boolean
}

export interface TransformationData {
  prompt: string
  conditions: string[]
  stylePreset: string
  quality: 'low' | 'medium' | 'high'
}

const TransformationForm = ({ onSubmit, loading = false }: TransformationFormProps) => {
  const [formData, setFormData] = useState<TransformationData>({
    prompt: '',
    conditions: [],
    stylePreset: 'natural',
    quality: 'high'
  })

  const [selectedConditions, setSelectedConditions] = useState<string[]>([])

  const stylePresets = [
    { id: 'natural', name: 'Natural', description: 'Clean, natural look with balanced colors' },
    { id: 'cinematic', name: 'Cinematic', description: 'Hollywood-style dramatic lighting' },
    { id: 'vintage', name: 'Vintage', description: 'Retro film look with warm tones' },
    { id: 'futuristic', name: 'Futuristic', description: 'Sci-fi aesthetic with neon lights' },
    { id: 'artistic', name: 'Artistic', description: 'Creative, artistic interpretation' }
  ]

  const conditionOptions = {
    time_of_day: ['sunrise', 'morning', 'noon', 'afternoon', 'sunset', 'twilight', 'night', 'midnight'],
    weather: ['clear', 'cloudy', 'rainy', 'stormy', 'foggy', 'misty', 'snowy', 'windy'],
    season: ['spring', 'summer', 'autumn', 'winter'],
    mood: ['peaceful', 'dramatic', 'mysterious', 'energetic', 'melancholic', 'romantic', 'tense']
  }

  const handleConditionToggle = (condition: string) => {
    setSelectedConditions(prev => {
      if (prev.includes(condition)) {
        return prev.filter(c => c !== condition)
      } else {
        return [...prev, condition]
      }
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.prompt.trim()) return

    const data = {
      ...formData,
      conditions: selectedConditions
    }
    onSubmit(data)
  }

  const generatePrompt = () => {
    const basePrompt = formData.prompt
    const conditions = selectedConditions.join(', ')
    const style = stylePresets.find(s => s.id === formData.stylePreset)?.name.toLowerCase()
    
    let generatedPrompt = basePrompt
    if (conditions) {
      generatedPrompt += `, ${conditions}`
    }
    if (style && style !== 'natural') {
      generatedPrompt += `, ${style} style`
    }
    
    setFormData(prev => ({ ...prev, prompt: generatedPrompt }))
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="w-full"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Main Prompt Input */}
        <div>
          <label className="block text-sm font-medium text-dark-100 mb-2">
            Transformation Prompt
          </label>
          <div className="relative">
            <textarea
              value={formData.prompt}
              onChange={(e) => setFormData(prev => ({ ...prev, prompt: e.target.value }))}
              placeholder="Describe the atmosphere you want to create... (e.g., 'a foggy autumn morning with golden light')"
              className="input-field w-full h-24 resize-none"
              required
            />
            <button
              type="button"
              onClick={generatePrompt}
              className="absolute top-2 right-2 p-2 text-primary-400 hover:text-primary-300 transition-colors"
              title="Generate prompt from conditions"
            >
              <Wand2 className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Style Preset Selection */}
        <div>
          <label className="block text-sm font-medium text-dark-100 mb-3">
            Style Preset
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {stylePresets.map((preset) => (
              <button
                key={preset.id}
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, stylePreset: preset.id }))}
                className={`p-4 rounded-lg border transition-all duration-200 text-left ${
                  formData.stylePreset === preset.id
                    ? 'border-primary-400 bg-primary-400/10'
                    : 'border-dark-600 hover:border-dark-500 bg-dark-800'
                }`}
              >
                <div className="flex items-center space-x-2 mb-2">
                  <Palette className="h-4 w-4 text-primary-400" />
                  <span className="font-medium text-dark-100">{preset.name}</span>
                </div>
                <p className="text-sm text-dark-400">{preset.description}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Condition Selection */}
        <div>
          <label className="block text-sm font-medium text-dark-100 mb-3">
            Atmospheric Conditions
          </label>
          <div className="space-y-4">
            {Object.entries(conditionOptions).map(([category, options]) => (
              <div key={category}>
                <h4 className="text-sm font-medium text-dark-200 mb-2 capitalize">
                  {category.replace('_', ' ')}
                </h4>
                <div className="flex flex-wrap gap-2">
                  {options.map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleConditionToggle(option)}
                      className={`px-3 py-1 rounded-full text-sm transition-all duration-200 ${
                        selectedConditions.includes(option)
                          ? 'bg-primary-400 text-white'
                          : 'bg-dark-700 text-dark-300 hover:bg-dark-600 hover:text-dark-100'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quality Selection */}
        <div>
          <label className="block text-sm font-medium text-dark-100 mb-3">
            Output Quality
          </label>
          <div className="flex space-x-4">
            {[
              { value: 'low', label: 'Low', desc: 'Faster processing' },
              { value: 'medium', label: 'Medium', desc: 'Balanced' },
              { value: 'high', label: 'High', desc: 'Best quality' }
            ].map((quality) => (
              <button
                key={quality.value}
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, quality: quality.value as any }))}
                className={`flex-1 p-4 rounded-lg border transition-all duration-200 ${
                  formData.quality === quality.value
                    ? 'border-primary-400 bg-primary-400/10'
                    : 'border-dark-600 hover:border-dark-500 bg-dark-800'
                }`}
              >
                <div className="text-center">
                  <div className="font-medium text-dark-100 mb-1">{quality.label}</div>
                  <div className="text-sm text-dark-400">{quality.desc}</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || !formData.prompt.trim()}
          className="btn-primary w-full py-4 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Processing...</span>
            </div>
          ) : (
            <div className="flex items-center justify-center space-x-2">
              <Sparkles className="h-5 w-5" />
              <span>Transform Video</span>
            </div>
          )}
        </button>
      </form>
    </motion.div>
  )
}

export default TransformationForm 