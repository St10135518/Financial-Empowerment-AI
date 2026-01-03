from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    password_hash: str
    full_name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    email: str
    full_name: str
    created_at: datetime

class FinancialProfile(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    monthly_income: float = 0
    monthly_expenses: float = 0
    savings_goal: float = 0
    risk_tolerance: str = "moderate"  # low, moderate, high
    skills: List[str] = []
    location: str = ""
    time_availability: str = ""  # part-time, full-time, weekends
    financial_level: str = "beginner"  # beginner, intermediate, advanced
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FinancialProfileUpdate(BaseModel):
    monthly_income: Optional[float] = None
    monthly_expenses: Optional[float] = None
    savings_goal: Optional[float] = None
    risk_tolerance: Optional[str] = None
    skills: Optional[List[str]] = None
    location: Optional[str] = None
    time_availability: Optional[str] = None
    financial_level: Optional[str] = None

class IncomeOpportunity(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    description: str
    category: str  # freelance, side-hustle, micro-business, gig
    estimated_income: str
    effort_level: str  # low, medium, high
    time_commitment: str
    skills_required: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BudgetAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    spending_leaks: List[Dict[str, Any]]
    recommendations: List[str]
    potential_savings: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class InvestmentAdvice(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    level: str  # beginner, intermediate, advanced
    recommendations: List[Dict[str, Any]]
    risk_assessment: str
    portfolio_suggestion: Dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OpportunityScan(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    opportunities: List[Dict[str, Any]]
    market_trends: List[str]
    personalized_alerts: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class EducationLesson(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    category: str
    level: str
    content: str
    duration_minutes: int
    points: int

class UserProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    completed_lessons: List[str] = []
    total_points: int = 0
    achievements: List[str] = []
    current_streak: int = 0
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    role: str  # user, assistant
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class MarketData(BaseModel):
    symbol: str
    price: float
    change_percent: float
    volume: Optional[float] = None
