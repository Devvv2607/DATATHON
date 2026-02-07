# Brand Trend Revenue Intelligence Agent

An AI-powered system that analyzes brand trends using Google Trends data and provides actionable revenue recommendations.

## Features

- **Trend Discovery**: Automatically discover trending topics in your business domain
- **Trend Classification**: Classify trends as growing, stable, or declining
- **Growth Recommendations**: Get 3 concrete actions to capitalize on growing trends
- **Decline Analysis**: Receive early warnings and pivot strategies for declining trends
- **Structured Output**: All results in JSON format for easy integration

## Setup

1. **Create virtual environment** (if not already created):
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   - Windows: `activate_venv.bat` or `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Add your GROQ API key to `.env`

## Usage

```bash
python -m src.main
```

Enter your brand domain when prompted, and the system will analyze trends and provide recommendations.

## Project Structure

```
.
├── src/                    # Source code
│   ├── models.py          # Data models
│   ├── input_validator.py # Input validation
│   ├── trend_discovery.py # Google Trends integration
│   ├── trend_analyzer.py  # Trend analysis
│   ├── classifier.py      # Trend classification
│   ├── groq_service.py    # GROQ API integration
│   ├── recommenders.py    # Recommendation generation
│   ├── formatter.py       # JSON output formatting
│   └── main.py           # Main application
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   ├── property/         # Property-based tests
│   └── integration/      # Integration tests
├── config/               # Configuration files
└── requirements.txt      # Python dependencies
```

## Requirements

- Python 3.8+
- GROQ API key
- Internet connection for Google Trends data

## License

MIT
