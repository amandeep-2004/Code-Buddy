#!/usr/bin/env python3
"""
Code Analyzer - Advanced Code Analysis and Documentation Pipeline
================================================================

A comprehensive tool for analyzing, documenting, and improving code quality.

Features:
- Multi-language code analysis (Python, JavaScript, Java, C++)
- Error detection and automatic correction
- Security vulnerability scanning
- Performance optimization suggestions
- Code documentation generation
- Quality scoring and metrics
- Interactive CLI interface

Author: Your Name
Version: 1.0.0
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import time

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.analyzer import CodeAnalyzer
from core.error_detector import ErrorDetector
from core.documentation import DocumentationGenerator

class CodeAnalysisPipeline:
    """Unified pipeline for comprehensive code analysis"""
    
    def __init__(self):
        """Initialize the analysis pipeline"""
        print("🚀 Initializing Code Analysis Pipeline...")
        self.analyzer = CodeAnalyzer()
        self.error_detector = ErrorDetector()
        self.doc_generator = DocumentationGenerator()
        print("✅ Pipeline initialized successfully!\n")
    
    def analyze_single_file(self, file_path: str, output_dir: str = None, 
                          auto_fix: bool = False, generate_docs: bool = True) -> Dict[str, Any]:
        """
        Analyze a single code file with full pipeline
        
        Args:
            file_path: Path to the code file
            output_dir: Directory to save output files
            auto_fix: Whether to automatically fix issues
            generate_docs: Whether to generate documentation
            
        Returns:
            Complete analysis results
        """
        print(f"📁 Analyzing file: {file_path}")
        
        if not os.path.exists(file_path):
            return {'error': f'File not found: {file_path}'}
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # Perform comprehensive analysis
            start_time = time.time()
            analysis_results = self.analyzer.comprehensive_analysis(
                code_content, file_path, auto_fix=auto_fix
            )
            analysis_time = time.time() - start_time
            
            # Add timing information
            analysis_results['analysis_time'] = round(analysis_time, 2)
            analysis_results['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Generate documentation if requested
            if generate_docs and output_dir:
                self._generate_documentation(analysis_results, output_dir, file_path)
            
            # Save auto-fix results if available
            if auto_fix and analysis_results.get('comprehensive_analysis', {}).get('auto_fix'):
                self._save_fixed_code(analysis_results, output_dir, file_path)
            
            # Print summary
            self._print_analysis_summary(analysis_results, file_path)
            
            return analysis_results
            
        except Exception as e:
            error_msg = f"Analysis failed for {file_path}: {str(e)}"
            print(f"❌ {error_msg}")
            return {'error': error_msg, 'file_path': file_path}
    
    def analyze_directory(self, directory_path: str, output_dir: str = None,
                         auto_fix: bool = False, generate_docs: bool = True,
                         file_extensions: List[str] = None) -> Dict[str, Any]:
        """
        Analyze all code files in a directory
        
        Args:
            directory_path: Path to the directory
            output_dir: Directory to save output files
            auto_fix: Whether to automatically fix issues
            generate_docs: Whether to generate documentation
            file_extensions: List of file extensions to analyze
            
        Returns:
            Combined analysis results for all files
        """
        print(f"📂 Analyzing directory: {directory_path}")
        
        if not os.path.exists(directory_path):
            return {'error': f'Directory not found: {directory_path}'}
        
        if file_extensions is None:
            file_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cc', '.cxx']
        
        results = {
            'directory': directory_path,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'files_analyzed': [],
            'summary': {
                'total_files': 0,
                'successful_analyses': 0,
                'failed_analyses': 0,
                'total_errors': 0,
                'total_warnings': 0,
                'average_quality_score': 0,
                'files_with_auto_fixes': 0
            }
        }
        
        # Find all code files
        code_files = []
        for root, dirs, files in os.walk(directory_path):
            # Skip virtual environment and other common directories
            dirs[:] = [d for d in dirs if d not in ['venv', '.venv', 'env', '.env', 
                                                  'node_modules', '.git', '__pycache__']]
            
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    code_files.append(os.path.join(root, file))
        
        print(f"Found {len(code_files)} code files to analyze")
        
        # Analyze each file
        quality_scores = []
        for file_path in code_files:
            print(f"\n📄 Processing: {os.path.relpath(file_path, directory_path)}")
            
            file_result = self.analyze_single_file(
                file_path, output_dir, auto_fix, generate_docs
            )
            
            results['files_analyzed'].append(file_result)
            results['summary']['total_files'] += 1
            
            if 'error' in file_result:
                results['summary']['failed_analyses'] += 1
            else:
                results['summary']['successful_analyses'] += 1
                
                # Collect metrics
                error_summary = file_result.get('error_analysis', {}).get('error_summary', {})
                results['summary']['total_errors'] += error_summary.get('total_errors', 0)
                results['summary']['total_warnings'] += error_summary.get('total_warnings', 0)
                
                quality_score = file_result.get('quality_score', 0)
                if quality_score > 0:
                    quality_scores.append(quality_score)
                
                # Check for auto-fixes
                comprehensive = file_result.get('comprehensive_analysis', {})
                if comprehensive.get('auto_fix_available'):
                    results['summary']['files_with_auto_fixes'] += 1
        
        # Calculate average quality score
        if quality_scores:
            results['summary']['average_quality_score'] = round(
                sum(quality_scores) / len(quality_scores), 1
            )
        
        # Generate combined report
        if output_dir:
            self._generate_directory_report(results, output_dir)
        
        # Print directory summary
        self._print_directory_summary(results)
        
        return results
    
    def _generate_documentation(self, analysis_results: Dict[str, Any], 
                              output_dir: str, file_path: str):
        """Generate documentation files"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.basename(file_path)
            base_name = os.path.splitext(filename)[0]
            
            # Generate different documentation formats
            formats = ['markdown', 'html', 'json']
            
            for fmt in formats:
                doc_content = self.doc_generator.generate_documentation(analysis_results, fmt)
                
                if fmt == 'markdown':
                    doc_path = os.path.join(output_dir, f"{base_name}_analysis.md")
                elif fmt == 'html':
                    doc_path = os.path.join(output_dir, f"{base_name}_analysis.html")
                else:  # json
                    doc_path = os.path.join(output_dir, f"{base_name}_analysis.json")
                
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(doc_content)
                
                print(f"📝 Generated {fmt.upper()} documentation: {doc_path}")
            
        except Exception as e:
            print(f"⚠️  Documentation generation failed: {e}")
    
    def _save_fixed_code(self, analysis_results: Dict[str, Any], 
                        output_dir: str, file_path: str):
        """Save auto-fixed code to a new file"""
        try:
            comprehensive = analysis_results.get('comprehensive_analysis', {})
            auto_fix = comprehensive.get('auto_fix', {})
            
            if auto_fix.get('fixes_applied'):
                os.makedirs(output_dir, exist_ok=True)
                filename = os.path.basename(file_path)
                base_name, ext = os.path.splitext(filename)
                fixed_path = os.path.join(output_dir, f"{base_name}_fixed{ext}")
                
                with open(fixed_path, 'w', encoding='utf-8') as f:
                    f.write(auto_fix['fixed_code'])
                
                print(f"🔧 Saved fixed code: {fixed_path}")
                print(f"   Applied {len(auto_fix['fixes_applied'])} fixes")
            
        except Exception as e:
            print(f"⚠️  Failed to save fixed code: {e}")
    
    def _generate_directory_report(self, results: Dict[str, Any], output_dir: str):
        """Generate a combined report for directory analysis"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate summary report
            report_path = os.path.join(output_dir, "directory_analysis_summary.json")
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"📊 Generated directory report: {report_path}")
            
            # Generate markdown summary
            md_report = self._create_markdown_summary(results)
            md_path = os.path.join(output_dir, "directory_analysis_summary.md")
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_report)
            
            print(f"📝 Generated markdown summary: {md_path}")
            
        except Exception as e:
            print(f"⚠️  Failed to generate directory report: {e}")
    
    def _create_markdown_summary(self, results: Dict[str, Any]) -> str:
        """Create a markdown summary of directory analysis"""
        summary = results['summary']
        
        md_content = f"""# Directory Analysis Summary

