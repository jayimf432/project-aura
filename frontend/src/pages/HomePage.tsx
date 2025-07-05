import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Sparkles, Video, Brain, Zap, ArrowRight } from 'lucide-react'

const HomePage = () => {
  const features = [
    {
      icon: Video,
      title: 'Video-to-Video Translation',
      description: 'Upload any video and transform its atmosphere while preserving motion and structure.',
      color: 'text-blue-400'
    },
    {
      icon: Brain,
      title: 'AI Creative Director',
      description: 'Get intelligent assistance in crafting the perfect transformation prompts.',
      color: 'text-purple-400'
    },
    {
      icon: Zap,
      title: 'High-Fidelity Output',
      description: 'Generate cinematic-quality videos with temporal consistency and no flickering.',
      color: 'text-green-400'
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary via-secondary to-primary">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-900/20 to-purple-900/20"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="mb-8"
            >
              <div className="flex justify-center mb-6">
                <div className="relative">
                  <Sparkles className="h-16 w-16 text-blue-400 animate-pulse-slow" />
                  <div className="absolute inset-0 bg-blue-400/20 rounded-full blur-xl"></div>
                </div>
              </div>
              
              <h1 className="text-5xl md:text-7xl font-bold mb-6">
                <span className="gradient-text">Project Aura</span>
              </h1>
              
              <p className="text-xl md:text-2xl text-secondary mb-8 max-w-3xl mx-auto">
                Transform the atmosphere of any video with AI-powered cinematic effects. 
                Create stunning visual transformations guided by an intelligent AI Creative Director.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <Link
                to="/transform"
                className="btn-primary inline-flex items-center justify-center px-8 py-4 text-lg font-semibold"
              >
                Start Transforming
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link
                to="/text-to-image"
                className="btn-secondary inline-flex items-center justify-center px-8 py-4 text-lg font-semibold"
              >
                Text-to-Image
              </Link>
              <Link
                to="/ai-director"
                className="btn-outline inline-flex items-center justify-center px-8 py-4 text-lg font-semibold"
              >
                Meet AI Director
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-secondary">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-primary mb-4">
              Powered by Cutting-Edge AI
            </h2>
            <p className="text-xl text-secondary max-w-2xl mx-auto">
              Our advanced AI technology combines multiple state-of-the-art models 
              to deliver exceptional video transformation results.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card hover:border-blue-500/50 transition-colors duration-300"
              >
                <div className={`${feature.color} mb-4`}>
                  <feature.icon className="h-12 w-12" />
                </div>
                <h3 className="text-xl font-semibold text-primary mb-3">
                  {feature.title}
                </h3>
                <p className="text-secondary leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-r from-blue-900/20 to-purple-900/20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-primary mb-6">
              Ready to Transform Your Videos?
            </h2>
            <p className="text-xl text-secondary mb-8">
              Join creators worldwide who are already using Project Aura to create 
              stunning cinematic transformations.
            </p>
            <Link
              to="/transform"
              className="btn-primary inline-flex items-center justify-center px-8 py-4 text-lg font-semibold"
            >
              Get Started Now
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default HomePage 