"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Send, Bot, User, TrendingDown, AlertCircle, Lightbulb, BarChart3, Sparkles } from "lucide-react"

// Helper function to render markdown-style text
const renderMarkdown = (text: string) => {
  const parts = text.split(/(\*\*.*?\*\*)/g)
  return parts.map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={index} className="font-semibold text-white">{part.slice(2, -2)}</strong>
    }
    return <span key={index}>{part}</span>
  })
}

interface Message {
  role: "user" | "assistant"
  content: string
  timestamp?: string
  structuredData?: StructuredData[]
  suggestedFollowups?: string[]
}

interface StructuredData {
  type: string
  data: any
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "👋 Hi! I'm your Trend Intelligence Assistant. Ask me:\n\n• Why a trend is declining\n• What content to create\n• Why you got a specific alert level\n• To show you the data\n\nTry: 'Why is fidget spinner declining?'",
      timestamp: new Date().toISOString()
    }
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [trendName, setTrendName] = useState("")
  
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const response = await fetch("http://localhost:8000/api/chat/message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: input,
          trend_name: trendName || null,
          conversation_history: messages.slice(-5)
        })
      })

      if (!response.ok) {
        throw new Error("Failed to get response")
      }

      const data = await response.json()

      const assistantMessage: Message = {
        role: "assistant",
        content: data.message,
        timestamp: new Date().toISOString(),
        structuredData: data.structured_data || [],
        suggestedFollowups: data.suggested_followups || []
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error("Chat error:", error)
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, I encountered an error. Please make sure the backend is running on port 8000.",
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleFollowup = (followup: string) => {
    setInput(followup)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const renderStructuredData = (data: StructuredData) => {
    switch (data.type) {
      case "analysis":
        return renderAnalysis(data.data)
      case "explanation":
        return renderExplanation(data.data)
      case "content":
        return renderContent(data.data)
      case "decline_signals":
        return renderDeclineSignals(data.data)
      case "chart":
        return renderChart(data.data)
      default:
        return null
    }
  }

  const renderAnalysis = (analysis: any) => {
    const causes = analysis?.root_causes || []
    const topCauses = causes.slice(0, 3)

    return (
      <div className="glass-card p-5 mt-3 rounded-2xl border border-orange-500/30">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 rounded-xl bg-orange-500/20">
            <TrendingDown className="w-5 h-5 text-orange-400" />
          </div>
          <h4 className="font-semibold text-white text-base">Decline Analysis</h4>
        </div>
        <div className="space-y-2">
          {topCauses.map((cause: any, idx: number) => (
            <div key={idx} className="flex justify-between items-center p-3 bg-white/5 rounded-xl border border-white/10 hover:border-orange-500/30 transition-colors">
              <span className="text-sm text-gray-200">{cause.cause_type?.replace(/_/g, " ")}</span>
              <span className="text-sm font-bold text-orange-400">
                {Math.round(cause.confidence * 100)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    )
  }

  const renderExplanation = (explanation: any) => {
    const signals = explanation?.signal_contributions || []
    const decision = explanation?.decision_summary || {}

    return (
      <div className="glass-card p-5 mt-3 rounded-2xl border border-blue-500/30">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 rounded-xl bg-blue-500/20">
            <AlertCircle className="w-5 h-5 text-blue-400" />
          </div>
          <h4 className="font-semibold text-white text-base">Alert Explanation</h4>
        </div>
        <div className="space-y-3">
          <div className="p-3 bg-gradient-to-br from-blue-950/30 to-blue-900/20 rounded-xl border border-blue-500/20">
            <div className="text-xs text-blue-300 mb-1">Status</div>
            <div className="font-semibold text-white">{decision.status}</div>
          </div>
          <div className="text-sm text-gray-200">
            <div className="font-semibold text-white mb-2">Top Signals:</div>
            {signals.slice(0, 3).map((sig: any, idx: number) => (
              <div key={idx} className="ml-3 mt-2 flex items-center gap-2">
                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full"></div>
                <span className="text-gray-300">{sig.signal?.replace(/_/g, " ")}: <span className="font-semibold text-blue-400">+{sig.impact_on_risk} points</span></span>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  const renderContent = (content: any) => {
    const reels = content?.reels || []

    return (
      <div className="glass-card p-5 mt-3 rounded-2xl border border-yellow-500/30">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 rounded-xl bg-yellow-500/20 shimmer">
            <Lightbulb className="w-5 h-5 text-yellow-400" />
          </div>
          <h4 className="font-semibold text-white text-base">Content Ideas</h4>
        </div>
        <div className="space-y-3">
          {reels.slice(0, 3).map((reel: any, idx: number) => (
            <div key={idx} className="p-4 bg-gradient-to-br from-yellow-950/30 to-amber-950/20 rounded-xl border border-yellow-500/20 hover:border-yellow-500/40 transition-colors">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-6 h-6 rounded-lg bg-yellow-500/20 flex items-center justify-center">
                  <span className="text-xs font-bold text-yellow-400">{idx + 1}</span>
                </div>
                <div className="font-semibold text-sm text-yellow-300">Reel Idea</div>
              </div>
              <div className="text-sm text-gray-200 leading-relaxed">{reel.hook}</div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  const renderDeclineSignals = (signals: any) => {
    const breakdown = signals?.signal_breakdown || {}
    const alertLevel = signals?.alert_level || "unknown"
    const riskScore = signals?.decline_risk_score || 0

    const getAlertColor = () => {
      switch(alertLevel) {
        case "red": return "border-red-500/30 bg-red-500/5";
        case "orange": return "border-orange-500/30 bg-orange-500/5";
        case "yellow": return "border-yellow-500/30 bg-yellow-500/5";
        default: return "border-green-500/30 bg-green-500/5";
      }
    }

    return (
      <div className={`glass-card p-5 mt-3 rounded-2xl border ${getAlertColor()}`}>
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 rounded-xl bg-purple-500/20">
            <BarChart3 className="w-5 h-5 text-purple-400" />
          </div>
          <h4 className="font-semibold text-white text-base">Decline Signals</h4>
        </div>
        <div className="space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 bg-white/5 rounded-xl border border-white/10">
              <div className="text-xs text-gray-400 mb-1">Risk Score</div>
              <div className="font-bold text-2xl gradient-text">{riskScore}/100</div>
            </div>
            <div className="p-3 bg-white/5 rounded-xl border border-white/10">
              <div className="text-xs text-gray-400 mb-1">Alert Level</div>
              <span className={`inline-block font-bold px-3 py-1 rounded-lg text-sm ${
                alertLevel === "red" ? "bg-red-500/20 text-red-400" :
                alertLevel === "orange" ? "bg-orange-500/20 text-orange-400" :
                alertLevel === "yellow" ? "bg-yellow-500/20 text-yellow-400" :
                "bg-green-500/20 text-green-400"
              }`}>
                {alertLevel.toUpperCase()}
              </span>
            </div>
          </div>
          <div className="pt-2">
            <div className="text-xs text-gray-400 mb-3 font-medium">Signal Breakdown:</div>
            <div className="space-y-2">
              {Object.entries(breakdown).map(([key, value]: [string, any]) => (
                <div key={key} className="flex justify-between items-center p-2 bg-white/5 rounded-lg border border-white/5">
                  <span className="text-sm text-gray-300">{key.replace(/_/g, " ")}</span>
                  <span className="text-sm font-semibold text-white">{value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  const renderChart = (data: any) => {
    return (
      <div className="glass-card p-5 mt-3 rounded-2xl border border-indigo-500/30">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2 rounded-xl bg-indigo-500/20">
            <BarChart3 className="w-5 h-5 text-indigo-400" />
          </div>
          <h4 className="font-semibold text-white text-base">Trend Data</h4>
        </div>
        <div className="text-sm text-gray-300">
          Full data visualization available in structured view
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-3 rounded-2xl glass-card shimmer">
              <Sparkles className="w-6 h-6 text-purple-400" />
            </div>
            <div>
              <h1 className="text-3xl font-bold gradient-text">
                AI Chat Assistant
              </h1>
              <p className="text-sm text-gray-400 mt-1">
                Powered by Groq • Unified Intelligence Platform
              </p>
            </div>
          </div>
        </div>

        {/* Optional Trend Name Input */}
        <div className="glass-card p-4 mb-4 border border-white/10 rounded-2xl">
          <label className="text-sm text-gray-400 mb-2 block font-medium">
            🎯 Set Trend Context (Optional)
          </label>
          <Input
            value={trendName}
            onChange={(e) => setTrendName(e.target.value)}
            placeholder="e.g., fidget spinner, cricket match, trending topic..."
            className="bg-black/30 border-white/10 rounded-xl text-white placeholder:text-gray-500"
          />
        </div>

        {/* Chat Container */}
        <div className="glass-card p-6 mb-6 rounded-2xl border border-white/10 h-[600px] flex flex-col backdrop-blur-xl">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto mb-4 space-y-4 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
            {messages.map((msg, idx) => (
              <div key={idx} className="flex gap-3">
                <div>
                  {/* Avatar */}
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
                    msg.role === "user" 
                      ? "bg-gradient-to-br from-blue-500 to-blue-600 shimmer" 
                      : "bg-gradient-to-br from-purple-500 to-pink-500 shimmer"
                  }`}>
                    {msg.role === "user" ? (
                      <User className="w-5 h-5 text-white" />
                    ) : (
                      <Bot className="w-5 h-5 text-white" />
                    )}
                  </div>
                </div>

                {/* Message Content */}
                <div className="flex-1">
                  <div className={`p-4 rounded-2xl ${
                    msg.role === "user"
                      ? "bg-gradient-to-br from-blue-600/20 to-blue-500/10 border border-blue-500/20"
                      : "glass-card border border-white/10"
                  }`}>
                    <div className="whitespace-pre-wrap text-sm leading-relaxed text-gray-100">
                      {renderMarkdown(msg.content)}
                    </div>
                  </div>

                  {/* Structured Data */}
                  {msg.structuredData && msg.structuredData.length > 0 && (
                    <div className="mt-2 space-y-2">
                      {msg.structuredData.map((data, dataIdx) => (
                        <div key={dataIdx}>
                          {renderStructuredData(data)}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Suggested Followups */}
                  {msg.suggestedFollowups && msg.suggestedFollowups.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {msg.suggestedFollowups.map((followup, fIdx) => (
                        <button
                          key={fIdx}
                          onClick={() => handleFollowup(followup)}
                          className="text-xs px-3 py-2 glass-card border border-white/10 hover:border-purple-500/50 rounded-xl transition-all hover:scale-105"
                        >
                          {followup}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 shimmer flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white animate-pulse" />
                </div>
                <div className="glass-card border border-white/10 p-4 rounded-2xl">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about trends, content strategies, or alerts..."
              className="flex-1 bg-black/30 border-white/10 rounded-xl text-white placeholder:text-gray-500 h-12"
              disabled={isLoading}
            />
            <Button
              onClick={handleSend}
              disabled={isLoading || !input.trim()}
              className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 shimmer rounded-xl px-6 h-12"
            >
              <Send className="w-5 h-5" />
            </Button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <button
            onClick={() => setInput("Why is fidget spinner declining?")}
            className="glass-card border border-white/10 rounded-2xl p-4 hover:border-orange-500/50 transition-all hover:scale-105 group"
          >
            <TrendingDown className="w-5 h-5 mb-2 text-orange-400 group-hover:scale-110 transition-transform" />
            <div className="text-sm font-medium text-white">Why Declining?</div>
          </button>
          <button
            onClick={() => setInput("What should I do about this trend?")}
            className="glass-card border border-white/10 rounded-2xl p-4 hover:border-yellow-500/50 transition-all hover:scale-105 group"
          >
            <Lightbulb className="w-5 h-5 mb-2 text-yellow-400 group-hover:scale-110 transition-transform" />
            <div className="text-sm font-medium text-white">What To Do?</div>
          </button>
          <button
            onClick={() => setInput("Why is this ORANGE?")}
            className="glass-card border border-white/10 rounded-2xl p-4 hover:border-blue-500/50 transition-all hover:scale-105 group"
          >
            <AlertCircle className="w-5 h-5 mb-2 text-blue-400 group-hover:scale-110 transition-transform" />
            <div className="text-sm font-medium text-white">Why Alert?</div>
          </button>
          <button
            onClick={() => setInput("Show me the data")}
            className="glass-card border border-white/10 rounded-2xl p-4 hover:border-purple-500/50 transition-all hover:scale-105 group"
          >
            <BarChart3 className="w-5 h-5 mb-2 text-purple-400 group-hover:scale-110 transition-transform" />
            <div className="text-sm font-medium text-white">Show Data</div>
          </button>
        </div>
      </div>
    </div>
  )
}
