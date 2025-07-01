import { Link } from 'react-router-dom'
import { Sparkles, Github, Twitter, Mail } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-dark-800 border-t border-dark-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <Link to="/" className="flex items-center space-x-2 mb-4">
              <Sparkles className="h-6 w-6 text-primary-400" />
              <span className="text-lg font-bold gradient-text">Project Aura</span>
            </Link>
            <p className="text-dark-300 text-sm leading-relaxed max-w-md">
              Transform the atmosphere of any video with AI-powered cinematic effects. 
              Create stunning visual transformations with our intelligent AI Creative Director.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-dark-100 font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/transform" className="text-dark-300 hover:text-primary-400 text-sm transition-colors">
                  Video Transform
                </Link>
              </li>
              <li>
                <Link to="/ai-director" className="text-dark-300 hover:text-primary-400 text-sm transition-colors">
                  AI Director
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-dark-300 hover:text-primary-400 text-sm transition-colors">
                  About
                </Link>
              </li>
            </ul>
          </div>

          {/* Social Links */}
          <div>
            <h3 className="text-dark-100 font-semibold mb-4">Connect</h3>
            <div className="flex space-x-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-dark-300 hover:text-primary-400 transition-colors"
              >
                <Github className="h-5 w-5" />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-dark-300 hover:text-primary-400 transition-colors"
              >
                <Twitter className="h-5 w-5" />
              </a>
              <a
                href="mailto:contact@projectaura.com"
                className="text-dark-300 hover:text-primary-400 transition-colors"
              >
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-dark-700 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-dark-400 text-sm">
            © 2024 Project Aura. All rights reserved.
          </p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link to="/privacy" className="text-dark-400 hover:text-dark-300 text-sm transition-colors">
              Privacy Policy
            </Link>
            <Link to="/terms" className="text-dark-400 hover:text-dark-300 text-sm transition-colors">
              Terms of Service
            </Link>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer 