'use client';

import React, { useState, useEffect, useRef, Suspense } from 'react';
import { motion, useScroll, useTransform, useSpring, useInView, AnimatePresence } from 'framer-motion';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, MeshDistortMaterial, Sphere, Float } from '@react-three/drei';
import * as THREE from 'three';
import { 
  TrendingUp, TrendingDown, Zap, Brain, Shield, Eye, Users, 
  BarChart3, Activity, AlertTriangle, ChevronRight, Moon, Sun,
  LineChart, PieChart, Network, Sparkles, ArrowRight
} from 'lucide-react';
import Link from 'next/link';

// ============================================
// THEME CONTEXT
// ============================================

const ThemeContext = React.createContext<{
  isDark: boolean;
  toggleTheme: () => void;
}>({
  isDark: true,
  toggleTheme: () => {},
});

const useTheme = () => React.useContext(ThemeContext);

// ============================================
// 3D COMPONENTS
// ============================================

// Animated 3D Trend Wave
function TrendWave() {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  useFrame(({ clock }) => {
    if (meshRef.current) {
      meshRef.current.rotation.x = Math.sin(clock.getElapsedTime() * 0.3) * 0.1;
      meshRef.current.rotation.y += 0.002;
      meshRef.current.position.y = Math.sin(clock.getElapsedTime() * 0.5) * 0.1;
    }
  });

  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
      <Sphere
        ref={meshRef}
        args={[1, 100, 100]}
        scale={hovered ? 1.1 : 1}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <MeshDistortMaterial
          color="#00FF88"
          attach="material"
          distort={0.4}
          speed={2}
          roughness={0.2}
          metalness={0.8}
        />
      </Sphere>
    </Float>
  );
}

// Particle System for Data Points
function DataParticles() {
  const particlesRef = useRef<THREE.Points>(null);
  const count = 1000;

  const positions = React.useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 10;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 10;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 10;
    }
    return pos;
  }, []);

  useFrame(({ clock }) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y = clock.getElapsedTime() * 0.05;
    }
  });

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.02}
        color="#00D9FF"
        transparent
        opacity={0.6}
        sizeAttenuation
      />
    </points>
  );
}

// ============================================
// ANIMATED COUNTER
// ============================================

function AnimatedCounter({ end, duration = 2, suffix = '' }: { end: number; duration?: number; suffix?: string }) {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true });

  useEffect(() => {
    if (!inView) return;

    let startTime: number;
    let animationFrame: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / (duration * 1000), 1);
      
      setCount(Math.floor(progress * end));

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, [end, duration, inView]);

  return <span ref={ref}>{count.toLocaleString()}{suffix}</span>;
}

// ============================================
// HERO SECTION
// ============================================

