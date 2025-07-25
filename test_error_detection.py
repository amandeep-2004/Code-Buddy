#!/usr/bin/env python3
"""
Test script to demonstrate the Error Detection capabilities
"""

from core.analyzer import CodeAnalyzer

# Sample Python code with various errors and issues
problematic_code = '''
# This code has multiple issues for demonstration

import os
import sys

def bad_function(x, y):
    # Syntax error on next line (missing closing parenthesis)
    # result = x + y + (1
    
    # Security issue - using eval
    dangerous = eval("x + y")
    
    # Performance issue - inefficient loop
    numbers = []
    for i in range(100):
        numbers.append(i * 2)
    
    # Logic issues
    if x == True:  # Should use 'if x:'
        print("x is true")
    
    if len(numbers) == 0:  # Should use 'if not numbers:'
        print("empty list")
    
    # Unused variable
    unused_var = "I'm not used anywhere"
    
    # Bare except clause
    try:
        result = x / y
    except:
        result = 0
    
    # System call security risk
    os.system("ls -la")
    
    return dangerous

# High complexity function
def complex_function(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        for i in range(10):
                            for j in range(10):
                                if i + j > 5:
                                    if i * j > 10:
                                        if a + b + c > 20:
                                            return True
    return False

class TestClass:
    def __init__(self):
        self.value = 0
    
    def method_with_issues(self):
        # More performance issues
        data = []
        for item in range(1000):
            data.append(item)  # Should use list comprehension
        
        # JavaScript-like equality (if this were JS)
        if self.value == True:
            return data
'''

# JavaScript code with issues
js_code_with_issues = '''
function badFunction(x, y) {
    // Security issues
    eval("console.log('This is dangerous')");
    document.write("<p>XSS risk</p>");
    
    // Logic issues
    if (x == y) {  // Should use === for strict equality
        console.log("Equal");
    }
    
    var oldStyle = "should use let or const";  // Deprecated var usage
    
    // Potential XSS
    element.innerHTML = userInput;
    
    return x + y;
}
'''

def test_error_detection():
    print("🚨 Testing Advanced Error Detection System")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = CodeAnalyzer()
    
    print("\n📋 Testing Python Code with Multiple Issues:")
    print("-" * 50)
    
    # Analyze the problematic Python code
    result = analyzer.analyze_code_file(problematic_code, "bad_code.py")
    
    if 'error_analysis' in result:
        error_data = result['error_analysis']
        
        print(f"📁 File: {error_data['filename']}")
        print(f"🔤 Language: {error_data['language']}")
        print(f"⭐ Quality Score: {error_data['quality_score']}/100")
        print(f"❌ Has Errors: {error_data['has_errors']}")
        print(f"⚠️  Has Issues: {error_data['has_issues']}")
        print()
        
        summary = error_data['error_summary']
        print("📊 Error Summary:")
        print(f"  🔴 Errors: {summary['total_errors']}")
        print(f"  🟡 Warnings: {summary['total_warnings']}")
        print(f"  🔵 Info: {summary['total_info']}")
        print()
        
        print("🔍 Issues by Type:")
        for error_type, issues in summary['errors_by_type'].items():
            print(f"\n  📂 {error_type.upper()} ({len(issues)} issues):")
            for issue in issues[:3]:  # Show first 3 issues of each type
                print(f"    • Line {issue['line']}: {issue['message']}")
                if issue['suggestion']:
                    print(f"      💡 Suggestion: {issue['suggestion']}")
            if len(issues) > 3:
                print(f"    ... and {len(issues) - 3} more {error_type} issues")
        
        print("\n🎯 Issues by Line (first 10 lines with issues):")
        sorted_lines = sorted(summary['errors_by_line'].items())[:10]
        for line_num, line_issues in sorted_lines:
            print(f"\n  📍 Line {line_num}:")
            for issue in line_issues:
                severity_icon = "🔴" if issue['severity'] == 'error' else "🟡" if issue['severity'] == 'warning' else "🔵"
                print(f"    {severity_icon} [{issue['type']}] {issue['message']}")
    
    print("\n" + "=" * 60)
    print("\n📋 Testing JavaScript Code with Issues:")
    print("-" * 50)
    
    # Analyze JavaScript code
    js_result = analyzer.analyze_code_file(js_code_with_issues, "bad_code.js")
    
    if 'error_analysis' in js_result:
        js_error_data = js_result['error_analysis']
        
        print(f"📁 File: {js_error_data['filename']}")
        print(f"🔤 Language: {js_error_data['language']}")
        print(f"⭐ Quality Score: {js_error_data['quality_score']}/100")
        print()
        
        js_summary = js_error_data['error_summary']
        print("📊 JavaScript Issues:")
        for error_type, issues in js_summary['errors_by_type'].items():
            print(f"\n  📂 {error_type.upper()} ({len(issues)} issues):")
            for issue in issues:
                print(f"    • Line {issue['line']}: {issue['message']}")
    
    print("\n" + "=" * 60)
    print("✅ Error Detection Testing Complete!")
    print("\n🔧 The system can detect:")
    print("  • Syntax errors (Python AST parsing)")
    print("  • Security vulnerabilities (eval, os.system, XSS risks)")
    print("  • Performance anti-patterns (inefficient loops)")
    print("  • Logic issues (equality comparisons, bare except)")
    print("  • Code complexity (McCabe complexity)")
    print("  • Unused variables")
    print("  • Style violations (via Pylint & Flake8)")
    print("  • Language-specific best practices")

if __name__ == "__main__":
    test_error_detection()
