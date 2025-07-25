from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class CodeAnalysisRequest(BaseModel):
    code: str
    filename: Optional[str] = None
    language: Optional[str] = None


class FunctionInfo(BaseModel):
    name: str
    type: str
    parameters: Optional[List[str]] = None
    line_start: int
    line_end: int
    docstring: Optional[str] = None


class ClassInfo(BaseModel):
    name: str
    type: str
    line_start: int
    line_end: int
    docstring: Optional[str] = None


class CodeAnalysisResponse(BaseModel):
    language: str
    line_count: int
    complexity: int
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    summary: str
    filename: Optional[str] = None
    error: Optional[str] = None


class DocumentationRequest(BaseModel):
    code: str
    filename: Optional[str] = None
    format: str = "markdown"  # markdown, html, json


class DocumentationResponse(BaseModel):
    documentation: str
    format: str
    filename: Optional[str] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    models_loaded: Dict[str, bool]
