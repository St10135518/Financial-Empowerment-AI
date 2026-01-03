from fastapi import FastAPI, APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timezone

from models import (
    User, UserCreate, UserLogin, UserResponse,
    FinancialProfile, FinancialProfileUpdate,
    IncomeOpportunity, BudgetAnalysis, InvestmentAdvice,
    OpportunityScan, EducationLesson, UserProgress,
    ChatMessage, ChatRequest
)
from auth_utils import hash_password, verify_password, create_access_token, verify_token
from ai_service import AIFinancialAdvisor
from market_service import MarketDataService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize services
ai_advisor = AIFinancialAdvisor()
market_service = MarketDataService()

# Create the main app
app = FastAPI(title="Financial Empowerment AI")
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== AUTH ROUTES ====================

@api_router.post("/auth/register", response_model=Dict[str, Any])
async def register(user_data: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name
    )
    
    user_dict = user.model_dump()
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    await db.users.insert_one(user_dict)
    
    # Create default financial profile
    profile = FinancialProfile(user_id=user.id)
    profile_dict = profile.model_dump()
    profile_dict['updated_at'] = profile_dict['updated_at'].isoformat()
    await db.financial_profiles.insert_one(profile_dict)
    
    # Create user progress
    progress = UserProgress(user_id=user.id)
    progress_dict = progress.model_dump()
    progress_dict['updated_at'] = progress_dict['updated_at'].isoformat()
    await db.user_progress.insert_one(progress_dict)
    
    # Create token
    token = create_access_token({"user_id": user.id})
    
    return {
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }

@api_router.post("/auth/login", response_model=Dict[str, Any])
async def login(credentials: UserLogin):
    user = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    if not user or not verify_password(credentials.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"user_id": user['id']})
    
    return {
        "token": token,
        "user": {
            "id": user['id'],
            "email": user['email'],
            "full_name": user['full_name']
        }
    }