function HeroSection() {
  const { isDark } = useTheme();
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setMousePosition({
      x: (e.clientX - rect.left - rect.width / 2) / 20,
      y: (e.clientY - rect.top - rect.height / 2) / 20,
    });
  };

  return (
    <div 
      className="relative min-h-screen flex items-center justify-center overflow-hidden"
      onMouseMove={handleMouseMove}
    >
      {/* Animated Background Grid */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute inset-0 bg-gradient-to-br from-[#00FF88]/20 via-transparent to-[#FF0080]/20" />
        <svg className="w-full h-full">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path
                d="M 40 0 L 0 0 0 40"
                fill="none"
                stroke={isDark ? '#00FF88' : '#0A0E27'}
                strokeWidth="0.5"
                opacity="0.3"
              />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      {/* 3D Background */}
      <div className="absolute inset-0 opacity-30">
        <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          <Suspense fallback={null}>
            <TrendWave />
            <DataParticles />
          </Suspense>
        </Canvas>
      </div>

      {/* Hero Content */}
      <div className="relative z-10 container mx-auto px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          style={{
            transform: `translate(${mousePosition.x}px, ${mousePosition.y}px)`,
          }}
        >
          {/* Pulse Badge */}
          <motion.div
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full border mb-8"
            style={{
              borderColor: isDark ? '#00FF88' : '#0A0E27',
              backgroundColor: isDark ? 'rgba(0, 255, 136, 0.1)' : 'rgba(10, 14, 39, 0.05)',
            }}
            animate={{
              boxShadow: [
                '0 0 0 0 rgba(0, 255, 136, 0)',
                '0 0 0 10px rgba(0, 255, 136, 0)',
              ],
            }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <Activity className="w-4 h-4 text-[#00FF88]" />
            <span className={isDark ? 'text-gray-300' : 'text-gray-700'}>
              AI-Powered Trend Intelligence
            </span>
          </motion.div>

          {/* Main Headline */}
          <h1 className="text-6xl md:text-8xl font-black mb-6 leading-tight">
            <span
              className="inline-block"
              style={{
                background: isDark
                  ? 'linear-gradient(135deg, #00FF88 0%, #00D9FF 50%, #FF0080 100%)'
                  : 'linear-gradient(135deg, #0A0E27 0%, #00FF88 50%, #FF0080 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }}
            >
              Predict Trend
            </span>
            <br />
            <span className={isDark ? 'text-white' : 'text-gray-900'}>
              Decline Before
            </span>
            <br />
            <span className="text-[#FF0080]">It Happens</span>
          </h1>

          {/* Subtitle */}
          <motion.p
            className={`text-xl md:text-2xl mb-12 max-w-3xl mx-auto ${
              isDark ? 'text-gray-400' : 'text-gray-600'
            }`}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
          >
            Explainable AI that analyzes social media trends in real-time,
            detects early warning signals, and predicts when trends will fade—with
            full transparency into <span className="text-[#00FF88] font-semibold">WHY</span>.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.8 }}
          >
            <Link href="/signup">
              <motion.button
                className="px-8 py-4 rounded-xl font-bold text-lg flex items-center gap-2 group relative overflow-hidden"
                style={{
                  backgroundColor: '#00FF88',
                  color: '#0A0E27',
                }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <span className="relative z-10">Start Analyzing Trends</span>
                <ArrowRight className="w-5 h-5 relative z-10 group-hover:translate-x-1 transition-transform" />
                <motion.div
                  className="absolute inset-0 bg-[#00D9FF]"
                  initial={{ x: '-100%' }}
                  whileHover={{ x: 0 }}
                  transition={{ duration: 0.3 }}
                />
              </motion.button>
            </Link>

            <Link href="/dashboard">
              <motion.button
                className={`px-8 py-4 rounded-xl font-bold text-lg flex items-center gap-2 border-2 ${
                  isDark
                    ? 'border-gray-700 text-gray-300 hover:border-[#00FF88]'
                    : 'border-gray-300 text-gray-700 hover:border-[#00FF88]'
                }`}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                View Live Demo
                <Sparkles className="w-5 h-5" />
              </motion.button>
            </Link>
          </motion.div>

          {/* Stats */}
          <motion.div
            className="grid grid-cols-3 gap-8 mt-20 max-w-3xl mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8, duration: 0.8 }}
          >
            {[
              { label: 'Trends Analyzed', value: 50000, suffix: '+' },
              { label: 'Accuracy Rate', value: 94, suffix: '%' },
              { label: 'Data Points', value: 2, suffix: 'M+' },
            ].map((stat, i) => (
              <motion.div
                key={i}
                className={`p-6 rounded-2xl border ${
                  isDark ? 'bg-gray-900/50 border-gray-800' : 'bg-white/80 border-gray-200'
                }`}
                whileHover={{ y: -5 }}
              >
                <div
                  className="text-4xl font-black mb-2"
                  style={{
                    background: 'linear-gradient(135deg, #00FF88, #00D9FF)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                  }}
                >
                  <AnimatedCounter end={stat.value} suffix={stat.suffix} />
                </div>
                <div className={isDark ? 'text-gray-400' : 'text-gray-600'}>
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>
      </div>

      {/* Scroll Indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        animate={{ y: [0, 10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <div className="w-6 h-10 rounded-full border-2 border-[#00FF88] flex justify-center p-2">
          <motion.div
            className="w-1.5 h-1.5 bg-[#00FF88] rounded-full"
            animate={{ y: [0, 12, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </div>
      </motion.div>
    </div>
  );
}

// ============================================
// TREND LIFECYCLE VISUALIZATION
// ============================================

function TrendLifecycleSection() {
  const { isDark } = useTheme();
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });

  const stages = [
    { name: 'Emerging', icon: Sparkles, color: '#00FF88', description: 'Trend starts gaining traction' },
    { name: 'Growing', icon: TrendingUp, color: '#00D9FF', description: 'Rapid adoption and engagement' },
    { name: 'Peak', icon: Zap, color: '#FFD700', description: 'Maximum saturation reached' },
    { name: 'Declining', icon: TrendingDown, color: '#FF6B6B', description: 'Engagement drops off' },
    { name: 'Dormant', icon: AlertTriangle, color: '#FF0080', description: 'Trend fades away' },
  ];

  return (
    <div
      ref={ref}
      className={`py-32 relative overflow-hidden ${isDark ? 'bg-[#0A0E27]' : 'bg-gray-50'}`}
    >
      {/* Section Header */}
      <div className="container mx-auto px-6 mb-20">
        <motion.div
          className="text-center"
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          <h2
            className="text-5xl md:text-6xl font-black mb-6"
            style={{
              background: isDark
                ? 'linear-gradient(135deg, #00FF88 0%, #00D9FF 100%)'
                : 'linear-gradient(135deg, #0A0E27 0%, #00FF88 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Trend Lifecycle Intelligence
          </h2>
          <p className={`text-xl ${isDark ? 'text-gray-400' : 'text-gray-600'} max-w-2xl mx-auto`}>
            We track every stage of a trend's journey—from emergence to decline
          </p>
        </motion.div>
      </div>

      {/* Lifecycle Stages */}
      <div className="container mx-auto px-6">
        <div className="relative">
          {/* Connection Line */}
          <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-[#00FF88] via-[#00D9FF] to-[#FF0080] hidden md:block" />

          <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
            {stages.map((stage, i) => (
              <motion.div
                key={i}
                className="relative"
                initial={{ opacity: 0, y: 50 }}
                animate={isInView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.6, delay: i * 0.1 }}
              >
                <motion.div
                  className={`p-6 rounded-2xl border-2 ${
                    isDark ? 'bg-gray-900/80 backdrop-blur' : 'bg-white'
                  }`}
                  style={{
                    borderColor: stage.color,
                  }}
                  whileHover={{ scale: 1.05, y: -10 }}
                  transition={{ type: 'spring', stiffness: 300 }}
                >
                  {/* Icon */}
                  <div
                    className="w-16 h-16 rounded-full flex items-center justify-center mb-4 mx-auto"
                    style={{
                      backgroundColor: `${stage.color}20`,
                      border: `2px solid ${stage.color}`,
                    }}
                  >
                    <stage.icon className="w-8 h-8" style={{ color: stage.color }} />
                  </div>

                  {/* Content */}
                  <h3 className={`text-xl font-bold mb-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                    {stage.name}
                  </h3>
                  <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                    {stage.description}
                  </p>

                  {/* Stage Number */}
                  <div
                    className="absolute -top-4 -right-4 w-10 h-10 rounded-full flex items-center justify-center font-bold"
                    style={{
                      backgroundColor: stage.color,
                      color: '#0A0E27',
                    }}
                  >
                    {i + 1}
                  </div>
                </motion.div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ============================================
// FEATURES SECTION
// ============================================

function FeaturesSection() {
  const { isDark } = useTheme();
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true });

  const features = [
    {
      icon: Eye,
      title: 'Early Warning Signals',
      description: 'Detect engagement drops, audience fatigue, and influencer disengagement before trends collapse.',
      color: '#00FF88',
      metrics: ['Engagement Drop: 23%', 'Creator Activity: -15%', 'Alert Level: Medium'],
    },
    {
      icon: Brain,
      title: 'Explainable AI',
      description: 'Every prediction comes with full transparency. See exactly WHY our AI thinks a trend will decline.',
      color: '#00D9FF',
      metrics: ['Feature Attribution', 'Causal Analysis', 'Confidence: 94%'],
    },
    {
      icon: Activity,
      title: 'Real-Time Analytics',
      description: 'Monitor social media trends across platforms with live data updates and instant insights.',
      color: '#FFD700',
      metrics: ['Live Monitoring', '5-Min Updates', '12 Platforms'],
    },
    {
      icon: Network,
      title: 'Influencer Tracking',
      description: 'Track creator participation, engagement patterns, and network effects driving trend momentum.',
      color: '#FF6B6B',
      metrics: ['Network Graph', 'Sentiment Analysis', '10K+ Influencers'],
    },
    {
      icon: Shield,
      title: 'Decline Prediction',
      description: 'ML models trained on historical trend data to predict when trends will start declining.',
      color: '#FF0080',
      metrics: ['Accuracy: 94%', 'Lead Time: 7-14 days', 'Risk Score'],
    },
    {
      icon: LineChart,
      title: 'ROI Optimization',
      description: 'Make data-driven decisions on when to invest in or exit from trending content strategies.',
      color: '#9D4EDD',
      metrics: ['ROI Calculator', 'Break-even Analysis', 'Risk Assessment'],
    },
  ];

  return (
    <div
      ref={ref}
      className={`py-32 relative ${isDark ? 'bg-gradient-to-b from-[#0A0E27] to-black' : 'bg-white'}`}
    >
      <div className="container mx-auto px-6">
        {/* Section Header */}
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0 }}
          animate={isInView ? { opacity: 1 } : {}}
        >
          <h2
            className="text-5xl md:text-6xl font-black mb-6"
            style={{
              background: 'linear-gradient(135deg, #00FF88, #FF0080)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Powerful Features
          </h2>
          <p className={`text-xl ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Everything you need to stay ahead of the trend curve
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 50 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: i * 0.1 }}
            >
              <motion.div
                className={`p-8 rounded-3xl border-2 h-full ${
                  isDark ? 'bg-gray-900/50 backdrop-blur' : 'bg-gray-50'
                }`}
                style={{
                  borderColor: `${feature.color}40`,
                }}
                whileHover={{
                  y: -10,
                  borderColor: feature.color,
                  boxShadow: `0 20px 40px ${feature.color}20`,
                }}
                transition={{ type: 'spring', stiffness: 300 }}
              >
                {/* Icon */}
                <div
                  className="w-16 h-16 rounded-2xl flex items-center justify-center mb-6"
                  style={{
                    backgroundColor: `${feature.color}20`,
                  }}
                >
                  <feature.icon className="w-8 h-8" style={{ color: feature.color }} />
                </div>

                {/* Title */}
                <h3 className={`text-2xl font-bold mb-4 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  {feature.title}
                </h3>

                {/* Description */}
                <p className={`mb-6 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                  {feature.description}
                </p>

                {/* Metrics */}
                <div className="space-y-2">
                  {feature.metrics.map((metric, idx) => (
                    <div
                      key={idx}
                      className={`px-3 py-2 rounded-lg text-sm font-mono ${
                        isDark ? 'bg-black/50' : 'bg-white'
                      }`}
                      style={{
                        border: `1px solid ${feature.color}40`,
                        color: feature.color,
                      }}
                    >
                      {metric}
                    </div>
                  ))}
                </div>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ============================================
// THEME TOGGLE
// ============================================

function ThemeToggle() {
  const { isDark, toggleTheme } = useTheme();

  return (
    <motion.button
      className="fixed top-6 right-6 z-50 p-4 rounded-full border-2"
      style={{
        backgroundColor: isDark ? '#0A0E27' : '#FFFFFF',
        borderColor: isDark ? '#00FF88' : '#0A0E27',
      }}
      onClick={toggleTheme}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
    >
      <AnimatePresence mode="wait">
        {isDark ? (
          <motion.div
            key="sun"
            initial={{ rotate: -90, opacity: 0 }}
            animate={{ rotate: 0, opacity: 1 }}
            exit={{ rotate: 90, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <Sun className="w-6 h-6 text-[#00FF88]" />
          </motion.div>
        ) : (
          <motion.div
            key="moon"
            initial={{ rotate: 90, opacity: 0 }}
            animate={{ rotate: 0, opacity: 1 }}
            exit={{ rotate: -90, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <Moon className="w-6 h-6 text-[#0A0E27]" />
          </motion.div>
        )}
      </AnimatePresence>
    </motion.button>
  );
}

// ============================================
// MAIN COMPONENT
// ============================================

export default function NewLandingPage() {
  const [isDark, setIsDark] = useState(true);

  const toggleTheme = () => setIsDark(!isDark);

  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      <div
        className={`min-h-screen transition-colors duration-500 ${
          isDark ? 'bg-black text-white' : 'bg-white text-gray-900'
        }`}
      >
        <ThemeToggle />
        <HeroSection />
        <TrendLifecycleSection />
        <FeaturesSection />
        
        {/* CTA Section */}
        <div className={`py-32 ${isDark ? 'bg-black' : 'bg-gray-50'}`}>
          <div className="container mx-auto px-6 text-center">
            <motion.h2
              className="text-5xl md:text-6xl font-black mb-8"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              style={{
                background: 'linear-gradient(135deg, #00FF88, #FF0080)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              Ready to Predict the Future?
            </motion.h2>
            <motion.p
              className={`text-xl mb-12 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
            >
              Join thousands of marketers and creators using TrendPulse
            </motion.p>
            <Link href="/signup">
              <motion.button
                className="px-12 py-5 rounded-xl font-bold text-xl"
                style={{
                  backgroundColor: '#00FF88',
                  color: '#0A0E27',
                }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Get Started Free
              </motion.button>
            </Link>
          </div>
        </div>
      </div>
    </ThemeContext.Provider>
  );
}
