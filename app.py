from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core import CodeAnalyzer, DocumentationGenerator
from models import (
    CodeAnalysisRequest, CodeAnalysisResponse, 
    DocumentationRequest, DocumentationResponse,
    HealthResponse
)
import uvicorn
from typing import Dict, Any

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Code Analysis and Documentation Generator",
    description="Advanced code analysis and documentation generation using transformer models and tree-sitter parsing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize components
code_analyzer = CodeAnalyzer()
doc_generator = DocumentationGenerator()

@app.get("/", response_class=HTMLResponse)
async def serve_web_interface():
    """Serve the web interface HTML file"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Web Interface Not Found</h1><p>Please ensure static/index.html exists.</p>",
            status_code=404
        )

@app.get("/api", response_model=Dict[str, str])
async def api_info():
    """API information endpoint"""
    return {
        "message": "Code Analysis and Documentation Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "web_interface": "/",
        "endpoints": {
            "analyze_file": "/analyze (POST - file upload)",
            "analyze_code": "/analyze/code (POST - JSON)",
            "generate_docs_file": "/documentation (POST - file upload)",
            "generate_docs_code": "/documentation/code (POST - JSON)",
            "health": "/health (GET)",
            "supported_languages": "/supported-languages (GET)"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        models_loaded={
            "summarizer": code_analyzer.summarizer is not None,
            "tokenizer": code_analyzer.tokenizer is not None,
            "code_model": code_analyzer.code_model is not None
        }
    )

@app.post("/analyze", response_model=Dict[str, Any])
async def analyze_code_file(file: UploadFile = File(...)):
    """Analyze uploaded code file"""
    try:
        content = await file.read()
        code_str = content.decode("utf-8")
        analysis_result = code_analyzer.analyze_code_file(code_str, file.filename)
        return analysis_result
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be text-based and UTF-8 encoded")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/code", response_model=Dict[str, Any])
async def analyze_code_text(request: CodeAnalysisRequest):
    """Analyze code provided as text"""
    try:
        analysis_result = code_analyzer.analyze_code_file(
            request.code, 
            request.filename
        )
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/documentation")
async def generate_documentation_file(
    file: UploadFile = File(...),
    format: str = "markdown"
):
    """Generate documentation from uploaded code file"""
    try:
        content = await file.read()
        code_str = content.decode("utf-8")
        
        # First analyze the code
        analysis_result = code_analyzer.analyze_code_file(code_str, file.filename)
        
        # Then generate documentation
        documentation = doc_generator.generate_documentation(analysis_result, format)
        
        # Return appropriate response type based on format
        if format.lower() == "html":
            return HTMLResponse(content=documentation, media_type="text/html")
        elif format.lower() == "json":
            return analysis_result  # JSON is already returned as analysis result with extra fields
        else:  # markdown
            return PlainTextResponse(content=documentation, media_type="text/plain")
            
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be text-based and UTF-8 encoded")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Documentation generation failed: {str(e)}")

@app.post("/documentation/code", response_model=DocumentationResponse)
async def generate_documentation_text(request: DocumentationRequest):
    """Generate documentation from code provided as text"""
    try:
        # First analyze the code
        analysis_result = code_analyzer.analyze_code_file(
            request.code, 
            request.filename
        )
        
        # Then generate documentation
        documentation = doc_generator.generate_documentation(
            analysis_result, 
            request.format
        )
        
        return DocumentationResponse(
            documentation=documentation,
            format=request.format,
            filename=request.filename
        )
        
    except Exception as e:
        return DocumentationResponse(
            documentation="",
            format=request.format,
            filename=request.filename,
            error=f"Documentation generation failed: {str(e)}"
        )

@app.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "supported_languages": list(code_analyzer.languages.keys()),
        "detection_methods": [
            "filename_extension",
            "content_analysis"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

