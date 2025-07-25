# Contributing to Code Analysis & Documentation Generator

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🚀 Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Branch Strategy
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical fixes

## 🛠️ Development Setup

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/code-analyzer.git
   cd code-analyzer
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\Activate.ps1 on Windows
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

## 📝 Pull Request Process

1. **Update tests** - Ensure your code has appropriate test coverage
2. **Update documentation** - Update README.md and docstrings as needed
3. **Follow code style** - Run linting tools before submitting
4. **Write descriptive commit messages**
5. **Create pull request** with a clear description

### Commit Message Format
```
type(scope): description

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(analyzer): add support for TypeScript analysis

- Implement TypeScript parser using tree-sitter
- Add error detection patterns for TypeScript
- Update documentation with TypeScript examples

Closes #123
```

## 🧪 Testing

Run the test suite before submitting:

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python test_analyzer.py
python test_error_detection.py

# Run with coverage
pytest --cov=core tests/
```

## 🎨 Code Style

We use several tools to maintain code quality:

```bash
# Format code
black .
autopep8 --in-place --recursive .

# Lint code
flake8 .
pylint core/

# Type checking
mypy core/
```

### Style Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep line length under 88 characters (Black default)
- Use type hints where appropriate

## 🐛 Bug Reports

Great Bug Reports tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening)

**Use the bug report template** when creating issues.

## 💡 Feature Requests

We welcome feature requests! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the feature** clearly and concisely
3. **Explain the use case** and benefits
4. **Consider implementation** if you have ideas

## 🏗️ Code Architecture

### Core Components

- **`core/analyzer.py`** - Main analysis engine
- **`core/error_detector.py`** - Error detection system
- **`core/documentation.py`** - Documentation generator
- **`app.py`** - FastAPI application
- **`models.py`** - Pydantic data models

### Adding New Features

#### Adding Language Support
1. Install tree-sitter language binding
2. Add to `self.languages` in `CodeAnalyzer.__init__()`
3. Implement extraction methods in `analyzer.py`
4. Add error patterns to `error_detector.py`
5. Update tests and documentation

#### Adding Error Detection
1. Add patterns to `common_patterns` in `ErrorDetector`
2. Implement detection method if needed
3. Add to `analyze_errors()` method
4. Write tests for new detection
5. Update documentation

## 📚 Documentation

- Keep README.md up to date
- Add docstrings to all public functions
- Update USAGE.md for new features
- Include examples in docstrings

### Docstring Format
```python
def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
    """Analyze code and return detailed results.
    
    Args:
        code: The source code to analyze
        language: Programming language (python, javascript, etc.)
        
    Returns:
        Dictionary containing analysis results including:
        - language: Detected/specified language
        - complexity: McCabe complexity score
        - functions: List of extracted functions
        - errors: List of detected issues
        
    Raises:
        ValueError: If language is not supported
        
    Example:
        >>> analyzer = CodeAnalyzer()
        >>> result = analyzer.analyze_code("def hello(): pass", "python")
        >>> result['language']
        'python'
    """
```

## 🔄 Release Process

1. **Version Bump** - Update version in relevant files
2. **Changelog** - Update CHANGELOG.md with new features/fixes
3. **Testing** - Ensure all tests pass
4. **Documentation** - Update docs if needed
5. **Tag Release** - Create git tag with version
6. **Release Notes** - Write detailed release notes

## 🌟 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Special recognition for significant contributions

## 📞 Questions?

- 
- 📧 **Email**: amandeepsasidharan@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/code-analyzer/issues)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
