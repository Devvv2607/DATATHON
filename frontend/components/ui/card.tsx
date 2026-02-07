import * as React from "react"

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className = "", children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={`rounded-lg border border-gray-800 bg-gray-900/50 shadow-sm ${className}`}
        {...props}
      >
        {children}
      </div>
    )
  }
)

Card.displayName = "Card"

export { Card }
