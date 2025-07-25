#!/usr/bin/env python3
"""
Test script to demonstrate the Code Analysis and Documentation Generator
"""

from core.analyzer import CodeAnalyzer

# Sample Python code to analyze
sample_code = '''
def fibonacci(n):
    """
    Calculate the nth Fibonacci number using recursion.
    
    Args:
        n (int): The position in the Fibonacci sequence
        
    Returns:
        int: The nth Fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    """A simple calculator class for basic arithmetic operations."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        """Add two numbers and store in history."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def multiply(self, a, b):
        """Multiply two numbers and store in history."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

def main():
    calc = Calculator()
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"Fibonacci(10) = {fibonacci(10)}")

if __name__ == "__main__":
    main()
'''

def test_analyzer():
    print("🚀 Testing Code Analysis and Documentation Generator")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = CodeAnalyzer()
    
    # Analyze the sample code
    result = analyzer.analyze_code_file(sample_code, "sample.py")
    
    # Display results
    print(f"📁 File: {result.get('filename', 'sample.py')}")
    print(f"🔤 Language: {result['language']}")
    print(f"📊 Lines of Code: {result['line_count']}")
    print(f"🔄 Complexity: {result['complexity']}")
    print()
    
    print("🔧 Functions Found:")
    for func in result['functions']:
        print(f"  • {func['name']}() - Lines {func['line_start']}-{func['line_end']}")
        if func['parameters']:
            print(f"    Parameters: {', '.join(func['parameters'])}")
        if func['docstring']:
            print(f"    Doc: {func['docstring'][:100]}...")
        print()
    
    print("🏗️ Classes Found:")
    for cls in result['classes']:
        print(f"  • {cls['name']} - Lines {cls['line_start']}-{cls['line_end']}")
        if cls['docstring']:
            print(f"    Doc: {cls['docstring']}")
        print()
    
    print("📝 Summary:")
    print(f"  {result['summary']}")
    print()
    
    print("✅ Analysis completed successfully!")

if __name__ == "__main__":
    test_analyzer()
