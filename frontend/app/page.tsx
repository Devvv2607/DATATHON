'use client';

import Link from "next/link";
import { TrendingUp, Brain, Zap, Target, ArrowRight, BarChart3, Sparkles } from "lucide-react";
import Shuffle from "./dashboard/3dText";
import DarkVeil from "@/components/DarkVeil";

export default function Home() {
  return (
    <div className="min-h-screen bg-black relative">
      {/* DarkVeil Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <DarkVeil
          hueShift={0}
          noiseIntensity={0.15}
          scanlineIntensity={0.05}
          speed={0.3}
          scanlineFrequency={0.5}
          warpAmount={0.2}
        />
      </div>

      {/* Additional gradient overlays for depth */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-0 -left-1/4 w-1/2 h-1/2 bg-blue-600/20 rounded-full blur-[150px]" />
        <div className="absolute bottom-0 -right-1/4 w-1/2 h-1/2 bg-cyan-600/20 rounded-full blur-[150px]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-1/3 h-1/3 bg-blue-700/15 rounded-full blur-[120px]" />
      </div>

      {/* Hero Section */}
      <div className="relative overflow-hidden z-10">
        
        <div className="relative max-w-7xl mx-auto px-6 py-24 sm:py-32">
          {/* Navigation */}
          <nav className="flex items-center justify-between mb-16">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-2xl glass-strong">
                <TrendingUp className="w-6 h-6 text-blue-400" />
              </div>
              <span className="text-2xl font-bold gradient-text">TrendPulse</span>
            </div>
            <div className="flex items-center gap-4">
              <Link
                href="/search"
                className="px-6 py-2.5 rounded-full glass hover:scale-105 transition-all duration-300"
              >
                Search Trends
              </Link>
              <Link
                href="/signup"
                className="px-6 py-2.5 rounded-full glass-strong hover:scale-105 transition-all duration-300"
              >
                Get Started
              </Link>
            </div>
          </nav>

          {/* Hero Content */}
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full glass-strong mb-8">
              <Sparkles className="w-4 h-4 text-blue-400" />
              <span className="text-sm text-blue-300 font-medium">AI-Powered Trend Intelligence</span>
            </div>
            
<Shuffle
  text="Predict Trend Decline "
  className="text-5xl sm:text-7xl font-bold normal-case "
  shuffleDirection="right"
  duration={0.40}
  animationMode="evenodd"
  shuffleTimes={1}
  ease="power3.out"
  stagger={0.03}
  threshold={0.1}
  triggerOnce={true}
  triggerOnHover
  respectReducedMotion={true}
  loop={false}
  loopDelay={0}
/>
            <h1 className="text-5xl sm:text-7xl font-bold mb-6 leading-tight">
              
              <span className="gradient-text">Before It Happens</span>
            </h1>

            {/* Spline 3D Widget */}
            <div className="w-full h-[500px] my-12 rounded-3xl overflow-hidden relative border border-slate-800/50 bg-transparent ">
              <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/30 pointer-events-none z-10" />
              <iframe 
                src="https://my.spline.design/widgetlytic-8MS7r1cHtOKxFl2NG9EH5xFR-5MO/"
                frameBorder="0"
                width="100%"
                height="100%"
                className="w-full h-full mix-blend-lighten opacity-90 pointer-events-none"
                style={{ background: 'transparent' }}
              />
            </div>
            
            <p className="text-xl text-slate-300 mb-12 max-w-2xl mx-auto leading-relaxed">
              Leverage machine learning to identify dying trends, understand why they're fading, 
              and simulate interventions—all in real-time.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
              <Link
                href="/search"
                className="group px-8 py-4 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 hover:shadow-[0_0_40px_rgba(96,165,250,0.4)] hover:scale-105 transition-all duration-300 flex items-center gap-2 text-lg font-semibold"
              >
                Search Trends
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/signup"
                className="px-8 py-4 rounded-full glass-strong hover:scale-105 transition-all duration-300 text-lg"
              >
                Get Started
              </Link>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto">
              <div>
                <div className="text-4xl font-bold text-blue-400 mb-2">85%</div>
                <div className="text-sm text-slate-400">Prediction Accuracy</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-purple-400 mb-2">30 days</div>
                <div className="text-sm text-slate-400">Early Warning</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-pink-400 mb-2">10M+</div>
                <div className="text-sm text-slate-400">Trends Analyzed</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-6 py-24 relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Why Choose TrendPulse?</h2>
          <p className="text-slate-400 text-lg">Transform raw social data into actionable insights</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Feature 1 */}
          <div className="p-6 rounded-3xl glass-card group cursor-pointer">
            <div className="w-12 h-12 rounded-2xl bg-blue-500/10 flex items-center justify-center mb-4 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300">
              <Brain className="w-6 h-6 text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold mb-2">AI Predictions</h3>
            <p className="text-slate-400 text-sm">
              XGBoost-powered models predict decline probability with 85% accuracy
            </p>
          </div>

          {/* Feature 2 */}
          <div className="p-6 rounded-3xl glass-card group cursor-pointer">
            <div className="w-12 h-12 rounded-2xl bg-purple-500/10 flex items-center justify-center mb-4 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300">
              <Sparkles className="w-6 h-6 text-purple-400" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Explainable AI</h3>
            <p className="text-slate-400 text-sm">
              SHAP values reveal exactly why a trend is declining
            </p>
          </div>

          {/* Feature 3 */}
          <div className="p-6 rounded-3xl glass-card group cursor-pointer">
            <div className="w-12 h-12 rounded-2xl bg-pink-500/10 flex items-center justify-center mb-4 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300">
              <Zap className="w-6 h-6 text-pink-400" />
            </div>
            <h3 className="text-xl font-semibold mb-2">What-If Simulator</h3>
            <p className="text-slate-400 text-sm">
              Test intervention strategies before spending a dollar
            </p>
          </div>

          {/* Feature 4 */}
          <div className="p-6 rounded-3xl glass-card group cursor-pointer">
            <div className="w-12 h-12 rounded-2xl bg-green-500/10 flex items-center justify-center mb-4 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300">
              <Target className="w-6 h-6 text-green-400" />
            </div>
            <h3 className="text-xl font-semibold mb-2">ROI Optimizer</h3>
            <p className="text-slate-400 text-sm">
              Calculate expected returns for every intervention dollar
            </p>
          </div>
        </div>
      </div>

      {/* Problem Statement */}
      <div className="max-w-7xl mx-auto px-6 py-24 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-red-500/10 border border-red-500/20 mb-6">
              <span className="text-red-400 font-semibold">The Problem</span>
            </div>
            <h2 className="text-4xl font-bold mb-6">67% of Trends Die Within 30 Days</h2>
            <p className="text-slate-300 text-lg mb-6 leading-relaxed">
              Brands invest millions in trend-jacking campaigns, only to watch engagement 
              plummet as trends naturally decay. By the time you realize it's dying, 
              it's already too late.
            </p>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-red-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                  <div className="w-2 h-2 rounded-full bg-red-500" />
                </div>
                <div>
                  <div className="font-semibold mb-1">Reactive, Not Proactive</div>
                  <div className="text-sm text-slate-400">Most tools show you what happened, not what's coming</div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-red-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                  <div className="w-2 h-2 rounded-full bg-red-500" />
                </div>
                <div>
                  <div className="font-semibold mb-1">No Actionable Insights</div>
                  <div className="text-sm text-slate-400">Data dashboards don't tell you how to save a dying trend</div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-red-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                  <div className="w-2 h-2 rounded-full bg-red-500" />
                </div>
                <div>
                  <div className="font-semibold mb-1">Wasted Budget</div>
                  <div className="text-sm text-slate-400">Campaigns continue spending on dead trends</div>
                </div>
              </div>
            </div>
          </div>

          <div>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-500/10 border border-green-500/20 mb-6">
              <span className="text-green-400 font-semibold">The Solution</span>
            </div>
            <h2 className="text-4xl font-bold mb-6">Predict, Explain, Intervene</h2>
            <p className="text-slate-300 text-lg mb-6 leading-relaxed">
              TrendPulse gives you 30-day advance warning with explainable AI, 
              so you can pivot before your competitors even notice the decline.
            </p>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-green-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                  <div className="w-2 h-2 rounded-full bg-green-500" />
                </div>
                <div>
                  <div className="font-semibold mb-1">Predictive Analytics</div>
                  <div className="text-sm text-slate-400">See decline probability before engagement drops</div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-green-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                  <div className="w-2 h-2 rounded-full bg-green-500" />
                </div>
                <div>
                  <div className="font-semibold mb-1">SHAP Explanations</div>
                  <div className="text-sm text-slate-400">Understand exactly why trends are fading</div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-green-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                  <div className="w-2 h-2 rounded-full bg-green-500" />
                </div>
                <div>
                  <div className="font-semibold mb-1">Simulation Engine</div>
                  <div className="text-sm text-slate-400">Test rescue strategies with predicted ROI</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-4xl mx-auto px-6 py-24 relative z-10">
        <div className="relative overflow-hidden rounded-xl border border-[#374151] bg-[#151922] p-12 text-center">
          {/* Subtle gradient overlay to match chart style */}
          <div className="absolute inset-0 bg-gradient-to-br from-[#3B82F6]/5 via-transparent to-[#8B5CF6]/5 pointer-events-none" />
          
          <div className="relative z-10">
            <BarChart3 className="w-16 h-16 mx-auto mb-6 text-[#3B82F6]" />
            <h2 className="text-4xl font-bold mb-4 text-[#F9FAFB]">Ready to Stay Ahead?</h2>
            <p className="text-xl text-[#D1D5DB] mb-8 max-w-2xl mx-auto">
              Join the brands that predict trend decline before their competitors even see it coming
            </p>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-lg bg-[#3B82F6] hover:bg-[#2563EB] transition-colors text-lg font-semibold group text-white"
            >
              Start Analyzing Trends
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="relative border-t border-white/5 py-12 z-10">
        <div className="max-w-7xl mx-auto px-6 text-center text-slate-400">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-1.5 rounded-xl glass-strong">
              <TrendingUp className="w-4 h-4 text-blue-400" />
            </div>
            <span className="font-semibold gradient-text">TrendPulse</span>
          </div>
          <p className="text-sm">
            AI-Powered Social Media Trend Intelligence Platform
          </p>
          <p className="text-xs mt-2 text-slate-500">
            Built for Datathon 2026
          </p>
        </div>
      </footer>
    </div>
  );
}