@api_router.get("/auth/me", response_model=UserResponse)
async def get_current_user(user_id: str = Depends(verify_token)):
    user = await db.users.find_one({"id": user_id}, {"_id": 0, "password_hash": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if isinstance(user['created_at'], str):
        user['created_at'] = datetime.fromisoformat(user['created_at'])
    
    return UserResponse(**user)

# ==================== PROFILE ROUTES ====================

@api_router.get("/profile", response_model=FinancialProfile)
async def get_profile(user_id: str = Depends(verify_token)):
    profile = await db.financial_profiles.find_one({"user_id": user_id}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if isinstance(profile['updated_at'], str):
        profile['updated_at'] = datetime.fromisoformat(profile['updated_at'])
    
    return FinancialProfile(**profile)

@api_router.put("/profile", response_model=FinancialProfile)
async def update_profile(profile_data: FinancialProfileUpdate, user_id: str = Depends(verify_token)):
    update_data = {k: v for k, v in profile_data.model_dump().items() if v is not None}
    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    await db.financial_profiles.update_one(
        {"user_id": user_id},
        {"$set": update_data}
    )
    
    profile = await db.financial_profiles.find_one({"user_id": user_id}, {"_id": 0})
    if isinstance(profile['updated_at'], str):
        profile['updated_at'] = datetime.fromisoformat(profile['updated_at'])
    
    return FinancialProfile(**profile)

# ==================== INCOME GENERATION ROUTES ====================

@api_router.post("/income-generation", response_model=List[IncomeOpportunity])
async def generate_income_opportunities(user_id: str = Depends(verify_token)):
    profile = await db.financial_profiles.find_one({"user_id": user_id}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    opportunities_data = await ai_advisor.generate_income_opportunities(
        skills=profile.get('skills', []),
        location=profile.get('location', ''),
        time_availability=profile.get('time_availability', ''),
        financial_level=profile.get('financial_level', 'beginner')
    )
    
    # Save opportunities
    opportunities = []
    for opp_data in opportunities_data:
        opp = IncomeOpportunity(
            user_id=user_id,
            title=opp_data['title'],
            description=opp_data['description'],
            category=opp_data['category'],
            estimated_income=opp_data['estimated_income'],
            effort_level=opp_data['effort_level'],
            time_commitment=opp_data['time_commitment'],
            skills_required=opp_data['skills_required']
        )
        opp_dict = opp.model_dump()
        opp_dict['created_at'] = opp_dict['created_at'].isoformat()
        await db.income_opportunities.insert_one(opp_dict)
        opportunities.append(opp)
    
    return opportunities

@api_router.get("/income-generation", response_model=List[IncomeOpportunity])
async def get_income_opportunities(user_id: str = Depends(verify_token)):
    opportunities = await db.income_opportunities.find({"user_id": user_id}, {"_id": 0}).sort("created_at", -1).limit(10).to_list(10)
    
    for opp in opportunities:
        if isinstance(opp['created_at'], str):
            opp['created_at'] = datetime.fromisoformat(opp['created_at'])
    
    return [IncomeOpportunity(**opp) for opp in opportunities]

# ==================== BUDGET ANALYSIS ROUTES ====================

@api_router.post("/budget/analyze", response_model=BudgetAnalysis)
async def analyze_budget(user_id: str = Depends(verify_token)):
    profile = await db.financial_profiles.find_one({"user_id": user_id}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    analysis_data = await ai_advisor.analyze_budget(
        monthly_income=profile.get('monthly_income', 0),
        monthly_expenses=profile.get('monthly_expenses', 0),
        spending_patterns={}
    )
    
    analysis = BudgetAnalysis(
        user_id=user_id,
        spending_leaks=analysis_data['spending_leaks'],
        recommendations=analysis_data['recommendations'],
        potential_savings=analysis_data['potential_savings']
    )
    
    analysis_dict = analysis.model_dump()
    analysis_dict['created_at'] = analysis_dict['created_at'].isoformat()
    await db.budget_analyses.insert_one(analysis_dict)
    
    return analysis

@api_router.get("/budget/latest", response_model=BudgetAnalysis)
async def get_latest_budget_analysis(user_id: str = Depends(verify_token)):
    analysis = await db.budget_analyses.find_one({"user_id": user_id}, {"_id": 0}, sort=[("created_at", -1)])
    if not analysis:
        raise HTTPException(status_code=404, detail="No budget analysis found")
    
    if isinstance(analysis['created_at'], str):
        analysis['created_at'] = datetime.fromisoformat(analysis['created_at'])
    
    return BudgetAnalysis(**analysis)

# ==================== INVESTMENT ADVICE ROUTES ====================

@api_router.post("/investment/advice", response_model=InvestmentAdvice)
async def get_investment_advice(user_id: str = Depends(verify_token)):
    profile = await db.financial_profiles.find_one({"user_id": user_id}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    monthly_savings = profile.get('monthly_income', 0) - profile.get('monthly_expenses', 0)
    
    advice_data = await ai_advisor.provide_investment_advice(
        financial_level=profile.get('financial_level', 'beginner'),
        risk_tolerance=profile.get('risk_tolerance', 'moderate'),
        monthly_savings=max(0, monthly_savings)
    )
    
    advice = InvestmentAdvice(
        user_id=user_id,
        level=advice_data['level'],
        recommendations=advice_data['recommendations'],
        risk_assessment=advice_data['risk_assessment'],
        portfolio_suggestion=advice_data['portfolio_suggestion']
    )
    
    advice_dict = advice.model_dump()
    advice_dict['created_at'] = advice_dict['created_at'].isoformat()
    await db.investment_advice.insert_one(advice_dict)
    
    return advice

@api_router.get("/investment/latest", response_model=InvestmentAdvice)
async def get_latest_investment_advice(user_id: str = Depends(verify_token)):
    advice = await db.investment_advice.find_one({"user_id": user_id}, {"_id": 0}, sort=[("created_at", -1)])
    if not advice:
        raise HTTPException(status_code=404, detail="No investment advice found")
    
    if isinstance(advice['created_at'], str):
        advice['created_at'] = datetime.fromisoformat(advice['created_at'])
    
    return InvestmentAdvice(**advice)

# ==================== OPPORTUNITY SCANNER ROUTES ====================

@api_router.post("/opportunities/scan", response_model=OpportunityScan)
async def scan_opportunities(user_id: str = Depends(verify_token)):
    profile = await db.financial_profiles.find_one({"user_id": user_id}, {"_id": 0})
    market_data = market_service.get_market_overview()
    
    scan_data = await ai_advisor.scan_opportunities(
        user_profile=profile,
        market_data={"stocks": market_data}
    )
    
    scan = OpportunityScan(
        user_id=user_id,
        opportunities=scan_data['opportunities'],
        market_trends=scan_data['market_trends'],
        personalized_alerts=scan_data['personalized_alerts']
    )
    
    scan_dict = scan.model_dump()
    scan_dict['created_at'] = scan_dict['created_at'].isoformat()
    await db.opportunity_scans.insert_one(scan_dict)
    
    return scan

@api_router.get("/opportunities/latest", response_model=OpportunityScan)
async def get_latest_opportunity_scan(user_id: str = Depends(verify_token)):
    scan = await db.opportunity_scans.find_one({"user_id": user_id}, {"_id": 0}, sort=[("created_at", -1)])
    if not scan:
        raise HTTPException(status_code=404, detail="No opportunity scan found")
    
    if isinstance(scan['created_at'], str):
        scan['created_at'] = datetime.fromisoformat(scan['created_at'])
    
    return OpportunityScan(**scan)

# ==================== EDUCATION ROUTES ====================

@api_router.get("/education/lessons", response_model=List[EducationLesson])
async def get_lessons(level: str = "beginner"):
    lessons_data = [
        {
            "id": "1",
            "title": "Understanding Compound Interest",
            "category": "Basics",
            "level": "beginner",
            "content": "Learn how your money can grow exponentially over time",
            "duration_minutes": 15,
            "points": 100
        },
        {
            "id": "2",
            "title": "Creating Your First Budget",
            "category": "Budgeting",
            "level": "beginner",
            "content": "Step-by-step guide to tracking income and expenses",
            "duration_minutes": 20,
            "points": 150
        },
        {
            "id": "3",
            "title": "Introduction to Stock Market",
            "category": "Investing",
            "level": "intermediate",
            "content": "Understanding stocks, bonds, and market basics",
            "duration_minutes": 30,
            "points": 200
        },
        {
            "id": "4",
            "title": "Tax Optimization Strategies",
            "category": "Advanced",
            "level": "advanced",
            "content": "Legal ways to minimize tax burden and maximize savings",
            "duration_minutes": 45,
            "points": 300
        }
    ]
    
    return [EducationLesson(**lesson) for lesson in lessons_data if lesson['level'] == level or level == \"all\"]

@api_router.post("/education/complete/{lesson_id}", response_model=UserProgress)
async def complete_lesson(lesson_id: str, user_id: str = Depends(verify_token)):
    progress = await db.user_progress.find_one({"user_id": user_id}, {"_id": 0})
    
    if lesson_id not in progress.get('completed_lessons', []):
        await db.user_progress.update_one(
            {"user_id": user_id},
            {
                "$push": {"completed_lessons": lesson_id},
                "$inc": {"total_points": 100, "current_streak": 1},
                "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}
            }
        )
    
    progress = await db.user_progress.find_one({"user_id": user_id}, {"_id": 0})
    if isinstance(progress['updated_at'], str):
        progress['updated_at'] = datetime.fromisoformat(progress['updated_at'])
    
    return UserProgress(**progress)

@api_router.get("/education/progress", response_model=UserProgress)
async def get_progress(user_id: str = Depends(verify_token)):
    progress = await db.user_progress.find_one({"user_id": user_id}, {"_id": 0})
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    if isinstance(progress['updated_at'], str):
        progress['updated_at'] = datetime.fromisoformat(progress['updated_at'])
    
    return UserProgress(**progress)

# ==================== AI CHAT ROUTES ====================

@api_router.post("/ai-chat", response_model=Dict[str, str])
async def chat_with_ai(chat_request: ChatRequest, user_id: str = Depends(verify_token)):
    profile = await db.financial_profiles.find_one({"user_id": user_id}, {"_id": 0})
    
    # Get recent chat history
    history = await db.chat_messages.find({"user_id": user_id}, {"_id": 0}).sort("timestamp", -1).limit(10).to_list(10)
    
    response = await ai_advisor.chat_with_advisor(
        user_message=chat_request.message,
        user_profile=profile,
        chat_history=history
    )
    
    # Save messages
    user_msg = ChatMessage(user_id=user_id, role="user", content=chat_request.message)
    assistant_msg = ChatMessage(user_id=user_id, role="assistant", content=response)
    
    user_msg_dict = user_msg.model_dump()
    user_msg_dict['timestamp'] = user_msg_dict['timestamp'].isoformat()
    assistant_msg_dict = assistant_msg.model_dump()
    assistant_msg_dict['timestamp'] = assistant_msg_dict['timestamp'].isoformat()
    
    await db.chat_messages.insert_many([user_msg_dict, assistant_msg_dict])
    
    return {"response": response}

@api_router.get("/ai-chat/history", response_model=List[ChatMessage])
async def get_chat_history(user_id: str = Depends(verify_token)):
    messages = await db.chat_messages.find({"user_id": user_id}, {"_id": 0}).sort("timestamp", -1).limit(50).to_list(50)
    
    for msg in messages:
        if isinstance(msg['timestamp'], str):
            msg['timestamp'] = datetime.fromisoformat(msg['timestamp'])
    
    return [ChatMessage(**msg) for msg in reversed(messages)]

# ==================== MARKET DATA ROUTES ====================

@api_router.get("/market/overview")
async def get_market_overview():
    stocks = market_service.get_market_overview()
    crypto = market_service.get_crypto_prices()
    
    return {
        "stocks": stocks,
        "crypto": crypto,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }

@api_router.get("/market/stock/{symbol}")
async def get_stock_data(symbol: str):
    return market_service.get_stock_quote(symbol)

# ==================== DASHBOARD STATS ====================

@api_router.get("/dashboard/stats")
async def get_dashboard_stats(user_id: str = Depends(verify_token)):
    profile = await db.financial_profiles.find_one({"user_id": user_id}, {"_id": 0})
    progress = await db.user_progress.find_one({"user_id": user_id}, {"_id": 0})
    
    monthly_savings = profile.get('monthly_income', 0) - profile.get('monthly_expenses', 0)
    savings_rate = (monthly_savings / profile.get('monthly_income', 1)) * 100 if profile.get('monthly_income', 0) > 0 else 0
    
    return {
        "monthly_income": profile.get('monthly_income', 0),
        "monthly_expenses": profile.get('monthly_expenses', 0),
        "monthly_savings": monthly_savings,
        "savings_rate": round(savings_rate, 1),
        "savings_goal": profile.get('savings_goal', 0),
        "goal_progress": round((monthly_savings / profile.get('savings_goal', 1)) * 100, 1) if profile.get('savings_goal', 0) > 0 else 0,
        "total_points": progress.get('total_points', 0),
        "completed_lessons": len(progress.get('completed_lessons', [])),
        "current_streak": progress.get('current_streak', 0)
    }

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
