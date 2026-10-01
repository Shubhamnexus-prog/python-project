/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        blueprint: {
          950: '#081527',
          900: '#0B1F3A',
          800: '#0F2A4A',
          700: '#153964',
          line: '#6EC6FF',
          linefaint: '#2C4A6E',
        },
        paper: '#F3F5F7',
        ink: '#171B22',
        slate: {
          DEFAULT: '#5B6B7C',
          light: '#8A99A8',
        },
        amber: {
          DEFAULT: '#E8A33D',
          soft: '#F6D9A8',
        },
        signal: {
          low: '#5FB88A',
          medium: '#6EC6FF',
          high: '#E8A33D',
          urgent: '#E15B4F',
        },
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        body: ['"Inter"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      backgroundImage: {
        'grid-blueprint':
          'linear-gradient(rgba(110,198,255,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(110,198,255,0.08) 1px, transparent 1px)',
      },
      backgroundSize: {
        grid: '28px 28px',
      },
    },
  },
  plugins: [],
}
