import ast
import re
import sys
import subprocess
import tempfile
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
# Import external tools with fallback
try:
    import pylint.lint
    import pylint.reporters.text
    PYLINT_AVAILABLE = True
except ImportError:
    PYLINT_AVAILABLE = False

try:
    from flake8.api import legacy as flake8
    FLAKE8_AVAILABLE = True
except ImportError:
    FLAKE8_AVAILABLE = False


@dataclass
class CodeError:
    """Represents a code error or issue"""
    type: str  # 'syntax', 'logic', 'style', 'security', 'performance'
    severity: str  # 'error', 'warning', 'info'
    line: int
    column: int
    message: str
    rule_id: str = None
    suggestion: str = None
    auto_fix: str = None  # Automatic fix suggestion
    confidence: float = 0.0  # Confidence in the fix (0.0-1.0)


class ErrorDetector:
    """Advanced error detection and correction using multiple static analysis tools and ML models"""
    
    def __init__(self):
        self.common_patterns = {
            'python': {
                'security': [
                    (r'eval\s*\(', 'Avoid using eval() - security risk', 'ast.literal_eval() for safe evaluation', 0.9),
                    (r'exec\s*\(', 'Avoid using exec() - security risk', 'Use specific function calls instead of exec()', 0.8),
                    (r'input\s*\(', 'Be careful with input() - validate user input', 'Add input validation', 0.7),
                    (r'os\.system\s*\(', 'Avoid os.system() - use subprocess instead', 'subprocess.run() with shell=False', 0.9),
                    (r'pickle\.loads?\s*\(', 'Pickle can execute arbitrary code - security risk', 'Use json or safer serialization', 0.8),
                ],
                'performance': [
                    (r'\+\s*=.*\[.*\]', 'Consider list comprehension for better performance', 'Use list comprehension or extend()', 0.8),
                    (r'len\s*\([^)]*\)\s*==\s*0', 'Use "not list" instead of "len(list) == 0"', 'if not container:', 0.9),
                    (r'len\s*\([^)]*\)\s*>\s*0', 'Use "if list" instead of "len(list) > 0"', 'if container:', 0.9),
                    (r'range\s*\(\s*len\s*\([^)]*\)\s*\)', 'Use enumerate() instead of range(len())', 'for i, item in enumerate(container):', 0.8),
                ],
                'style': [
                    (r'==\s*True\b', 'Use "if condition:" instead of "if condition == True:"', 'if condition:', 0.9),
                    (r'==\s*False\b', 'Use "if not condition:" instead of "if condition == False:"', 'if not condition:', 0.9),
                    (r'!=\s*True\b', 'Use "if not condition:" instead of "if condition != True:"', 'if not condition:', 0.9),
                    (r'!=\s*False\b', 'Use "if condition:" instead of "if condition != False:"', 'if condition:', 0.9),
                ],
                'logic': [
                    (r'except\s*:', 'Bare except clause - specify exception types', 'except Exception as e:', 0.7),
                    (r'import \*', 'Avoid wildcard imports', 'Import specific names', 0.8),
                    (r'global\s+\w+', 'Avoid global variables when possible', 'Use function parameters or class attributes', 0.6),
                ]
            },
            'javascript': {
                'security': [
                    (r'eval\s*\(', 'Avoid using eval() - security risk', 'JSON.parse() for JSON or specific parsing', 0.8),
                    (r'innerHTML\s*=', 'Be careful with innerHTML - XSS risk', 'textContent or createElement()', 0.7),
                    (r'document\.write\s*\(', 'Avoid document.write() - use safer alternatives', 'appendChild() or innerHTML with sanitization', 0.8),
                    (r'setTimeout\s*\(\s*["\']', 'Avoid string-based setTimeout', 'Use function reference', 0.9),
                ],
                'style': [
                    (r'==\s*[^=]', 'Consider using === for strict equality', 'Use === instead of ==', 0.9),
                    (r'!=\s*[^=]', 'Consider using !== for strict inequality', 'Use !== instead of !=', 0.9),
                    (r'var\s+', 'Consider using let or const instead of var', 'let for variables, const for constants', 0.8),
                ],
                'logic': [
                    (r'console\.log\s*\(', 'Remove console.log in production', 'Use proper logging or remove', 0.6),
                    (r'alert\s*\(', 'Avoid alert() in production code', 'Use proper user notification', 0.7),
                ]
            }
        }
        
        # Automatic fixes for common patterns
        self.auto_fixes = {
            'python': {
                r'len\s*\(([^)]+)\)\s*==\s*0': r'not \1',
                r'len\s*\(([^)]+)\)\s*>\s*0': r'\1',
                r'==\s*True\b': r'',
                r'==\s*False\b': r'',
                r'!=\s*True\b': r'not ',
                r'!=\s*False\b': r'',
            },
            'javascript': {
                r'==\s*([^=])': r'=== \1',
                r'!=\s*([^=])': r'!== \1',
                r'var\s+': r'let ',
            }
        }
    
    def detect_syntax_errors(self, code: str, language: str) -> List[CodeError]:
        """Detect syntax errors in code"""
        errors = []
        
        if language == 'python':
            try:
                ast.parse(code)
            except SyntaxError as e:
                errors.append(CodeError(
                    type='syntax',
                    severity='error',
                    line=e.lineno or 1,
                    column=e.offset or 1,
                    message=str(e.msg),
                    rule_id='syntax_error',
                    suggestion='Fix the syntax error according to Python grammar rules'
                ))
            except Exception as e:
                errors.append(CodeError(
                    type='syntax',
                    severity='error',
                    line=1,
                    column=1,
                    message=f"Parse error: {str(e)}",
                    rule_id='parse_error'
                ))
        
        return errors
    
    def detect_style_issues(self, code: str, language: str) -> List[CodeError]:
        """Detect style and formatting issues using flake8"""
        errors = []
        
        if language != 'python':
            return errors
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Run flake8
            style_guide = flake8.get_style_guide()
            report = style_guide.check_files([temp_file])
            
            # Parse flake8 output
            for error in report.get_statistics('E'):
                parts = error.split(':')
                if len(parts) >= 4:
                    line_num = int(parts[1])
                    col_num = int(parts[2])
                    message = ':'.join(parts[3:]).strip()
                    
                    errors.append(CodeError(
                        type='style',
                        severity='warning',
                        line=line_num,
                        column=col_num,
                        message=message,
                        rule_id='flake8',
                        suggestion='Follow PEP 8 style guidelines'
                    ))
            
            # Clean up
            os.unlink(temp_file)
            
        except Exception as e:
            print(f"Style check failed: {e}")
        
        return errors
    
    def detect_pylint_issues(self, code: str, language: str) -> List[CodeError]:
        """Detect issues using pylint"""
        errors = []
        
        if language != 'python':
            return errors
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Capture pylint output
            from io import StringIO
            output = StringIO()
            
            # Run pylint with minimal configuration
            pylint_opts = [
                '--disable=import-error,missing-module-docstring',
                '--reports=no',
                '--score=no',
                temp_file
            ]
            
            try:
                pylint.lint.Run(pylint_opts, reporter=pylint.reporters.text.TextReporter(output), exit=False)
                
                # Parse pylint output
                for line in output.getvalue().split('\n'):
                    if ':' in line and ('error' in line or 'warning' in line):
                        try:
                            parts = line.split(':')
                            if len(parts) >= 3:
                                line_num = int(parts[1])
                                severity = 'error' if 'error' in line else 'warning'
                                message = ':'.join(parts[2:]).strip()
                                
                                errors.append(CodeError(
                                    type='logic',
                                    severity=severity,
                                    line=line_num,
                                    column=1,
                                    message=message,
                                    rule_id='pylint',
                                    suggestion='Review code logic and structure'
                                ))
                        except (ValueError, IndexError):
                            continue
            except SystemExit:
                pass  # Pylint calls sys.exit, ignore it
            
            # Clean up
            os.unlink(temp_file)
            
        except Exception as e:
            print(f"Pylint check failed: {e}")
        
        return errors
    
    def detect_pattern_issues(self, code: str, language: str) -> List[CodeError]:
        """Detect common anti-patterns and issues using regex patterns"""
        errors = []
        
        if language not in self.common_patterns:
            return errors
        
        patterns = self.common_patterns[language]
        lines = code.split('\n')
        
        for category, pattern_list in patterns.items():
            for item in pattern_list:
                if len(item) >= 4:  # New format with auto-fix and confidence
                    pattern, message, auto_fix, confidence = item
                else:  # Old format for backward compatibility
                    pattern, message = item[:2]
                    auto_fix, confidence = None, 0.0
                
                for line_num, line in enumerate(lines, 1):
                    match = re.search(pattern, line)
                    if match:
                        severity = 'error' if category == 'security' else 'warning'
                        
                        # Generate automatic fix if available
                        generated_fix = None
                        if language in self.auto_fixes and pattern in self.auto_fixes[language]:
                            try:
                                generated_fix = re.sub(pattern, self.auto_fixes[language][pattern], line)
                            except:
                                generated_fix = None
                        
                        errors.append(CodeError(
                            type=category,
                            severity=severity,
                            line=line_num,
                            column=match.start() + 1,
                            message=message,
                            rule_id=f'pattern_{category}',
                            suggestion=self._get_suggestion(category, pattern),
                            auto_fix=auto_fix or generated_fix,
                            confidence=confidence
                        ))
        
        return errors
    
    def detect_complexity_issues(self, code: str, language: str) -> List[CodeError]:
        """Detect complexity-related issues"""
        errors = []
        
        if language != 'python':
            return errors
        
        try:
            tree = ast.parse(code)
            
            class ComplexityVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.complexity_issues = []
                
                def visit_FunctionDef(self, node):
                    # Count complexity indicators
                    complexity = 1  # Base complexity
                    
                    for child in ast.walk(node):
                        if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                            complexity += 1
                        elif isinstance(child, ast.BoolOp):
                            complexity += len(child.values) - 1
                    
                    if complexity > 10:  # McCabe complexity threshold
                        self.complexity_issues.append(CodeError(
                            type='complexity',
                            severity='warning',
                            line=node.lineno,
                            column=node.col_offset,
                            message=f"Function '{node.name}' has high complexity ({complexity})",
                            rule_id='high_complexity',
                            suggestion='Consider breaking this function into smaller functions'
                        ))
                    
                    self.generic_visit(node)
            
            visitor = ComplexityVisitor()
            visitor.visit(tree)
            errors.extend(visitor.complexity_issues)
            
        except Exception as e:
            print(f"Complexity analysis failed: {e}")
        
        return errors
    
    def detect_unused_variables(self, code: str, language: str) -> List[CodeError]:
        """Detect unused variables"""
        errors = []
        
        if language != 'python':
            return errors
        
        try:
            tree = ast.parse(code)
            
            class UnusedVariableVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.defined_vars = set()
                    self.used_vars = set()
                    self.var_lines = {}
                    self.unused_issues = []
                
                def visit_Name(self, node):
                    if isinstance(node.ctx, ast.Store):
                        self.defined_vars.add(node.id)
                        self.var_lines[node.id] = node.lineno
                    elif isinstance(node.ctx, ast.Load):
                        self.used_vars.add(node.id)
                    self.generic_visit(node)
                
                def visit_FunctionDef(self, node):
                    # Save current state
                    old_defined = self.defined_vars.copy()
                    old_used = self.used_vars.copy()
                    old_lines = self.var_lines.copy()
                    
                    # Add function parameters
                    for arg in node.args.args:
                        self.defined_vars.add(arg.arg)
                        self.var_lines[arg.arg] = node.lineno
                    
                    self.generic_visit(node)
                    
                    # Check for unused variables in this function
                    unused = self.defined_vars - self.used_vars
                    for var in unused:
                        if not var.startswith('_'):  # Ignore variables starting with _
                            self.unused_issues.append(CodeError(
                                type='logic',
                                severity='warning',
                                line=self.var_lines.get(var, node.lineno),
                                column=1,
                                message=f"Unused variable '{var}'",
                                rule_id='unused_variable',
                                suggestion=f"Remove unused variable '{var}' or prefix with '_' if intentional"
                            ))
                    
                    # Restore state
                    self.defined_vars = old_defined
                    self.used_vars = old_used
                    self.var_lines = old_lines
            
            visitor = UnusedVariableVisitor()
            visitor.visit(tree)
            errors.extend(visitor.unused_issues)
            
        except Exception as e:
            print(f"Unused variable analysis failed: {e}")
        
        return errors
    
    def _get_suggestion(self, category: str, pattern: str) -> str:
        """Get suggestion based on error category and pattern"""
        suggestions = {
            'security': 'Review security implications and use safer alternatives',
            'performance': 'Consider optimizing for better performance',
            'logic': 'Review logic and consider best practices',
            'style': 'Follow language style guidelines'
        }
        return suggestions.get(category, 'Review and fix this issue')
    
    def analyze_errors(self, code: str, language: str, filename: str = None) -> Dict[str, Any]:
        """Comprehensive error analysis"""
        all_errors = []
        
        # Run all error detection methods
        all_errors.extend(self.detect_syntax_errors(code, language))
        all_errors.extend(self.detect_pattern_issues(code, language))
        all_errors.extend(self.detect_complexity_issues(code, language))
        all_errors.extend(self.detect_unused_variables(code, language))
        
        # Only run external tools for Python if available
        if language == 'python':
            if FLAKE8_AVAILABLE:
                try:
                    all_errors.extend(self.detect_style_issues(code, language))
                except Exception as e:
                    print(f"Style analysis skipped: {e}")
            
            if PYLINT_AVAILABLE:
                try:
                    all_errors.extend(self.detect_pylint_issues(code, language))
                except Exception as e:
                    print(f"Pylint analysis skipped: {e}")
        
        # Group errors by type and severity
        error_summary = {
            'total_errors': len([e for e in all_errors if e.severity == 'error']),
            'total_warnings': len([e for e in all_errors if e.severity == 'warning']),
            'total_info': len([e for e in all_errors if e.severity == 'info']),
            'errors_by_type': {},
            'errors_by_line': {}
        }
        
        for error in all_errors:
            # Group by type
            if error.type not in error_summary['errors_by_type']:
                error_summary['errors_by_type'][error.type] = []
            error_summary['errors_by_type'][error.type].append({
                'severity': error.severity,
                'line': error.line,
                'column': error.column,
                'message': error.message,
                'rule_id': error.rule_id,
                'suggestion': error.suggestion
            })
            
            # Group by line
            if error.line not in error_summary['errors_by_line']:
                error_summary['errors_by_line'][error.line] = []
            error_summary['errors_by_line'][error.line].append({
                'type': error.type,
                'severity': error.severity,
                'column': error.column,
                'message': error.message,
                'rule_id': error.rule_id,
                'suggestion': error.suggestion
            })
        
        return {
            'filename': filename,
            'language': language,
            'error_summary': error_summary,
            'has_errors': error_summary['total_errors'] > 0,
            'has_issues': len(all_errors) > 0,
            'quality_score': self._calculate_quality_score(error_summary, len(code.split('\n')))
        }
    
    def _calculate_quality_score(self, error_summary: Dict, line_count: int) -> float:
        """Calculate a code quality score (0-100)"""
        total_issues = (
            error_summary['total_errors'] * 3 +  # Errors are weighted more
            error_summary['total_warnings'] * 2 +
            error_summary['total_info'] * 1
        )
        
        # Normalize by lines of code
        if line_count == 0:
            return 100.0
        
        issues_per_line = total_issues / line_count
        
        # Calculate score (100 is perfect, decreases with more issues)
        score = max(0, 100 - (issues_per_line * 50))
        return round(score, 1)
    
    def auto_fix_code(self, code: str, language: str, errors: List[CodeError] = None) -> Dict[str, Any]:
        """Automatically fix common code issues"""
        if errors is None:
            # Analyze code to find errors first
            analysis = self.analyze_errors(code, language)
            errors = self._extract_errors_from_analysis(analysis)
        
        fixed_code = code
        fixes_applied = []
        fixes_skipped = []
        
        # Sort errors by line number (descending) to avoid line number shifts
        fixable_errors = [e for e in errors if e.auto_fix and e.confidence > 0.5]
        fixable_errors.sort(key=lambda x: x.line, reverse=True)
        
        lines = fixed_code.split('\n')
        
        for error in fixable_errors:
            try:
                if error.line <= len(lines):
                    line_idx = error.line - 1
                    original_line = lines[line_idx]
                    
                    # Apply regex-based fixes
                    if language in self.auto_fixes:
                        for pattern, replacement in self.auto_fixes[language].items():
                            if re.search(pattern, original_line):
                                fixed_line = re.sub(pattern, replacement, original_line)
                                if fixed_line != original_line:
                                    lines[line_idx] = fixed_line
                                    fixes_applied.append({
                                        'line': error.line,
                                        'original': original_line.strip(),
                                        'fixed': fixed_line.strip(),
                                        'rule_id': error.rule_id,
                                        'confidence': error.confidence,
                                        'message': error.message
                                    })
                                    break
                    
                    # Apply specific auto-fixes from error detection
                    elif hasattr(error, 'auto_fix') and error.auto_fix:
                        # This would need more sophisticated parsing for complex fixes
                        pass
            
            except Exception as e:
                fixes_skipped.append({
                    'line': error.line,
                    'error': str(e),
                    'rule_id': error.rule_id,
                    'message': error.message
                })
        
        fixed_code = '\n'.join(lines)
        
        return {
            'original_code': code,
            'fixed_code': fixed_code,
            'fixes_applied': fixes_applied,
            'fixes_skipped': fixes_skipped,
            'total_fixes': len(fixes_applied),
            'language': language
        }
    
    def suggest_improvements(self, code: str, language: str) -> Dict[str, Any]:
        """Suggest code improvements beyond just fixing errors"""
        suggestions = []
        
        if language == 'python':
            # Check for common Python improvements
            lines = code.split('\n')
            
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # Suggest f-strings instead of format()
                if '.format(' in line_stripped:
                    suggestions.append({
                        'line': i,
                        'type': 'modernization',
                        'message': 'Consider using f-strings instead of .format()',
                        'suggestion': 'Use f"text {variable}" instead of "text {}".format(variable)',
                        'confidence': 0.8
                    })
                
                # Suggest pathlib instead of os.path
                if 'os.path.' in line_stripped:
                    suggestions.append({
                        'line': i,
                        'type': 'modernization',
                        'message': 'Consider using pathlib instead of os.path',
                        'suggestion': 'from pathlib import Path; Path(filename).exists()',
                        'confidence': 0.7
                    })
                
                # Suggest type hints
                if line_stripped.startswith('def ') and '->' not in line_stripped:
                    suggestions.append({
                        'line': i,
                        'type': 'typing',
                        'message': 'Consider adding type hints',
                        'suggestion': 'def function_name(param: type) -> return_type:',
                        'confidence': 0.6
                    })
        
        elif language == 'javascript':
            lines = code.split('\n')
            
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # Suggest arrow functions
                if line_stripped.startswith('function(') and '=>' not in line_stripped:
                    suggestions.append({
                        'line': i,
                        'type': 'modernization',
                        'message': 'Consider using arrow functions',
                        'suggestion': '(params) => { ... }',
                        'confidence': 0.7
                    })
                
                # Suggest const/let instead of var
                if line_stripped.startswith('var '):
                    suggestions.append({
                        'line': i,
                        'type': 'modernization',
                        'message': 'Use const or let instead of var',
                        'suggestion': 'const for constants, let for variables',
                        'confidence': 0.9
                    })
        
        return {
            'language': language,
            'suggestions': suggestions,
            'total_suggestions': len(suggestions)
        }
    
    def _extract_errors_from_analysis(self, analysis: Dict[str, Any]) -> List[CodeError]:
        """Extract CodeError objects from analysis results"""
        errors = []
        
        if 'error_summary' in analysis:
            for error_type, error_list in analysis['error_summary'].get('errors_by_type', {}).items():
                for error_data in error_list:
                    errors.append(CodeError(
                        type=error_type,
                        severity=error_data.get('severity', 'warning'),
                        line=error_data.get('line', 1),
                        column=error_data.get('column', 1),
                        message=error_data.get('message', ''),
                        rule_id=error_data.get('rule_id'),
                        suggestion=error_data.get('suggestion')
                    ))
        
        return errors
    
    def comprehensive_analysis(self, code: str, language: str, filename: str = None, auto_fix: bool = False) -> Dict[str, Any]:
        """Perform comprehensive code analysis with optional auto-fixing"""
        # Basic error analysis
        error_analysis = self.analyze_errors(code, language, filename)
        
        # Improvement suggestions
        improvements = self.suggest_improvements(code, language)
        
        result = {
            'filename': filename,
            'language': language,
            'error_analysis': error_analysis,
            'improvements': improvements,
            'auto_fix_available': False
        }
        
        # Auto-fix if requested
        if auto_fix:
            errors = self._extract_errors_from_analysis(error_analysis)
            fix_results = self.auto_fix_code(code, language, errors)
            result['auto_fix'] = fix_results
            result['auto_fix_available'] = len(fix_results['fixes_applied']) > 0
        
        return result
