/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: { ink: '#090b0d', panel: '#0d1114', line: '#263137', cyan: '#28d7e8', lime: '#b5e46c' },
      fontFamily: { sans: ['Inter', 'ui-sans-serif', 'system-ui'], mono: ['"JetBrains Mono"', 'monospace'] },
      boxShadow: { glow: '0 0 28px rgba(40, 215, 232, .16)' }
    }
  },
  plugins: []
};
