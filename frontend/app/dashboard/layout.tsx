'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { useAuth } from '@/contexts/AuthContext';
import { DomainProvider } from '@/contexts/DomainContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import {
  TrendingUp,
  BarChart3,
  Brain,
  Sliders,
  Network,
  Lightbulb,
  Activity,
  Shield,
  Sparkles,
  MessageCircle,
  Share2,
  LogOut,
  DollarSign,
  FileText,
  Calendar,
  GitBranch,
  Database,
  Zap
} from 'lucide-react';

const generalNavigation = [
  { name: 'Overview', href: '/dashboard', icon: Activity },
  { name: 'Trend Lifecycle', href: '/dashboard/trendLifecycle', icon: TrendingUp },
  { name: 'Decline Signals', href: '/dashboard/declineSignals', icon: Shield },
  { name: 'Comeback AI', href: '/dashboard/comeback', icon: Sparkles },
  { name: 'Chat Assistant', href: '/dashboard/chat', icon: MessageCircle },
  { name: 'Social Graph', href: '/dashboard/social-graph', icon: Share2 },
//   { name: 'Explainability', href: '/dashboard/explainability', icon: Brain },
//   { name: 'What-If Simulator', href: '/dashboard/simulator', icon: Sliders },
//   { name: 'Network Analysis', href: '/dashboard/network', icon: Network },
//   { name: 'Strategy & ROI', href: '/dashboard/strategy', icon: Lightbulb },
];

const businessNavigation = [
  { name: 'Business Data', href: '/dashboard/business/business-data', icon: Database },
  { name: 'ROI Dashboard', href: '/dashboard/business/roi-analysis', icon: DollarSign },
  { name: 'What-If Simulator', href: '/dashboard/business/what-if-simulator', icon: Zap },
  { name: 'Investment Decisions', href: '/dashboard/business/investment-decisions', icon: TrendingUp },
  { name: 'Executive Summary', href: '/dashboard/business/executive-summary', icon: FileText },
  { name: 'Campaign Timing', href: '/dashboard/business/campaign-timing', icon: Calendar },
  { name: 'Alternative Trends', href: '/dashboard/business/alternative-trends', icon: GitBranch },
  { name: 'Risk Analysis', href: '/dashboard/business/risk-analysis', icon: Shield },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const { user, logout, isBusinessUser } = useAuth();

  const handleLogout = () => {
    logout();
    window.location.href = '/';
  };

  // Select navigation based on user type
  const navigation = isBusinessUser ? businessNavigation : generalNavigation;

  return (
    <ProtectedRoute>
      <DomainProvider>
      <div className="flex h-screen bg-black relative overflow-hidden">
      {/* Animated background */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-blue-600/10 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-0 left-0 w-1/2 h-1/2 bg-purple-600/10 rounded-full blur-[120px] animate-pulse" style={{animationDelay: '1.5s'}} />
      </div>

      {/* Sidebar */}
      <aside className="relative w-64 border-r border-white/10 glass-strong p-6 flex flex-col z-10">
        {/* Logo */}
        <div className="mb-8">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl glass-card">
              <TrendingUp className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <h1 className="text-xl font-bold gradient-text">TrendPulse</h1>
              <p className="text-xs text-gray-500 mt-0.5">AI Analytics</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1.5">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  'flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-medium transition-all duration-300',
                  isActive
                    ? 'glass-card text-blue-400 shadow-[0_0_20px_rgba(96,165,250,0.2)]'
                    : 'text-gray-400 hover:text-white hover:glass'
                )}
              >
                <item.icon className="w-5 h-5" />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="pt-6 border-t border-white/10 space-y-2">
          <div className="flex items-center gap-3 px-3 py-2 rounded-2xl glass-card">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-sm font-bold">
              {user?.full_name?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white truncate">{user?.full_name || 'User'}</p>
              <p className="text-xs text-gray-500 capitalize">{user?.user_type || 'General'}</p>
            </div>
          </div>
          
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-medium text-gray-400 hover:text-white hover:glass transition-all duration-300"
          >
            <LogOut className="w-5 h-5" />
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="relative flex-1 overflow-auto z-10">
        <div className="p-8">
          {children}
        </div>
      </main>
      </div>
      </DomainProvider>
    </ProtectedRoute>
  );
}
