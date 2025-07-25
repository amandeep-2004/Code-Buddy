import ast
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
import tree_sitter_java as tsjava
import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser, Node
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from .error_detector import ErrorDetector


@dataclass
class CodeElement:
    """Represents a code element (function, class, variable, etc.)"""
    name: str
    type: str  # 'function', 'class', 'variable', 'import', etc.
    description: str
    parameters: List[str] = None
    return_type: str = None
    complexity: int = 0
    line_start: int = 0
    line_end: int = 0
    docstring: str = None


class CodeAnalyzer:
    """Advanced code analyzer using tree-sitter and transformer models"""
    
    def __init__(self):
        # Initialize language parsers
        self.languages = {
            'python': Language(tspython.language()),
            'javascript': Language(tsjavascript.language()),
            'java': Language(tsjava.language()),
            'cpp': Language(tscpp.language()),
        }
        
        # Initialize transformer models for different tasks
        self.summarizer = None
        self.code_model = None
        self.tokenizer = None
        
        # Initialize error detector
        self.error_detector = ErrorDetector()
        
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize transformer models for code analysis"""
        try:
            # For code summarization - use a smaller, more reliable model
            self.summarizer = pipeline(
                "summarization", 
                model="facebook/bart-large-cnn",
                max_length=150,
                min_length=30,
                do_sample=False
            )
            print("✓ Summarization model loaded successfully")
            
        except Exception as e:
            print(f"Warning: Could not initialize summarization model: {e}")
            self.summarizer = None
            
        # Skip CodeBERT for now as it's complex to set up
        self.tokenizer = None
        self.code_model = None
        print("ℹ Code-specific models skipped for this demo")
    
    def detect_language(self, code: str, filename: str = None) -> str:
        """Detect programming language from code content or filename"""
        if filename:
            extension = filename.split('.')[-1].lower()
            extension_map = {
                'py': 'python',
                'js': 'javascript',
                'ts': 'javascript',  # TypeScript treated as JavaScript for now
                'java': 'java',
                'cpp': 'cpp',
                'cc': 'cpp',
                'cxx': 'cpp',
                'c': 'cpp'
            }
            if extension in extension_map:
                return extension_map[extension]
        
        # Fallback to content-based detection
        if 'def ' in code and 'import ' in code:
            return 'python'
        elif 'function ' in code or 'const ' in code or 'let ' in code:
            return 'javascript'
        elif 'public class ' in code or 'private ' in code:
            return 'java'
        elif '#include' in code or 'std::' in code:
            return 'cpp'
        
        return 'python'  # Default
    
    def parse_code(self, code: str, language: str) -> Node:
        """Parse code using tree-sitter"""
        if language not in self.languages:
            raise ValueError(f"Unsupported language: {language}")
        
        parser = Parser(self.languages[language])
        tree = parser.parse(bytes(code, "utf8"))
        return tree.root_node
    
    def extract_functions(self, node: Node, code_bytes: bytes, language: str) -> List[CodeElement]:
        """Extract function definitions from AST"""
        functions = []
        
        def traverse(node):
            if language == 'python' and node.type == 'function_definition':
                func_name = self._get_node_text(node.child_by_field_name('name'), code_bytes)
                parameters = self._extract_python_parameters(node, code_bytes)
                docstring = self._extract_python_docstring(node, code_bytes)
                
                functions.append(CodeElement(
                    name=func_name,
                    type='function',
                    description=f"Function: {func_name}",
                    parameters=parameters,
                    line_start=node.start_point[0] + 1,
                    line_end=node.end_point[0] + 1,
                    docstring=docstring
                ))
            
            elif language == 'javascript' and node.type == 'function_declaration':
                func_name = self._get_node_text(node.child_by_field_name('name'), code_bytes)
                parameters = self._extract_js_parameters(node, code_bytes)
                
                functions.append(CodeElement(
                    name=func_name,
                    type='function',
                    description=f"Function: {func_name}",
                    parameters=parameters,
                    line_start=node.start_point[0] + 1,
                    line_end=node.end_point[0] + 1
                ))
            
            for child in node.children:
                traverse(child)
        
        traverse(node)
        return functions
    
    def extract_classes(self, node: Node, code_bytes: bytes, language: str) -> List[CodeElement]:
        """Extract class definitions from AST"""
        classes = []
        
        def traverse(node):
            if language == 'python' and node.type == 'class_definition':
                class_name = self._get_node_text(node.child_by_field_name('name'), code_bytes)
                docstring = self._extract_python_docstring(node, code_bytes)
                
                classes.append(CodeElement(
                    name=class_name,
                    type='class',
                    description=f"Class: {class_name}",
                    line_start=node.start_point[0] + 1,
                    line_end=node.end_point[0] + 1,
                    docstring=docstring
                ))
            
            elif language == 'java' and node.type == 'class_declaration':
                class_name = self._get_node_text(node.child_by_field_name('name'), code_bytes)
                
                classes.append(CodeElement(
                    name=class_name,
                    type='class',
                    description=f"Class: {class_name}",
                    line_start=node.start_point[0] + 1,
                    line_end=node.end_point[0] + 1
                ))
            
            for child in node.children:
                traverse(child)
        
        traverse(node)
        return classes
    
    def _get_node_text(self, node: Node, code_bytes: bytes) -> str:
        """Get text content of a tree-sitter node"""
        if node is None:
            return ""
        return code_bytes[node.start_byte:node.end_byte].decode('utf8')
    
    def _extract_python_parameters(self, func_node: Node, code_bytes: bytes) -> List[str]:
        """Extract parameter names from Python function"""
        params = []
        parameters_node = func_node.child_by_field_name('parameters')
        if parameters_node:
            for child in parameters_node.children:
                if child.type == 'identifier':
                    params.append(self._get_node_text(child, code_bytes))
        return params
    
    def _extract_js_parameters(self, func_node: Node, code_bytes: bytes) -> List[str]:
        """Extract parameter names from JavaScript function"""
        params = []
        parameters_node = func_node.child_by_field_name('parameters')
        if parameters_node:
            for child in parameters_node.children:
                if child.type == 'identifier':
                    params.append(self._get_node_text(child, code_bytes))
        return params
    
    def _extract_python_docstring(self, node: Node, code_bytes: bytes) -> Optional[str]:
        """Extract docstring from Python function or class"""
        body = node.child_by_field_name('body')
        if body and body.children:
            first_stmt = body.children[0]
            if first_stmt.type == 'expression_statement':
                expr = first_stmt.children[0]
                if expr.type == 'string':
                    docstring = self._get_node_text(expr, code_bytes)
                    # Remove quotes
                    return docstring.strip('"""').strip("'''").strip('"').strip("'").strip()
        return None
    
    def calculate_complexity(self, node: Node) -> int:
        """Calculate cyclomatic complexity of code"""
        complexity = 1  # Base complexity
        
        def traverse(node):
            nonlocal complexity
            if node.type in ['if_statement', 'while_statement', 'for_statement', 
                           'try_statement', 'case_statement', 'conditional_expression']:
                complexity += 1
            
            for child in node.children:
                traverse(child)
        
        traverse(node)
        return complexity
    
    def generate_summary(self, code: str) -> str:
        """Generate a summary of the code using transformer model"""
        if not self.summarizer:
            return "Code analysis complete. Summary generation unavailable."
        
        try:
            # Truncate code if too long
            max_length = 1024
            if len(code) > max_length:
                code = code[:max_length] + "..."
            
            # Add context to help the model understand it's code
            prompt = f"This is a code snippet:\n{code}\n\nSummary:"
            
            result = self.summarizer(prompt, max_length=150, min_length=30, do_sample=False)
            return result[0]['summary_text']
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def analyze_code_file(self, code: str, filename: str = None) -> Dict[str, Any]:
        """Comprehensive analysis of a code file"""
        try:
            language = self.detect_language(code, filename)
            code_bytes = bytes(code, "utf8")
            root_node = self.parse_code(code, language)
            
            # Extract code elements
            functions = self.extract_functions(root_node, code_bytes, language)
            classes = self.extract_classes(root_node, code_bytes, language)
            
            # Calculate metrics
            complexity = self.calculate_complexity(root_node)
            line_count = len(code.split('\n'))
            
            # Generate summary
            summary = self.generate_summary(code)
            
            # Perform error analysis
            error_analysis = self.error_detector.analyze_errors(code, language, filename)
            
            return {
                'language': language,
                'line_count': line_count,
                'complexity': complexity,
                'functions': [
                    {
                        'name': f.name,
                        'type': f.type,
                        'parameters': f.parameters,
                        'line_start': f.line_start,
                        'line_end': f.line_end,
                        'docstring': f.docstring
                    } for f in functions
                ],
                'classes': [
                    {
                        'name': c.name,
                        'type': c.type,
                        'line_start': c.line_start,
                        'line_end': c.line_end,
                        'docstring': c.docstring
                    } for c in classes
                ],
                'summary': summary,
                'error_analysis': error_analysis,
                'quality_score': error_analysis['quality_score'],
                'has_errors': error_analysis['has_errors'],
                'filename': filename
            }
        
        except Exception as e:
            return {
                'error': f"Analysis failed: {str(e)}",
                'filename': filename
            }
    
    def comprehensive_analysis(self, code: str, filename: str = None, auto_fix: bool = False) -> Dict[str, Any]:
        """Perform comprehensive code analysis with error detection, suggestions, and optional auto-fixing"""
        try:
            # Basic code analysis
            basic_analysis = self.analyze_code_file(code, filename)
            
            if 'error' in basic_analysis:
                return basic_analysis
            
            language = basic_analysis['language']
            
            # Enhanced error analysis with suggestions and auto-fix
            comprehensive_result = self.error_detector.comprehensive_analysis(
                code, language, filename, auto_fix
            )
            
            # Merge results
            result = {
                **basic_analysis,
                'comprehensive_analysis': comprehensive_result,
                'improvements_available': len(comprehensive_result.get('improvements', {}).get('suggestions', [])) > 0,
                'auto_fix_available': comprehensive_result.get('auto_fix_available', False)
            }
            
            return result
            
        except Exception as e:
            return {
                'error': f"Comprehensive analysis failed: {str(e)}",
                'filename': filename
            }
    
    def fix_code_issues(self, code: str, filename: str = None) -> Dict[str, Any]:
        """Automatically fix detected code issues"""
        try:
            language = self.detect_language(code, filename)
            return self.error_detector.auto_fix_code(code, language)
        except Exception as e:
            return {
                'error': f"Auto-fix failed: {str(e)}",
                'filename': filename
            }
