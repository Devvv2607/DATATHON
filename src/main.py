"""Main entry point for Brand Trend Revenue Intelligence Agent"""
import sys
import os
from dotenv import load_dotenv
from input_validator import InputValidator
from pipeline import TrendIntelligencePipeline


def main():
    """Main application entry point"""
    # Load environment variables
    load_dotenv()
    
    # Check for GROQ API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("\n" + "="*60)
        print("ERROR: GROQ_API_KEY not found")
        print("="*60)
        print("\nPlease set your GROQ API key:")
        print("1. Copy .env.example to .env")
        print("2. Add your GROQ API key to .env")
        print("3. Or set environment variable: GROQ_API_KEY=your_key")
        print("\n" + "="*60 + "\n")
        sys.exit(1)
    
    try:
        # Initialize components
        validator = InputValidator()
        pipeline = TrendIntelligencePipeline(groq_api_key=api_key)
        
        # Get domain from user
        domain = validator.prompt_for_domain()
        
        print("\n" + "="*60)
        print(f"Analyzing trends for: {domain}")
        print("="*60)
        
        # Run analysis
        result = pipeline.analyze_domain(domain)
        
        # Display results
        print("\n" + "="*60)
        print("ANALYSIS RESULTS")
        print("="*60 + "\n")
        print(result)
        print("\n" + "="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nAnalysis cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        print("\nPlease check your configuration and try again.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
