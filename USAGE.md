# Code Analysis and Documentation Generator

A sophisticated tool that uses transformer models (BERT, RoBERTa, BART) and tree-sitter parsing to analyze code and generate comprehensive documentation.

## Features

🔍 **Advanced Code Analysis**
- Multi-language support (Python, JavaScript, Java, C++)
- Function and class extraction
- Cyclomatic complexity calculation
- Parameter detection and documentation

🤖 **AI-Powered Documentation**
- Automatic summary generation using BART transformer
- Multiple output formats (Markdown, HTML, JSON)
- Docstring extraction and analysis

🚀 **REST API Interface**
- FastAPI-based web service
- File upload and text-based analysis
- Interactive API documentation

## Quick Start

### 1. Activate the Virtual Environment
```bash
D:\website\code_analyzer\venv\Scripts\Activate.ps1
```

### 2. Start the API Server
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the Interactive Documentation
Open your browser and visit: `http://localhost:8000/docs`

## API Endpoints

### 📊 Analysis Endpoints
- `POST /analyze` - Upload code files for analysis
- `POST /analyze/code` - Analyze code provided as JSON text
- `GET /health` - Check system health and model status

### 📝 Documentation Endpoints
- `POST /documentation` - Generate docs from uploaded files
- `POST /documentation/code` - Generate docs from JSON text
- `GET /supported-languages` - List supported programming languages

### Example API Usage

**Analyze Code (JSON)**
```bash
curl -X POST "http://localhost:8000/analyze/code" \
     -H "Content-Type: application/json" \
     -d '{
       "code": "def hello_world():\n    \"\"\"Print hello world\"\"\"\n    print(\"Hello, World!\")",
       "filename": "example.py"
     }'
```

**Generate Documentation**
```bash
curl -X POST "http://localhost:8000/documentation/code" \
     -H "Content-Type: application/json" \
     -d '{
       "code": "class Calculator:\n    def add(self, a, b):\n        return a + b",
       "filename": "calc.py",
       "format": "markdown"
     }'
```

## Testing the Analyzer

Run the test script to see the analyzer in action:
```bash
python test_analyzer.py
```

## Supported Languages

- **Python** (.py) - Full support with docstring extraction
- **JavaScript** (.js, .ts) - Function and class detection
- **Java** (.java) - Class and method analysis
- **C++** (.cpp, .cc, .cxx, .c) - Basic structure analysis

## Output Formats

### 1. Analysis Results (JSON)
```json
{
  "language": "python",
  "line_count": 25,
  "complexity": 3,
  "functions": [...],
  "classes": [...],
  "summary": "AI-generated code summary"
}
```

### 2. Documentation Formats
- **Markdown** - Clean, readable documentation
- **HTML** - Styled web-ready documentation
- **JSON** - Structured data with metadata

## Project Structure

```
code_analyzer/
├── app.py                 # FastAPI application
├── models.py              # Pydantic data models
├── requirements.txt       # Dependencies
├── core/
│   ├── analyzer.py        # Core analysis engine
│   ├── documentation.py   # Documentation generator
│   └── __init__.py
├── test_analyzer.py       # Test script
└── venv/                  # Virtual environment
```

## Key Components

### 🧠 CodeAnalyzer
- Tree-sitter parsing for syntax analysis
- BART model for code summarization
- Multi-language detection and processing

### 📄 DocumentationGenerator
- Template-based documentation generation
- Multiple output format support
- Structured content organization

### 🌐 FastAPI Application
- RESTful API endpoints
- File upload support
- CORS enabled for web integration

## Advanced Usage

### Custom Analysis
```python
from core.analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()
result = analyzer.analyze_code_file(code_string, "filename.py")
```

### Documentation Generation
```python
from core.documentation import DocumentationGenerator

doc_gen = DocumentationGenerator()
docs = doc_gen.generate_documentation(analysis_result, "markdown")
```

## Performance Notes

- **Model Loading**: First startup takes ~2-3 minutes to download BART model
- **Analysis Speed**: ~1-2 seconds per file for typical code files
- **Memory Usage**: ~2-3 GB RAM when transformer models are loaded

## Development

To extend the analyzer:

1. **Add Language Support**: Update `self.languages` in `CodeAnalyzer`
2. **Custom Models**: Modify `_initialize_models()` method
3. **New Endpoints**: Add routes to `app.py`
4. **Documentation Templates**: Update `DocumentationGenerator`

## Troubleshooting

### Common Issues
- **Model Download Fails**: Check internet connection, models are large (~1.6GB)
- **Tree-sitter Errors**: Ensure all language bindings are installed
- **Memory Issues**: Close other applications, transformer models are memory-intensive

### Error Messages
- `Analysis failed`: Usually indicates syntax errors in the input code
- `Summary generation unavailable`: Transformer model failed to load
- `Unsupported language`: Language not in supported list

## License

This project is for educational and development purposes.
