import { motion } from 'framer-motion'
import { Sun, Moon } from 'lucide-react'
import { useTheme } from '../contexts/ThemeContext'

const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme()

  return (
    <motion.button
      onClick={toggleTheme}
      className="relative p-2 rounded-xl bg-tertiary border border-primary transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-500/50"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      <motion.div
        className="relative w-6 h-6"
        initial={false}
        animate={{ rotate: theme === 'dark' ? 180 : 0 }}
        transition={{ duration: 0.3 }}
      >
        <motion.div
          className="absolute inset-0"
          initial={false}
          animate={{ 
            opacity: theme === 'light' ? 1 : 0,
            scale: theme === 'light' ? 1 : 0.8
          }}
          transition={{ duration: 0.2 }}
        >
          <Sun className="w-6 h-6 text-yellow-500" />
        </motion.div>
        
        <motion.div
          className="absolute inset-0"
          initial={false}
          animate={{ 
            opacity: theme === 'dark' ? 1 : 0,
            scale: theme === 'dark' ? 1 : 0.8
          }}
          transition={{ duration: 0.2 }}
        >
          <Moon className="w-6 h-6 text-blue-400" />
        </motion.div>
      </motion.div>
      
      {/* Glow effect */}
      <motion.div
        className="absolute inset-0 rounded-xl"
        initial={false}
        animate={{
          boxShadow: theme === 'dark' 
            ? '0 0 20px rgba(59, 130, 246, 0.3)' 
            : '0 0 20px rgba(245, 158, 11, 0.3)'
        }}
        transition={{ duration: 0.3 }}
      />
    </motion.button>
  )
}

export default ThemeToggle 