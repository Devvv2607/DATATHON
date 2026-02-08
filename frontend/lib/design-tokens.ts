/**
 * TrendPulse Design System
 * Editorial data journalism meets Apple Vision Pro
 */

export const colors = {
  // Base: Deep neutral, NOT pitch black
  base: {
    ink: '#0A0E14',        // Primary background
    graphite: '#151922',   // Secondary surfaces
    charcoal: '#1F2937',   // Tertiary surfaces
    slate: '#374151',      // Borders
    fog: '#4B5563',        // Subtle elements
  },
  
  // Signal: Meaning-encoded colors (not decorative)
  signal: {
    amber: '#F59E0B',      // Warning/attention
    coral: '#F97316',      // Decline/risk
    acid: '#84CC16',       // Growth/positive
    cyan: '#06B6D4',       // Information/neutral
    electric: '#3B82F6',   // Primary actions
    violet: '#8B5CF6',     // Secondary actions
  },
  
  // Status colors (semantic)
  status: {
    emerging: '#84CC16',
    growth: '#06B6D4',
    peak: '#3B82F6',
    declining: '#F97316',
    dead: '#6B7280',
  },
  
  // Typography
  text: {
    primary: '#F9FAFB',
    secondary: '#D1D5DB',
    tertiary: '#9CA3AF',
    muted: '#6B7280',
  },
  
  // Gradients
  gradients: {
    lifecycle: 'linear-gradient(90deg, #84CC16 0%, #3B82F6 50%, #F97316 100%)',
    electric: 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)',
    warning: 'linear-gradient(135deg, #F59E0B 0%, #F97316 100%)',
    success: 'linear-gradient(135deg, #84CC16 0%, #06B6D4 100%)',
  }
} as const;

export const typography = {
  // Font families
  sans: 'Inter, -apple-system, BlinkMacSystemFont, system-ui, sans-serif',
  display: 'Space Grotesk, Inter, sans-serif',
  mono: 'JetBrains Mono, Consolas, Monaco, monospace',
  
  // Font sizes (using Tailwind scale)
  size: {
    xs: '0.75rem',      // 12px
    sm: '0.875rem',     // 14px
    base: '1rem',       // 16px
    lg: '1.125rem',     // 18px
    xl: '1.25rem',      // 20px
    '2xl': '1.5rem',    // 24px
    '3xl': '1.875rem',  // 30px
    '4xl': '2.25rem',   // 36px
    '5xl': '3rem',      // 48px
    '6xl': '3.75rem',   // 60px
    '7xl': '4.5rem',    // 72px
  },
  
  // Line heights
  leading: {
    tight: '1.25',
    normal: '1.5',
    relaxed: '1.75',
  },
  
  // Letter spacing
  tracking: {
    tight: '-0.025em',
    normal: '0',
    wide: '0.025em',
    wider: '0.05em',
    widest: '0.1em',
  }
} as const;

export const spacing = {
  section: {
    sm: '4rem',   // 64px
    md: '6rem',   // 96px
    lg: '8rem',   // 128px
    xl: '12rem',  // 192px
  },
  container: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  }
} as const;

export const borderRadius = {
  sm: '0.375rem',  // 6px
  md: '0.5rem',    // 8px
  lg: '0.75rem',   // 12px
  xl: '1rem',      // 16px
  '2xl': '1.5rem', // 24px
  full: '9999px',
} as const;

export const shadows = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
  glow: {
    electric: '0 0 20px rgba(59, 130, 246, 0.3)',
    acid: '0 0 20px rgba(132, 204, 22, 0.3)',
    coral: '0 0 20px rgba(249, 115, 22, 0.3)',
  }
} as const;

export const transitions = {
  fast: '150ms cubic-bezier(0.4, 0, 0.2, 1)',
  base: '200ms cubic-bezier(0.4, 0, 0.2, 1)',
  slow: '300ms cubic-bezier(0.4, 0, 0.2, 1)',
  smooth: '400ms cubic-bezier(0.22, 1, 0.36, 1)',
} as const;
