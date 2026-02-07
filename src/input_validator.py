"""Input validation for Brand Trend Revenue Intelligence Agent"""
from models import ValidationResult


class InputValidator:
    """Validates and sanitizes user input from terminal"""
    
    def validate_domain(self, domain: str) -> ValidationResult:
        """
        Validate a brand domain input.
        
        Args:
            domain: The domain string to validate
            
        Returns:
            ValidationResult with validation status and normalized value
        """
        if domain is None:
            return ValidationResult(
                is_valid=False,
                error_message="Domain cannot be empty"
            )
        
        # Strip whitespace
        normalized = domain.strip()
        
        # Check if empty after stripping
        if not normalized or normalized.isspace():
            return ValidationResult(
                is_valid=False,
                error_message="Domain cannot be empty"
            )
        
        # Additional normalization: lowercase for consistency
        normalized = normalized.lower()
        
        return ValidationResult(
            is_valid=True,
            normalized_value=normalized
        )
    
    def prompt_for_domain(self) -> str:
        """
        Prompt user for brand domain via terminal input.
        
        Returns:
            Validated and normalized domain string
        """
        while True:
            print("\n" + "="*60)
            print("Brand Trend Revenue Intelligence Agent")
            print("="*60)
            print("\nEnter your brand domain/category")
            print("(e.g., clothing, technology, food, fitness, etc.)")
            print("-"*60)
            
            domain = input("Domain: ").strip()
            
            validation = self.validate_domain(domain)
            
            if validation.is_valid:
                return validation.normalized_value
            else:
                print(f"\n❌ Error: {validation.error_message}")
                print("Please try again.\n")
