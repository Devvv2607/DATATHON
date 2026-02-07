"""Main application pipeline orchestrator"""
import logging
from typing import Optional
from models import TrendData, ErrorResponse
from input_validator import InputValidator
from trend_discovery import TrendDiscoveryService
from trend_analyzer import TrendAnalyzer
from classifier import TrendClassifier
from groq_service import GroqService
from recommenders import GrowthRecommender, DeclineAnalyzer
from formatter import ResponseFormatter


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TrendIntelligencePipeline:
    """Orchestrates the complete trend analysis pipeline"""
    
    def __init__(self, groq_api_key: Optional[str] = None):
        """
        Initialize the pipeline with all components.
        
        Args:
            groq_api_key: Optional GROQ API key
        """
        try:
            # Initialize all components
            self.validator = InputValidator()
            self.discovery = TrendDiscoveryService()
            self.analyzer = TrendAnalyzer()
            self.classifier = TrendClassifier()
            self.groq_service = GroqService(api_key=groq_api_key)
            self.growth_recommender = GrowthRecommender(self.groq_service)
            self.decline_analyzer = DeclineAnalyzer(self.groq_service)
            self.formatter = ResponseFormatter()
            
            logger.info("Pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {str(e)}")
            raise
    
    def analyze_domain(self, domain: str) -> str:
        """
        Analyze trends for a given domain and return JSON response.
        
        Args:
            domain: Business domain/category
            
        Returns:
            JSON string with analysis results
        """
        try:
            # Step 1: Validate input
            logger.info(f"Validating domain: {domain}")
            validation = self.validator.validate_domain(domain)
            
            if not validation.is_valid:
                error = ErrorResponse(
                    error_type="validation_error",
                    message=validation.error_message,
                    retry_possible=True
                )
                return self.formatter.format_error(error)
            
            normalized_domain = validation.normalized_value
            logger.info(f"Domain validated: {normalized_domain}")
            
            # Step 2: Discover trends
            logger.info("Discovering trends...")
            print("\n🔍 Discovering trends in your domain...")
            trends = self.discovery.discover_trends(normalized_domain, limit=3)
            
            if not trends or len(trends) == 0:
                error = ErrorResponse(
                    error_type="no_data",
                    message="No trends found for this domain",
                    retry_possible=True
                )
                return self.formatter.format_error(error)
            
            logger.info(f"Found {len(trends)} trends")
            print(f"✓ Found {len(trends)} trends")
            
            # Analyze the first (most relevant) trend
            trend = trends[0]
            logger.info(f"Analyzing trend: {trend.keyword}")
            print(f"\n📊 Analyzing: {trend.keyword}")
            
            # Step 3: Analyze trend metrics
            logger.info("Calculating trend metrics...")
            print("   Calculating growth metrics...")
            metrics = self.analyzer.analyze_trend_momentum(trend)
            logger.info(f"Growth slope: {metrics.growth_slope:.1f}%")
            
            # Step 4: Classify trend
            logger.info("Classifying trend...")
            print("   Classifying trend momentum...")
            classification = self.classifier.classify(metrics)
            logger.info(f"Classification: {classification.category}")
            print(f"   ✓ Trend is {classification.category.upper()}")
            
            # Step 5: Generate recommendations
            recommendations = None
            
            if classification.category == "growing":
                logger.info("Generating growth recommendations...")
                print("\n💡 Generating growth recommendations...")
                recommendations = self.growth_recommender.generate_recommendations(
                    trend, metrics, normalized_domain
                )
                logger.info("Growth recommendations generated")
                
            elif classification.category == "declining":
                logger.info("Analyzing decline and pivot strategy...")
                print("\n⚠️  Analyzing decline and pivot strategy...")
                recommendations = self.decline_analyzer.analyze_decline(
                    trend, metrics, normalized_domain
                )
                logger.info("Decline analysis complete")
            
            # Step 6: Format response
            logger.info("Formatting response...")
            print("\n📄 Formatting results...\n")
            response = self.formatter.format_response(
                classification, recommendations, trend
            )
            
            logger.info("Analysis complete")
            return response
            
        except Exception as e:
            logger.error(f"Pipeline error: {str(e)}", exc_info=True)
            error = ErrorResponse(
                error_type="pipeline_error",
                message=f"Analysis failed: {str(e)}",
                retry_possible=True
            )
            return self.formatter.format_error(error)
