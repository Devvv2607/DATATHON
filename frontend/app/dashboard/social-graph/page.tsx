"use client"

import { useCallback, useState, type FormEvent } from "react"
import {
  AlertCircle,
  Loader2,
  RefreshCcw,
  Search,
  Share2,
  Sparkles,
  X,
} from "lucide-react"

import {
  RedditNetworkGraph,
  redditNodePalette,
} from "@/components/social-graph/RedditNetworkGraph"
import type {
  RedditSocialGraphResponse,
  SelectedGraphNode,
} from "@/types/social-graph"
import type { Network } from "vis-network"

const RANGE_LABELS: Record<string, string> = {
  day: "Past day",
  month: "Past month",
  year: "Past year",
}

const RANGE_OPTIONS: { value: "day" | "month" | "year"; label: string }[] = [
  { value: "day", label: "Past day" },
  { value: "month", label: "Past month" },
  { value: "year", label: "Past year" },
]

export default function SocialGraphPage() {
  const getCachedGraph = (keyword: string, timeRange: string) => {
    if (typeof window === 'undefined') return null;
    const cached = localStorage.getItem(`social_graph_${keyword}_${timeRange}`);
    if (cached) {
      try {
        const { data, timestamp } = JSON.parse(cached);
        // Use cache if less than 2 hours old
        if (Date.now() - timestamp < 2 * 60 * 60 * 1000) {
          return data;
        }
      } catch (e) {
        return null;
      }
    }
    return null;
  };

  const [keyword, setKeyword] = useState("")
  const [timeRange, setTimeRange] = useState<"day" | "month" | "year">("day")
  const [graphData, setGraphData] = useState<RedditSocialGraphResponse | null>(null)
  const [selectedNode, setSelectedNode] = useState<SelectedGraphNode | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [networkInstance, setNetworkInstance] = useState<Network | null>(null)

  const runQuery = useCallback(async () => {
    setError(null)
    setSelectedNode(null)

    try {
      const trimmedKeyword = keyword.trim()
      if (!trimmedKeyword) {
        throw new Error("Enter a keyword to search on Reddit.")
      }

      // Check cache first
      const cachedData = getCachedGraph(trimmedKeyword, timeRange);
      if (cachedData) {
        setGraphData(cachedData);
      }

      setLoading(!cachedData);

      const payload = {
        keyword: trimmedKeyword,
        time_range: timeRange,
        max_posts: 20,
        max_comments: 100,
        max_users: 25,
      }

      const response = await fetch("http://localhost:8000/api/social-graph/reddit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        const message = await response.text()
        throw new Error(message || "Failed to fetch social graph data.")
      }

      const data = await response.json()
      setGraphData(data)
      
      // Cache the result
      localStorage.setItem(`social_graph_${trimmedKeyword}_${timeRange}`, JSON.stringify({
        data,
        timestamp: Date.now()
      }));
    } catch (err) {
      console.error(err)
      if (!graphData) {
        setGraphData(null);
        setError(err instanceof Error ? err.message : "Unable to fetch Reddit data.")
      }
    } finally {
      setLoading(false)
    }
  }, [keyword, timeRange])

  const handleSubmit = useCallback(
    async (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault()
      await runQuery()
    },
    [runQuery]
  )

  return (
    <div className="min-h-screen">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-3 rounded-2xl glass-card">
              <Sparkles className="w-6 h-6 text-cyan-400" />
            </div>
            <div>
              <h1 className="text-3xl font-bold gradient-text">
                Reddit Social Graph
              </h1>
              <p className="text-sm text-gray-400 mt-1">
                Visualize Reddit Network Intelligence
              </p>
            </div>
          </div>
          <p className="text-sm text-gray-400">
            Explore how Reddit users, posts, and comments connect across a topic. Enter a keyword and
            choose a time window to analyze up to 20 posts, 100 comments, and 25 high-activity users.
          </p>
        </div>

        {/* Query Form */}
        <section className="glass-card p-6 rounded-2xl border border-white/10">
          <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-[2fr_auto_auto] items-end">
            <label className="flex flex-col gap-2 text-sm font-medium text-white">
              Keyword
              <div className="relative">
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
                <input
                  type="text"
                  value={keyword}
                  onChange={(event) => setKeyword(event.target.value)}
                  placeholder="e.g. elections, crypto, AI"
                  className="w-full rounded-xl border border-white/10 bg-black/30 py-3 pl-10 pr-4 text-white placeholder:text-gray-500 focus:border-cyan-500 focus:outline-none"
                />
              </div>
            </label>

            <div className="flex flex-col gap-2 text-sm font-medium text-white">
              Time range
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value as "day" | "month" | "year")}
                className="rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-white focus:border-cyan-500 focus:outline-none"
              >
                {RANGE_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <button
              type="submit"
              className="bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 rounded-xl px-6 py-3 text-sm font-semibold text-white transition disabled:cursor-not-allowed disabled:opacity-50"
              disabled={loading}
            >
              {loading ? (
                <span className="inline-flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" /> Fetching
                </span>
              ) : (
                "Build Graph"
              )}
            </button>
          </form>

          {error && (
            <div className="mt-4 flex items-center gap-2 rounded-xl border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-400">
              <AlertCircle className="h-4 w-4" />
              <p>{error}</p>
            </div>
          )}

          {graphData && (
            <p className="mt-3 text-xs uppercase tracking-wider text-gray-500">
              Range · {RANGE_LABELS[graphData.query.time_range] ?? graphData.query.time_range}
            </p>
          )}
        </section>

        {/* Graph Container */}
        <div className="relative">
          <RedditNetworkGraph
            data={graphData}
            onSelect={setSelectedNode}
            onNetworkReady={setNetworkInstance}
          />

          <div className="pointer-events-none absolute inset-0">
            {/* Legend */}
            <div className="pointer-events-auto absolute left-6 top-6 flex flex-wrap gap-3 rounded-2xl border border-white/10 glass-card px-5 py-3 text-xs uppercase tracking-wider text-white shadow-lg">
              {[
                { label: "Posts", color: redditNodePalette.post },
                { label: "Comments", color: redditNodePalette.comment },
                { label: "Users", color: redditNodePalette.user },
              ].map((item) => (
                <span key={item.label} className="flex items-center gap-2">
                  <span
                    className="h-2.5 w-2.5 rounded-full"
                    style={{ backgroundColor: item.color }}
                  />
                  {item.label}
                </span>
              ))}
            </div>

            {/* Reset Button */}
            <button
              type="button"
              onClick={() =>
                networkInstance?.moveTo({
                  position: { x: 0, y: 0 },
                  scale: 1,
                  animation: { duration: 600, easingFunction: "easeInOutQuad" },
                })
              }
              className="pointer-events-auto absolute right-6 top-6 inline-flex items-center gap-2 rounded-2xl border border-white/10 glass-card px-4 py-2 text-xs font-semibold uppercase tracking-wider text-white shadow-lg transition hover:bg-white/10"
            >
              <RefreshCcw className="h-3.5 w-3.5" />
              Reset
            </button>

            {/* Node Details Panel */}
            {selectedNode && (
              <div className="pointer-events-auto absolute bottom-6 right-6 w-full max-w-sm rounded-2xl border border-white/10 glass-card p-5 text-sm text-white shadow-lg">
                <div className="mb-3 flex items-center justify-between gap-3">
                  <p className="text-xs uppercase tracking-wider text-gray-400">
                    {selectedNode.type}
                  </p>
                  <button
                    type="button"
                    onClick={() => setSelectedNode(null)}
                    className="text-gray-400 transition hover:text-white"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>

                {selectedNode.type === "user" && "username" in selectedNode.payload && (
                  <div className="space-y-2">
                    <p className="text-xl font-semibold">@{selectedNode.payload.username}</p>
                    <p className="text-gray-300">Posts authored: {selectedNode.payload.post_count}</p>
                    <p className="text-gray-300">Comments made: {selectedNode.payload.comment_count}</p>
                  </div>
                )}

                {selectedNode.type === "post" && "title" in selectedNode.payload && (
                  <div className="space-y-2">
                    <p className="text-lg font-semibold">{selectedNode.payload.title}</p>
                    <p className="text-gray-300">u/{selectedNode.payload.author}</p>
                    <p className="text-gray-300">Score: {selectedNode.payload.score}</p>
                    <p className="text-gray-300">Comments: {selectedNode.payload.num_comments}</p>
                    <a
                      href={selectedNode.payload.permalink}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-2 text-cyan-400 hover:text-cyan-300"
                    >
                      View on Reddit <Share2 className="h-3 w-3" />
                    </a>
                  </div>
                )}

                {selectedNode.type === "comment" && "body" in selectedNode.payload && (
                  <div className="space-y-2">
                    <p className="font-semibold">Comment</p>
                    <p className="text-gray-300">{selectedNode.payload.body || "[deleted]"}</p>
                    <p className="text-gray-400">u/{selectedNode.payload.author}</p>
                    <p className="text-gray-300">Score: {selectedNode.payload.score}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