**Directory:** `{results['directory']}`  
**Analysis Date:** {results['timestamp']}

## Overview

| Metric | Value |
|--------|-------|
| Total Files | {summary['total_files']} |
| Successful Analyses | {summary['successful_analyses']} |
| Failed Analyses | {summary['failed_analyses']} |
| Total Errors | {summary['total_errors']} |
| Total Warnings | {summary['total_warnings']} |
| Average Quality Score | {summary['average_quality_score']}/100 |
| Files with Auto-fixes | {summary['files_with_auto_fixes']} |

## File Details

"""
        
        for file_result in results['files_analyzed']:
            if 'error' not in file_result:
                filename = os.path.basename(file_result.get('filename', 'Unknown'))
                quality = file_result.get('quality_score', 0)
                language = file_result.get('language', 'Unknown')
                
                md_content += f"### {filename}\n"
                md_content += f"- **Language:** {language}\n"
                md_content += f"- **Quality Score:** {quality}/100\n"
                md_content += f"- **Lines of Code:** {file_result.get('line_count', 0)}\n"
                md_content += f"- **Complexity:** {file_result.get('complexity', 0)}\n"
                
                error_summary = file_result.get('error_analysis', {}).get('error_summary', {})
                if error_summary.get('total_errors', 0) > 0 or error_summary.get('total_warnings', 0) > 0:
                    md_content += f"- **Issues:** {error_summary.get('total_errors', 0)} errors, {error_summary.get('total_warnings', 0)} warnings\n"
                
                md_content += "\n"
        
        return md_content
    
    def _print_analysis_summary(self, analysis_results: Dict[str, Any], file_path: str):
        """Print a summary of the analysis results"""
        filename = os.path.basename(file_path)
        
        if 'error' in analysis_results:
            print(f"❌ Analysis failed for {filename}")
            return
        
        print(f"\n📊 Analysis Summary for {filename}")
        print("=" * 50)
        print(f"Language: {analysis_results.get('language', 'Unknown')}")
        print(f"Lines of Code: {analysis_results.get('line_count', 0)}")
        print(f"Complexity: {analysis_results.get('complexity', 0)}")
        print(f"Quality Score: {analysis_results.get('quality_score', 0)}/100")
        print(f"Analysis Time: {analysis_results.get('analysis_time', 0)}s")
        
        # Error summary
        error_summary = analysis_results.get('error_analysis', {}).get('error_summary', {})
        print(f"Errors: {error_summary.get('total_errors', 0)}")
        print(f"Warnings: {error_summary.get('total_warnings', 0)}")
        
        # Improvements and fixes
        comprehensive = analysis_results.get('comprehensive_analysis', {})
        if comprehensive.get('improvements_available'):
            improvements = comprehensive.get('improvements', {})
            print(f"Improvement Suggestions: {len(improvements.get('suggestions', []))}")
        
        if comprehensive.get('auto_fix_available'):
            auto_fix = comprehensive.get('auto_fix', {})
            print(f"Auto-fixes Applied: {auto_fix.get('total_fixes', 0)}")
        
        print("=" * 50)
    
    def _print_directory_summary(self, results: Dict[str, Any]):
        """Print a summary of directory analysis"""
        summary = results['summary']
        
        print(f"\n📊 Directory Analysis Complete")
        print("=" * 60)
        print(f"Directory: {results['directory']}")
        print(f"Files Analyzed: {summary['total_files']}")
        print(f"Successful: {summary['successful_analyses']}")
        print(f"Failed: {summary['failed_analyses']}")
        print(f"Total Errors: {summary['total_errors']}")
        print(f"Total Warnings: {summary['total_warnings']}")
        print(f"Average Quality Score: {summary['average_quality_score']}/100")
        print(f"Files with Auto-fixes: {summary['files_with_auto_fixes']}")
        print("=" * 60)

def create_argument_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Advanced Code Analysis and Documentation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single file
  python main.py file example.py
  
  # Analyze a file with auto-fix
  python main.py file example.py --auto-fix --output ./output
  
  # Analyze entire directory
  python main.py directory ./src --output ./analysis_reports
  
  # Analyze specific file types
  python main.py directory ./src --extensions .py .js --no-docs
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Analysis mode')
    
    # File analysis
    file_parser = subparsers.add_parser('file', help='Analyze a single file')
    file_parser.add_argument('path', help='Path to the code file')
    file_parser.add_argument('--output', '-o', help='Output directory for results')
    file_parser.add_argument('--auto-fix', action='store_true', 
                           help='Automatically fix detected issues')
    file_parser.add_argument('--no-docs', action='store_true',
                           help='Skip documentation generation')
    
    # Directory analysis
    dir_parser = subparsers.add_parser('directory', help='Analyze a directory')
    dir_parser.add_argument('path', help='Path to the directory')
    dir_parser.add_argument('--output', '-o', help='Output directory for results')
    dir_parser.add_argument('--auto-fix', action='store_true',
                          help='Automatically fix detected issues')
    dir_parser.add_argument('--no-docs', action='store_true',
                          help='Skip documentation generation')
    dir_parser.add_argument('--extensions', nargs='+', 
                          default=['.py', '.js', '.ts', '.java', '.cpp', '.c'],
                          help='File extensions to analyze')
    
    return parser

def main():
    """Main entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize pipeline
    pipeline = CodeAnalysisPipeline()
    
    try:
        if args.command == 'file':
            # Analyze single file
            results = pipeline.analyze_single_file(
                file_path=args.path,
                output_dir=args.output,
                auto_fix=args.auto_fix,
                generate_docs=not args.no_docs
            )
            
        elif args.command == 'directory':
            # Analyze directory
            results = pipeline.analyze_directory(
                directory_path=args.path,
                output_dir=args.output,
                auto_fix=args.auto_fix,
                generate_docs=not args.no_docs,
                file_extensions=args.extensions
            )
        
        # Save results if output directory specified
        if args.output and 'error' not in results:
            os.makedirs(args.output, exist_ok=True)
            results_path = os.path.join(args.output, 'analysis_results.json')
            with open(results_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n💾 Complete results saved to: {results_path}")
        
        print(f"\n🎉 Analysis pipeline completed successfully!")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
