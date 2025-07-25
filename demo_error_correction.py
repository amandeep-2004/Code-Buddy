#!/usr/bin/env python3
"""
Demo script to showcase the enhanced error detection and correction features
"""

import sys
import os
sys.path.append('.')

from core.analyzer import CodeAnalyzer
from core.error_detector import ErrorDetector
import json

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n{'-'*40}")
    print(f"  {title}")
    print(f"{'-'*40}")

def demo_error_detection():
    """Demonstrate error detection capabilities"""
    print_section("ERROR DETECTION DEMO")
    
    # Sample code with various issues
    sample_code = '''
import os
import sys

def bad_function(data):
    # Security issues
    result = eval(data)
    os.system("ls -la")
    
    # Performance issues
    items = []
    for i in range(len(data)):
        items.append(data[i])
    
    # Style issues
    if len(items) == 0:
        return None
    if result == True:
        print("Success")
    
    # Logic issues
    try:
        process_data()
    except:
        pass
    
    unused_var = "This won't be used"
    
    return result

def complex_function(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        for i in range(10):
                            if i % 2 == 0:
                                for j in range(5):
                                    if j > 2:
                                        print("Complex nested logic")
    return True
'''
    
    analyzer = CodeAnalyzer()
    
    print("Analyzing code with multiple issues...")
    analysis = analyzer.comprehensive_analysis(sample_code, "demo.py", auto_fix=False)
    
    if 'error' in analysis:
        print(f"Analysis failed: {analysis['error']}")
        return
    
    # Display basic metrics
    print_subsection("Basic Metrics")
    print(f"Language: {analysis['language']}")
    print(f"Lines of Code: {analysis['line_count']}")
    print(f"Complexity: {analysis['complexity']}")
    print(f"Quality Score: {analysis['quality_score']}/100")
    print(f"Has Errors: {analysis['has_errors']}")
    
    # Display error analysis
    print_subsection("Error Analysis")
    error_summary = analysis['error_analysis']['error_summary']
    print(f"Total Errors: {error_summary['total_errors']}")
    print(f"Total Warnings: {error_summary['total_warnings']}")
    
    print("\nErrors by Type:")
    for error_type, errors in error_summary['errors_by_type'].items():
        print(f"  {error_type.upper()}: {len(errors)} issues")
        for i, error in enumerate(errors[:3]):  # Show first 3 errors
            print(f"    {i+1}. Line {error['line']}: {error['message']}")
            if error.get('suggestion'):
                print(f"       Suggestion: {error['suggestion']}")
    
    # Display improvement suggestions
    comprehensive = analysis.get('comprehensive_analysis', {})
    improvements = comprehensive.get('improvements', {})
    if improvements.get('suggestions'):
        print_subsection("Improvement Suggestions")
        for suggestion in improvements['suggestions'][:5]:  # Show first 5
            print(f"Line {suggestion['line']} ({suggestion['type']}): {suggestion['message']}")
            print(f"  Suggestion: {suggestion['suggestion']}")
            print(f"  Confidence: {suggestion['confidence']:.1%}")

def demo_auto_fix():
    """Demonstrate automatic error correction"""
    print_section("AUTO-FIX DEMO")
    
    # Sample code with fixable issues
    fixable_code = '''
def example_function(data):
    # These issues can be automatically fixed
    if len(data) == 0:
        return False
    
    if len(data) > 0:
        print("Data available")
    
    if result == True:
        return "success"
    
    if status != False:
        process_data()
    
    return True
'''
    
    analyzer = CodeAnalyzer()
    
    print("Original code:")
    print(fixable_code)
    
    print_subsection("Auto-fixing Issues")
    
    # Perform auto-fix
    fix_result = analyzer.fix_code_issues(fixable_code, "fixable.py")
    
    if 'error' in fix_result:
        print(f"Auto-fix failed: {fix_result['error']}")
        return
    
    print(f"Total fixes applied: {fix_result['total_fixes']}")
    
    if fix_result['fixes_applied']:
        print("\nFixes Applied:")
        for fix in fix_result['fixes_applied']:
            print(f"  Line {fix['line']}:")
            print(f"    Original: {fix['original']}")
            print(f"    Fixed:    {fix['fixed']}")
            print(f"    Rule:     {fix['rule_id']}")
            print(f"    Confidence: {fix['confidence']:.1%}")
    
    if fix_result['fixes_skipped']:
        print(f"\nFixes skipped: {len(fix_result['fixes_skipped'])}")
    
    print_subsection("Fixed Code")
    print(fix_result['fixed_code'])

