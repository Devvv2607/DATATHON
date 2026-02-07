'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
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
  MessageCircle
} from 'lucide-react';

const navigation = [
  { name: 'Overview', href: '/dashboard', icon: Activity },
  { name: 'Trend Lifecycle', href: '/dashboard/trendLifecycle', icon: TrendingUp },
  { name: 'Decline Signals', href: '/dashboard/declineSignals', icon: Shield },
  { name: 'Comeback AI', href: '/dashboard/comeback', icon: Sparkles },
  { name: 'Chat Assistant', href: '/dashboard/chat', icon: MessageCircle },
  { name: 'Explainability', href: '/dashboard/explainability', icon: Brain },
  { name: 'What-If Simulator', href: '/dashboard/simulator', icon: Sliders },
  { name: 'Network Analysis', href: '/dashboard/network', icon: Network },
  { name: 'Strategy & ROI', href: '/dashboard/strategy', icon: Lightbulb },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
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
        <div className="pt-6 border-t border-white/10">
          <div className="flex items-center gap-3 px-3 py-2 rounded-2xl glass-card">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-sm font-bold shimmer">
              U
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white truncate">User</p>
              <p className="text-xs text-gray-500">Premium</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="relative flex-1 overflow-auto z-10">
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
