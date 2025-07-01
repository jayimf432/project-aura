import { motion } from 'framer-motion'

const AboutPage = () => {
  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <h1 className="text-4xl font-bold text-dark-100 mb-4">
            About Project Aura
          </h1>
          <p className="text-xl text-dark-300 mb-8">
            Learn more about our mission and technology.
          </p>
          <div className="card max-w-2xl mx-auto">
            <p className="text-dark-300">
              About page content coming soon...
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default AboutPage 