def demo_comprehensive_analysis():
    """Demonstrate comprehensive analysis with auto-fix"""
    print_section("COMPREHENSIVE ANALYSIS WITH AUTO-FIX")
    
    # Sample JavaScript code with issues
    js_code = '''
function processData(data) {
    var result = null;
    var status = "pending";
    
    if (data == null) {
        return false;
    }
    
    if (status == "ready") {
        console.log("Processing data");
        result = data.map(function(item) {
            return item * 2;
        });
    }
    
    if (result != null) {
        alert("Processing complete!");
        return result;
    }
    
    return false;
}
'''
    
    analyzer = CodeAnalyzer()
    
    print("Analyzing JavaScript code with auto-fix enabled...")
    analysis = analyzer.comprehensive_analysis(js_code, "demo.js", auto_fix=True)
    
    if 'error' in analysis:
        print(f"Analysis failed: {analysis['error']}")
        return
    
    print_subsection("Analysis Results")
    print(f"Language: {analysis['language']}")
    print(f"Quality Score: {analysis['quality_score']}/100")
    print(f"Improvements Available: {analysis['improvements_available']}")
    print(f"Auto-fix Available: {analysis['auto_fix_available']}")
    
    # Show comprehensive analysis details
    comprehensive = analysis.get('comprehensive_analysis', {})
    
    if comprehensive.get('auto_fix'):
        auto_fix = comprehensive['auto_fix']
        print_subsection("Auto-fix Results")
        print(f"Fixes applied: {auto_fix['total_fixes']}")
        
        if auto_fix['fixes_applied']:
            print("\nFixed Issues:")
            for fix in auto_fix['fixes_applied']:
                print(f"  Line {fix['line']}: {fix['message']}")
                print(f"    {fix['original']} → {fix['fixed']}")

def demo_pattern_detection():
    """Demonstrate advanced pattern detection"""
    print_section("ADVANCED PATTERN DETECTION")
    
    security_code = '''
import pickle
import subprocess

def unsafe_operations(user_input):
    # Security risks
    data = eval(user_input)
    result = exec(user_input)
    file_data = pickle.loads(user_input)
    
    # Command injection risk
    subprocess.call(f"ls {user_input}", shell=True)
    
    return data
'''
    
    detector = ErrorDetector()
    
    print("Analyzing code for security vulnerabilities...")
    analysis = detector.analyze_errors(security_code, 'python', 'security_demo.py')
    
    print_subsection("Security Issues Detected")
    security_errors = analysis['error_summary']['errors_by_type'].get('security', [])
    
    for i, error in enumerate(security_errors, 1):
        print(f"{i}. Line {error['line']}: {error['message']}")
        print(f"   Suggestion: {error['suggestion']}")

def main():
    """Run all demos"""
    print("🔍 Enhanced Error Detection and Correction Demo")
    print("=" * 60)
    
    try:
        demo_error_detection()
        demo_auto_fix()
        demo_comprehensive_analysis()
        demo_pattern_detection()
        
        print_section("DEMO COMPLETE")
        print("✅ All error detection and correction features demonstrated successfully!")
        print("\nKey Features Shown:")
        print("• Multi-language error detection (Python, JavaScript)")
        print("• Security vulnerability detection")
        print("• Performance issue identification")
        print("• Code style and logic problems")
        print("• Automatic error correction")
        print("• Improvement suggestions")
        print("• Comprehensive code quality scoring")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
