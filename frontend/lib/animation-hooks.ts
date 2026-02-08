/**
 * TrendPulse Animation Hooks
 * Reusable animation logic for cinematic effects
 */

import { useEffect, useRef, useState } from 'react';
import { useSpring, useTransform, useInView, useMotionValue, MotionValue } from 'framer-motion';

// ============================================
// CINEMATIC COUNTER HOOK
// ============================================

/**
 * Animated number counter with spring physics (like Stripe)
 * 
 * @param target - The final number to count to
 * @param duration - How long the animation takes (ms)
 * @param delay - Delay before starting (ms)
 * @returns MotionValue that animates from 0 to target
 */
export function useCinematicCounter(
  target: number,
  duration: number = 2000,
  delay: number = 300
): MotionValue<number> {
  const spring = useSpring(0, {
    stiffness: 60,
    damping: 25,
  });

  useEffect(() => {
    const timer = setTimeout(() => {
      spring.set(target);
    }, delay);

    return () => clearTimeout(timer);
  }, [target, delay, spring]);

  return useTransform(spring, (value) => Math.floor(value));
}

/**
 * Format animated number with commas and custom formatting
 */
export function useFormattedCounter(
  target: number,
  options: {
    duration?: number;
    delay?: number;
    prefix?: string;
    suffix?: string;
    decimals?: number;
  } = {}
): string {
  const {
    duration = 2000,
    delay = 300,
    prefix = '',
    suffix = '',
    decimals = 0,
  } = options;

  const counter = useCinematicCounter(target, duration, delay);
  const [display, setDisplay] = useState(prefix + '0' + suffix);

  useEffect(() => {
    const unsubscribe = counter.on('change', (latest) => {
      const formatted = decimals > 0
        ? latest.toFixed(decimals)
        : Math.floor(latest).toLocaleString();
      setDisplay(prefix + formatted + suffix);
    });

    return () => unsubscribe();
  }, [counter, prefix, suffix, decimals]);

  return display;
}

// ============================================
// SCROLL REVEAL HOOK
// ============================================

/**
 * Trigger animation when element enters viewport
 * 
 * @param options - IntersectionObserver options
 * @returns ref and inView boolean
 */
export function useScrollReveal(options: {
  threshold?: number;
  triggerOnce?: boolean;
} = {}) {
  const { threshold = 0.2, triggerOnce = true } = options;
  const ref = useRef(null);
  const isInView = useInView(ref, {
    once: triggerOnce,
    amount: threshold,
  });

  return { ref, isInView };
}

// ============================================
// MOUSE POSITION HOOK
// ============================================

/**
 * Track mouse position relative to element
 * Useful for parallax effects
 */
export function useMousePosition(elementRef: React.RefObject<HTMLElement>) {
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = element.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;

      // Normalize to -1 to 1
      const normalizedX = (e.clientX - centerX) / (rect.width / 2);
      const normalizedY = (e.clientY - centerY) / (rect.height / 2);

      x.set(normalizedX);
      y.set(normalizedY);
    };

    element.addEventListener('mousemove', handleMouseMove);

    return () => {
      element.removeEventListener('mousemove', handleMouseMove);
    };
  }, [elementRef, x, y]);

  return { x, y };
}

/**
 * Create parallax effect from mouse position
 */
export function useParallax(
  elementRef: React.RefObject<HTMLElement>,
  strength: number = 20
) {
  const { x, y } = useMousePosition(elementRef);

  const translateX = useTransform(x, [-1, 1], [-strength, strength]);
  const translateY = useTransform(y, [-1, 1], [-strength, strength]);

  return { translateX, translateY };
}

// ============================================
// TILT EFFECT HOOK
// ============================================

/**
 * 3D tilt effect on hover (like Apple product cards)
 */
export function useTiltEffect(elementRef: React.RefObject<HTMLElement>, maxTilt: number = 10) {
  const rotateX = useMotionValue(0);
  const rotateY = useMotionValue(0);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = element.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;

      const angleX = ((e.clientY - centerY) / rect.height) * maxTilt;
      const angleY = ((e.clientX - centerX) / rect.width) * -maxTilt;

      rotateX.set(angleX);
      rotateY.set(angleY);
    };

    const handleMouseLeave = () => {
      rotateX.set(0);
      rotateY.set(0);
    };

    element.addEventListener('mousemove', handleMouseMove);
    element.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      element.removeEventListener('mousemove', handleMouseMove);
      element.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, [elementRef, maxTilt, rotateX, rotateY]);

  return { rotateX, rotateY };
}

