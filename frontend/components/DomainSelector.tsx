'use client';

import { useState, useEffect } from 'react';
import { Building2, ShoppingBag, Utensils, Laptop, Sparkles, Dumbbell, Film, Car, Home, GraduationCap, Plane } from 'lucide-react';

interface Domain {
  key: string;
  name: string;
  icon: React.ReactNode;
  color: string;
}

const DOMAINS: Domain[] = [
  { key: 'fashion_retail', name: 'Fashion & Retail', icon: <ShoppingBag className="w-5 h-5" />, color: 'from-pink-500 to-purple-500' },
  { key: 'food_beverage', name: 'Food & Beverage', icon: <Utensils className="w-5 h-5" />, color: 'from-orange-500 to-red-500' },
  { key: 'technology', name: 'Technology', icon: <Laptop className="w-5 h-5" />, color: 'from-blue-500 to-cyan-500' },
  { key: 'beauty_cosmetics', name: 'Beauty & Cosmetics', icon: <Sparkles className="w-5 h-5" />, color: 'from-pink-400 to-rose-500' },
  { key: 'fitness_wellness', name: 'Fitness & Wellness', icon: <Dumbbell className="w-5 h-5" />, color: 'from-green-500 to-emerald-500' },
  { key: 'entertainment', name: 'Entertainment', icon: <Film className="w-5 h-5" />, color: 'from-purple-500 to-indigo-500' },
  { key: 'automotive', name: 'Automotive', icon: <Car className="w-5 h-5" />, color: 'from-gray-500 to-slate-600' },
  { key: 'real_estate', name: 'Real Estate', icon: <Home className="w-5 h-5" />, color: 'from-amber-500 to-yellow-500' },
  { key: 'education', name: 'Education', icon: <GraduationCap className="w-5 h-5" />, color: 'from-blue-400 to-indigo-500' },
  { key: 'travel_hospitality', name: 'Travel & Hospitality', icon: <Plane className="w-5 h-5" />, color: 'from-teal-500 to-cyan-500' },
];

interface DomainSelectorProps {
  value: string;
  onChange: (domain: string) => void;
  className?: string;
}

export default function DomainSelector({ value, onChange, className = '' }: DomainSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const selectedDomain = DOMAINS.find(d => d.key === value) || DOMAINS[2]; // Default to technology

  return (
    <div className={`relative ${className}`}>
      {/* Selected Domain Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-3 px-4 py-3 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all duration-300 w-full"
      >
        <div className={`p-2 rounded-lg bg-gradient-to-br ${selectedDomain.color}`}>
          {selectedDomain.icon}
        </div>
        <div className="flex-1 text-left">
          <div className="text-sm text-gray-400">Business Domain</div>
          <div className="font-semibold text-white">{selectedDomain.name}</div>
        </div>
        <svg
          className={`w-5 h-5 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-gray-900/95 backdrop-blur-xl border border-white/10 rounded-xl shadow-2xl z-50 overflow-hidden">
          <div className="p-2 max-h-96 overflow-y-auto">
            {DOMAINS.map((domain) => (
              <button
                key={domain.key}
                onClick={() => {
                  onChange(domain.key);
                  setIsOpen(false);
                }}
                className={`w-full flex items-center gap-3 px-3 py-3 rounded-lg transition-all duration-200 ${
                  value === domain.key
                    ? 'bg-white/10 border border-white/20'
                    : 'hover:bg-white/5 border border-transparent'
                }`}
              >
                <div className={`p-2 rounded-lg bg-gradient-to-br ${domain.color}`}>
                  {domain.icon}
                </div>
                <div className="flex-1 text-left">
                  <div className="font-medium text-white">{domain.name}</div>
                </div>
                {value === domain.key && (
                  <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Backdrop to close dropdown */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
}
