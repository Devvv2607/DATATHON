# 🎨 Frontend - TrendPredict Dashboard

Modern, dark-mode-first dashboard built with Next.js 14, TypeScript, and Tailwind CSS.

## 📁 Structure

```
frontend/
├── app/
│   ├── dashboard/
│   │   ├── layout.tsx                  # Sidebar navigation
│   │   ├── page.tsx                    # Main dashboard
│   │   ├── trendLifecycle/            # Lifecycle visualization
│   │   ├── explainability/            # XAI insights
│   │   ├── simulator/                 # What-if simulator
│   │   ├── network/                   # Network analysis
│   │   └── strategy/                  # Strategy & ROI
│   ├── globals.css                    # Global styles
│   └── layout.tsx                     # Root layout
│
├── components/
│   └── dashboard/
│       ├── Charts.tsx                 # Recharts wrappers
│       ├── MetricCard.tsx             # Metric display card
│       ├── ProbabilityGauge.tsx       # Circular gauge
│       └── TrendCard.tsx              # Trend overview card
│
├── lib/
│   ├── api.ts                         # Backend API client
│   ├── mockData.ts                    # Development data
│   └── utils.ts                       # Utility functions
│
└── package.json
```

## 🚀 Development

### Install Dependencies
```bash
npm install
```

### Run Development Server
```bash
npm run dev
```

### Build for Production
```bash
npm run build
npm start
```

Visit `http://localhost:3000/dashboard` to see the application.

---

Built for hackathons | Modern SaaS UI | Production-ready