// ============================================
// PERCENTAGE ANIMATION HOOK
// ============================================

/**
 * Animate a percentage value (0-100)
 */
export function usePercentageAnimation(
  target: number,
  duration: number = 1500
): number {
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const start = performance.now();
    const animate = (time: number) => {
      const elapsed = time - start;
      const progress = Math.min(elapsed / duration, 1);

      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      setCurrent(eased * target);

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
  }, [target, duration]);

  return current;
}

// ============================================
// STAGGER DELAY CALCULATOR
// ============================================

/**
 * Calculate delay for stagger animation based on index
 */
export function useStaggerDelay(index: number, delayPerItem: number = 0.08): number {
  return index * delayPerItem;
}

// ============================================
// REDUCED MOTION CHECK
// ============================================

/**
 * Check if user prefers reduced motion
 */
export function useReducedMotion(): boolean {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handleChange = (e: MediaQueryListEvent) => {
      setPrefersReducedMotion(e.matches);
    };

    mediaQuery.addEventListener('change', handleChange);

    return () => {
      mediaQuery.removeEventListener('change', handleChange);
    };
  }, []);

  return prefersReducedMotion;
}

// ============================================
// PROGRESS ANIMATION HOOK
// ============================================

/**
 * Animate a progress bar or circular progress
 */
export function useProgress(
  target: number,
  duration: number = 1000
): number {
  const spring = useSpring(0, {
    stiffness: 80,
    damping: 20,
  });

  const [progress, setProgress] = useState(0);

  useEffect(() => {
    spring.set(target);

    const unsubscribe = spring.on('change', (latest) => {
      setProgress(Math.min(Math.max(latest, 0), 100));
    });

    return () => unsubscribe();
  }, [target, spring]);

  return progress;
}

// ============================================
// TYPEWRITER EFFECT HOOK
// ============================================

/**
 * Typewriter text animation
 */
export function useTypewriter(
  text: string,
  speed: number = 50,
  delay: number = 0
): string {
  const [displayText, setDisplayText] = useState('');

  useEffect(() => {
    const startTimer = setTimeout(() => {
      let index = 0;
      const timer = setInterval(() => {
        if (index < text.length) {
          setDisplayText(text.slice(0, index + 1));
          index++;
        } else {
          clearInterval(timer);
        }
      }, speed);

      return () => clearInterval(timer);
    }, delay);

    return () => clearTimeout(startTimer);
  }, [text, speed, delay]);

  return displayText;
}

// ============================================
// WAVE ANIMATION HOOK
// ============================================

/**
 * Generate wave animation values for loading states
 */
export function useWaveAnimation(count: number = 3) {
  const [dots, setDots] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setDots((prev) => (prev + 1) % (count + 1));
    }, 500);

    return () => clearInterval(timer);
  }, [count]);

  return '.'.repeat(dots);
}

// ============================================
// COLOR INTERPOLATION HOOK
// ============================================

/**
 * Smoothly interpolate between two colors
 */
export function useColorTransition(
  fromColor: string,
  toColor: string,
  progress: number
): string {
  // Simple RGB interpolation (enhance with chroma.js for production)
  const from = hexToRgb(fromColor);
  const to = hexToRgb(toColor);

  if (!from || !to) return fromColor;

  const r = Math.round(from.r + (to.r - from.r) * progress);
  const g = Math.round(from.g + (to.g - from.g) * progress);
  const b = Math.round(from.b + (to.b - from.b) * progress);

  return `rgb(${r}, ${g}, ${b})`;
}

function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
}

// ============================================
// LOADING STATE HOOK
// ============================================

/**
 * Manage loading states with minimum display time
 * Prevents flash of loading spinner
 */
export function useMinimumLoadingTime(
  isLoading: boolean,
  minimumTime: number = 500
): boolean {
  const [showLoading, setShowLoading] = useState(false);
  const timerRef = useRef<NodeJS.Timeout | undefined>(undefined);

  useEffect(() => {
    if (isLoading) {
      setShowLoading(true);
    } else {
      timerRef.current = setTimeout(() => {
        setShowLoading(false);
      }, minimumTime);
    }

    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, [isLoading, minimumTime]);

  return showLoading;
}
