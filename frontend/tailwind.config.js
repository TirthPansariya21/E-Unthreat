/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: '#070B14',
          sidebar: '#0B101D',
          card: 'rgba(15, 22, 38, 0.85)',
          'card-solid': '#0F1626',
          border: 'rgba(30, 45, 75, 0.6)',
          'border-hover': 'rgba(56, 189, 248, 0.3)',
          cyan: '#38BDF8',
          blue: '#3B82F6',
          indigo: '#6366F1',
          danger: '#EF4444',
          warning: '#F59E0B',
          success: '#10B981',
          muted: '#64748B',
          text: '#F8FAFC',
          'text-secondary': '#94A3B8',
        }
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      boxShadow: {
        'cyan-glow': '0 0 20px rgba(56, 189, 248, 0.25)',
        'blue-glow': '0 0 25px rgba(59, 130, 246, 0.35)',
        'danger-glow': '0 0 25px rgba(239, 68, 68, 0.3)',
        'warning-glow': '0 0 25px rgba(245, 158, 11, 0.3)',
        'success-glow': '0 0 25px rgba(16, 185, 129, 0.3)',
      },
      animation: {
        'pulse-glow': 'pulseGlow 2.5s infinite ease-in-out',
        'fade-in': 'fadeIn 0.3s ease-out',
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.4', transform: 'scale(0.85)' },
        },
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(4px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
}
