# 🚀 Code Analysis & Documentation Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-Transformer%20Models-purple.svg)](https://huggingface.co)

> **Advanced AI-powered code analysis and documentation generation using transformer models (BERT, RoBERTa, BART) and tree-sitter parsing**

![Code Analyzer Demo](https://via.placeholder.com/800x400/2c3e50/white?text=Code+Analysis+%26+Documentation+Generator)

## ✨ Features

### 🔍 **Advanced Code Analysis**
- **Multi-language Support**: Python, JavaScript, Java, C++
- **Function & Class Extraction**: Automatically identify and analyze code structures
- **Complexity Analysis**: McCabe complexity calculation with warnings
- **Parameter Detection**: Extract function parameters and documentation
- **Tree-sitter Parsing**: Precise syntax analysis using industry-standard parsers

### 🛡️ **Comprehensive Error Detection & Correction**
- **Syntax Errors**: Real-time syntax validation using AST parsing
- **Security Vulnerabilities**: Detect `eval()`, `os.system()`, XSS risks, and more
- **Performance Issues**: Identify inefficient loops and anti-patterns
- **Logic Problems**: Catch bare except clauses, unused variables, poor comparisons
- **Style Violations**: PEP 8 compliance checking via Flake8 & Pylint
- **Automatic Error Correction**: Fix common issues automatically
- **Quality Scoring**: 0-100 code quality assessment with detailed suggestions

### 🤖 **AI-Powered Documentation**
- **Automatic Summarization**: BART transformer model for intelligent code summaries
- **Multiple Output Formats**: Markdown, HTML, JSON documentation
- **Docstring Extraction**: Parse and analyze existing documentation
- **Template-based Generation**: Professional documentation templates

### 🌐 **Unified Analysis Pipeline**
- **Command-line Interface**: Easy-to-use CLI for automation
- **Batch Processing**: Analyze entire directories
- **Auto-fix Capabilities**: Automatically correct detected issues
- **Multiple Output Formats**: Markdown, HTML, JSON reports
- **FastAPI Web Interface**: Optional web-based analysis
- **Progress Tracking**: Real-time analysis progress

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- 4GB+ RAM (for transformer models)
- Windows, macOS, or Linux

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/code-analyzer.git
cd code-analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Command Line Usage

#### Analyze a Single File
```bash
# Basic analysis
python main.py file example.py

# With auto-fix and output
python main.py file example.py --auto-fix --output ./output
```

#### Analyze a Directory
```bash
# Analyze all supported files
python main.py directory ./src --output ./reports

# Analyze specific file types
python main.py directory ./src --extensions .py .js --output ./reports
```

### 4. Web Interface (Optional)
```bash
# Start the web server
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Access web interface
# - Web Interface: http://localhost:8000/static/index.html
# - API Documentation: http://localhost:8000/docs
```

## 📖 Usage Examples

### Web Interface
Visit `http://localhost:8000/static/index.html` for the interactive web interface:

- 📝 **Text Input**: Paste code directly
- 📁 **File Upload**: Upload `.py`, `.js`, `.java`, `.cpp` files
- 🎯 **Real-time Analysis**: Get instant feedback on code quality
- 📊 **Visual Results**: Beautiful metrics and error reporting
- 📄 **Export Documentation**: Download in multiple formats

### API Endpoints

#### Analyze Code (JSON)
```bash
curl -X POST "http://localhost:8000/analyze/code" \
     -H "Content-Type: application/json" \
     -d '{
       "code": "def hello_world():\n    print(\"Hello, World!\")",
       "filename": "example.py"
     }'
```

#### Upload File for Analysis
```bash
curl -X POST "http://localhost:8000/analyze" \
     -F "file=@your_code.py"
```

#### Generate Documentation
```bash
curl -X POST "http://localhost:8000/documentation/code" \
     -H "Content-Type: application/json" \
     -d '{
       "code": "class Calculator:\n    def add(self, a, b):\n        return a + b",
       "filename": "calc.py",
       "format": "markdown"
     }'
```

## 🧪 Testing & Demo

### Run Analysis Tests
```bash
python test_analyzer.py
```

### Test Error Detection
```bash
python test_error_detection.py
```

### Example Analysis Output
```json
{
  "language": "python",
  "line_count": 25,
  "complexity": 3,
  "quality_score": 85.3,
  "has_errors": false,
  "functions": [
    {
      "name": "calculate_fibonacci",
      "parameters": ["n"],
      "line_start": 5,
      "line_end": 12,
      "docstring": "Calculate nth Fibonacci number"
    }
  ],
  "error_analysis": {
    "total_errors": 0,
    "total_warnings": 2,
    "errors_by_type": {...}
  },
  "summary": "This code implements a Fibonacci calculator..."
}
```

## 🏗️ Architecture

```
code_analyzer/
├── 📁 core/                         # Core analysis engines
│   ├── analyzer.py                  # Main code analyzer
│   ├── error_detector.py            # Error detection & correction
│   ├── documentation.py             # Documentation generator
│   └── __init__.py
├── 📁 static/                        # Web interface (optional)
│   └── index.html                   # Frontend application
├── 📄 main.py                       # Main CLI pipeline
├── 📄 app.py                        # FastAPI web application
├── 📄 demo_error_correction.py      # Feature demonstration
├── 📄 requirements.txt              # Dependencies
├── 🧪 test_analyzer.py              # Analysis tests
├── 🧪 test_error_detection.py       # Error detection tests
└── 📖 README.md                     # This file
```

## 🔧 Supported Languages

| Language | Extension | Features |
|----------|-----------|----------|
| **Python** | `.py` | ✅ Full support (syntax, errors, complexity, docs) |
| **JavaScript** | `.js`, `.ts` | ✅ Functions, classes, security patterns |
| **Java** | `.java` | ✅ Classes, methods, basic analysis |
| **C++** | `.cpp`, `.cc`, `.h` | ✅ Basic structure analysis |

## 🤖 AI Models Used

- **BART** (`facebook/bart-large-cnn`): Code summarization and documentation
- **Tree-sitter**: Multi-language syntax parsing
- **Custom ML**: Pattern recognition for error detection

## ⚡ Performance

- **First Startup**: ~2-3 minutes (model download)
- **Analysis Speed**: ~1-2 seconds per file
- **Memory Usage**: ~2-3 GB RAM (with models loaded)
- **Supported File Size**: Up to 10MB per file

## 🔍 Error Detection Categories

| Category | Examples | Severity |
|----------|----------|----------|
| **🛡️ Security** | `eval()`, `os.system()`, XSS | Error |
| **⚡ Performance** | Inefficient loops, list operations | Warning |
| **🧠 Logic** | Unused variables, bare except | Warning |
| **🎨 Style** | PEP 8 violations, formatting | Warning |
| **📊 Complexity** | High McCabe complexity | Warning |

## 🛠️ Development

### Adding New Languages
1. Install tree-sitter language binding
2. Add language to `self.languages` in `CodeAnalyzer`
3. Implement language-specific extraction methods
4. Add error patterns to `ErrorDetector`

### Custom Error Patterns
```python
# Add to error_detector.py
self.common_patterns['language'] = {
    'security': [
        (r'dangerous_function\s*\(', 'Avoid dangerous_function')
    ]
}
```

### Extending Documentation Templates
Modify templates in `core/documentation.py`:
- `template_markdown`: Markdown format
- `template_html`: HTML format with CSS
- `generate_json_documentation`: JSON structure

## 📊 API Reference

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and status |
| `/health` | GET | Health check and model status |
| `/analyze` | POST | Upload file for analysis |
| `/analyze/code` | POST | Analyze code from JSON |
| `/documentation` | POST | Generate docs from file |
| `/documentation/code` | POST | Generate docs from JSON |
| `/supported-languages` | GET | List supported languages |

### Response Models

#### Analysis Response
```typescript
{
  language: string,
  line_count: number,
  complexity: number,
  quality_score: number,
  has_errors: boolean,
  functions: Function[],
  classes: Class[],
  error_analysis: ErrorAnalysis,
  summary: string
}
```

#### Error Analysis
```typescript
{
  total_errors: number,
  total_warnings: number,
  errors_by_type: {[key: string]: Issue[]},
  errors_by_line: {[key: number]: Issue[]},
  quality_score: number
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Disable model loading for faster startup
EXPORT SKIP_MODEL_LOADING=true

# Optional: Custom model cache directory
EXPORT TRANSFORMERS_CACHE=/path/to/cache
```

### Model Configuration
Modify `core/analyzer.py` to use different models:
```python
self.summarizer = pipeline(
    "summarization", 
    model="your-custom-model",
    max_length=200
)
```

## 🚨 Troubleshooting

### Common Issues

#### Model Download Fails
```bash
# Solution: Check internet connection and disk space
# Models are ~1.6GB, ensure sufficient storage
```

#### Memory Issues
```bash
# Solution: Close other applications
# Minimum 4GB RAM recommended for optimal performance
```

#### Tree-sitter Errors
```bash
# Solution: Reinstall language bindings
pip uninstall tree-sitter-python tree-sitter-javascript
pip install tree-sitter-python tree-sitter-javascript
```

#### Port Already in Use
```bash
# Solution: Use different port
uvicorn app:app --port 8001
```

### Debug Mode
```bash
# Enable detailed logging
uvicorn app:app --reload --log-level debug
```

## 📈 Roadmap

### v2.0 Planned Features
- [ ] **VS Code Extension**: Direct IDE integration
- [ ] **Git Integration**: Analyze commits and pull requests
- [ ] **Custom Rules**: User-defined error patterns
- [ ] **Batch Processing**: Analyze entire projects
- [ ] **Performance Metrics**: Detailed timing and memory analysis
- [ ] **Code Suggestions**: AI-powered fix recommendations
- [ ] **Team Analytics**: Multi-developer code quality metrics
- [ ] **CI/CD Integration**: GitHub Actions, Jenkins plugins

### v2.1 Advanced Features
- [ ] **Code Clone Detection**: Identify duplicate code
- [ ] **Dependency Analysis**: Import and usage tracking
- [ ] **Test Coverage**: Integration with coverage tools
- [ ] **Custom Models**: Fine-tuned transformers for specific domains
- [ ] **Real-time Collaboration**: Live code review features

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Development Setup
```bash
# Fork the repository
git clone https://github.com/yourusername/code-analyzer.git
cd code-analyzer

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 .
pylint core/
```

### Submitting Issues
- 🐛 **Bug Reports**: Use the bug report template
- 💡 **Feature Requests**: Describe the use case and benefits
- 📖 **Documentation**: Help improve our docs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face**: For providing excellent transformer models
- **Tree-sitter**: For robust syntax parsing capabilities
- **FastAPI**: For the high-performance web framework
- **Pylint & Flake8**: For static analysis tools
- **The Open Source Community**: For continuous inspiration

## 📞 Support

- 📧 **Email**: amandeepsasidharan@gmail.com
- 📖 **Documentation**: [Full documentation](https://docs.codeanalyzer.dev)


---

<div align="center">

**⭐ Star this repository if you find it helpful!**

ge](https://codeanalyzer.dev) • [📖 Docs](https://docs.codeanalyzer.dev) • [🚀 Demo](https://demo.codeanalyzer.dev)

</div>
