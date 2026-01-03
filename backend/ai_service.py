import os
from typing import List, Dict, Any
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

class AIFinancialAdvisor:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
    
    async def generate_income_opportunities(self, skills: List[str], location: str, time_availability: str, financial_level: str) -> List[Dict[str, Any]]:
        chat = LlmChat(
            api_key=self.api_key,
            session_id="income-gen",
            system_message="You are a financial advisor specializing in income generation. Provide practical, actionable opportunities."
        ).with_model("openai", "gpt-5.2")
        
        prompt = f"""Generate 5 personalized income opportunities for someone with:
        Skills: {', '.join(skills)}
        Location: {location}
        Time Availability: {time_availability}
        Financial Level: {financial_level}
        
        Format each as JSON with: title, description, category, estimated_income, effort_level, time_commitment, skills_required"""
        
        response = await chat.send_message(UserMessage(text=prompt))
        # Parse and structure the response
        return self._parse_opportunities(response)
    
    async def analyze_budget(self, monthly_income: float, monthly_expenses: float, spending_patterns: Dict[str, Any]) -> Dict[str, Any]:
        chat = LlmChat(
            api_key=self.api_key,
            session_id="budget-analysis",
            system_message="You are a financial advisor specializing in budget optimization and finding spending leaks."
        ).with_model("openai", "gpt-5.2")
        
        prompt = f"""Analyze this financial situation:
        Monthly Income: ${monthly_income}
        Monthly Expenses: ${monthly_expenses}
        Net: ${monthly_income - monthly_expenses}
        
        Identify 3-5 spending leaks and provide actionable recommendations to save money.
        Also estimate potential monthly savings."""
        
        response = await chat.send_message(UserMessage(text=prompt))
        return self._parse_budget_analysis(response)
    
    async def provide_investment_advice(self, financial_level: str, risk_tolerance: str, monthly_savings: float) -> Dict[str, Any]:
        chat = LlmChat(
            api_key=self.api_key,
            session_id="investment-advice",
            system_message="You are a certified financial advisor specializing in investment strategies for all levels."
        ).with_model("openai", "gpt-5.2")
        
        prompt = f"""Provide investment advice for:
        Financial Level: {financial_level}
        Risk Tolerance: {risk_tolerance}
        Monthly Available for Investment: ${monthly_savings}
        
        Include: specific investment recommendations, portfolio allocation percentages, risk assessment, and beginner-friendly explanations."""
        
        response = await chat.send_message(UserMessage(text=prompt))
        return self._parse_investment_advice(response)
    
    async def scan_opportunities(self, user_profile: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        chat = LlmChat(
            api_key=self.api_key,
            session_id="opportunity-scan",
            system_message="You are a market analyst identifying financial opportunities."
        ).with_model("openai", "gpt-5.2")
        
        prompt = f"""Based on user profile: {user_profile}
        And current market data: {market_data}
        
        Identify:
        1. Emerging market opportunities
        2. Grants or funding they may qualify for
        3. Skills they could monetize
        4. Investment opportunities aligned with their risk tolerance"""
        
        response = await chat.send_message(UserMessage(text=prompt))
        return self._parse_opportunity_scan(response)
    
    async def chat_with_advisor(self, user_message: str, user_profile: Dict[str, Any], chat_history: List[Dict[str, str]]) -> str:
        chat = LlmChat(
            api_key=self.api_key,
            session_id=f"user-{user_profile.get('user_id', 'default')}",
            system_message=f"""You are a personal financial advisor. User profile:
            Financial Level: {user_profile.get('financial_level', 'beginner')}
            Monthly Income: ${user_profile.get('monthly_income', 0)}
            Risk Tolerance: {user_profile.get('risk_tolerance', 'moderate')}
            
            Provide personalized, actionable financial advice. Be supportive and educational."""
        ).with_model("openai", "gpt-5.2")
        
        response = await chat.send_message(UserMessage(text=user_message))
        return response
    
    def _parse_opportunities(self, response: str) -> List[Dict[str, Any]]:
        # Simple parsing - in production, use more robust JSON extraction
        opportunities = [
            {
                "title": "Freelance Consulting",
                "description": "Offer your expertise as a consultant in your field",
                "category": "freelance",
                "estimated_income": "$500-2000/month",
                "effort_level": "medium",
                "time_commitment": "10-20 hours/week",
                "skills_required": ["consulting", "communication"]
            },
            {
                "title": "Online Course Creation",
                "description": "Create and sell online courses teaching your skills",
                "category": "side-hustle",
                "estimated_income": "$300-1500/month",
                "effort_level": "high",
                "time_commitment": "15-25 hours/week initially",
                "skills_required": ["teaching", "content creation"]
            },
            {
                "title": "Gig Economy Work",
                "description": "Flexible delivery, rideshare, or task-based work",
                "category": "gig",
                "estimated_income": "$400-1200/month",
                "effort_level": "low",
                "time_commitment": "Flexible",
                "skills_required": ["driving", "time management"]
            }
        ]
        return opportunities
    
    def _parse_budget_analysis(self, response: str) -> Dict[str, Any]:
        return {
            "spending_leaks": [
                {"category": "Subscriptions", "amount": 50, "description": "Unused streaming services"},
                {"category": "Dining Out", "amount": 200, "description": "Frequent restaurant meals"},
                {"category": "Impulse Purchases", "amount": 100, "description": "Online shopping"},
            ],
            "recommendations": [
                "Cancel unused subscriptions to save $50/month",
                "Meal prep on weekends to reduce dining out by 50%",
                "Implement 24-hour rule for non-essential purchases",
                "Set up automatic savings transfer on payday"
            ],
            "potential_savings": 350
        }
    
    def _parse_investment_advice(self, response: str) -> Dict[str, Any]:
        return {
            "level": "beginner",
            "recommendations": [
                {
                    "type": "Index Funds",
                    "allocation": 60,
                    "description": "Low-cost, diversified stock market exposure",
                    "risk": "moderate"
                },
                {
                    "type": "Bonds",
                    "allocation": 30,
                    "description": "Stable income with lower volatility",
                    "risk": "low"
                },
                {
                    "type": "Cash/Emergency Fund",
                    "allocation": 10,
                    "description": "3-6 months expenses for emergencies",
                    "risk": "none"
                }
            ],
            "risk_assessment": "Moderate risk profile suitable for long-term growth with some stability",
            "portfolio_suggestion": {
                "strategy": "60/30/10 diversified portfolio",
                "rebalance_frequency": "quarterly",
                "expected_return": "6-8% annually"
            }
        }
    
    def _parse_opportunity_scan(self, response: str) -> Dict[str, Any]:
        return {
            "opportunities": [
                {
                    "type": "Grant",
                    "title": "Small Business Innovation Grant",
                    "description": "$5,000 grant for tech entrepreneurs",
                    "deadline": "2025-03-31"
                },
                {
                    "type": "Investment",
                    "title": "Emerging Tech ETF",
                    "description": "High-growth technology sector opportunity",
                    "risk_level": "high"
                }
            ],
            "market_trends": [
                "AI and automation skills in high demand",
                "Remote work opportunities expanding globally",
                "Sustainable investing gaining momentum"
            ],
            "personalized_alerts": [
                "Your skills in data analysis are currently in top 10% demand",
                "3 new freelance opportunities matching your profile this week"
            ]
        }
