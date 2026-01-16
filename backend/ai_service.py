import os
from typing import List, Dict, Any
import logging
import httpx
import asyncio
from groq import AsyncGroq
from dotenv import load_dotenv
from pathlib import Path
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

class AIFinancialAdvisor:
    def __init__(self):
        self.groq_api_key = os.environ.get('GROQ_API_KEY')
        self.groq_model = os.environ.get('GROQ_MODEL', 'llama-3.1-8b-instant')
        self.client = AsyncGroq(api_key=self.groq_api_key) if self.groq_api_key else None
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self.logger = logging.getLogger("AIFinancialAdvisor")
        self.last_error = None
    
    def _json_instructions(self, schema_hint: str) -> str:
        return (
            "\n\nReturn ONLY valid JSON that matches this schema. "
            "No prose, no markdown, no code fences. "
            f"Schema hint: {schema_hint}"
        )

    def _safe_json_load(self, text: str) -> Any:
        """Best-effort JSON extraction. Falls back to empty structure on failure."""
        if not text:
            return None
        try:
            return json.loads(text)
        except Exception:
            pass
        try:
            start_obj = text.find('{')
            start_arr = text.find('[')
            starts = [x for x in [start_obj, start_arr] if x != -1]
            if not starts:
                return None
            start = min(starts)
            end = max(text.rfind('}'), text.rfind(']'))
            if end > start:
                snippet = text[start:end+1]
                return json.loads(snippet)
        except Exception:
            return None
    
    async def generate_income_opportunities(self, skills: List[str], location: str, time_availability: str, financial_level: str) -> List[Dict[str, Any]]:
        try:
            schema = "{ opportunities: Array<{ title: string, description: string, category: 'freelance'|'side-hustle'|'gig', estimated_income: string, effort_level: 'low'|'medium'|'high', time_commitment: string, skills_required: string[] }> }"
            prompt = (
                f"You are a financial advisor. Generate 3 personalized income opportunities for someone with:\n"
                f"Skills: {', '.join(skills) if skills else 'general skills'}\n"
                f"Location: {location or 'any location'}\n"
                f"Time: {time_availability or 'flexible'}\n"
                f"Level: {financial_level or 'beginner'}\n\n"
                "Be specific and practical."
                + self._json_instructions(schema)
            )
            
            response = await self._call_llm(prompt)
            return self._parse_opportunities(response)
        except Exception as e:
            print(f"AI Service error in generate_income_opportunities: {e}")
            return self._parse_opportunities("")
    
    async def analyze_budget(self, monthly_income: float, monthly_expenses: float, spending_patterns: Dict[str, Any]) -> Dict[str, Any]:
        try:
            schema = "{ spending_leaks: Array<{ category: string, amount: number, description: string }>, recommendations: string[], potential_savings: number }"
            prompt = (
                "You are a financial advisor. Analyze this budget:\n"
                f"Income: ${monthly_income}/month\n"
                f"Expenses: ${monthly_expenses}/month\n"
                f"Net: ${monthly_income - monthly_expenses}/month\n\n"
                "Identify 3-5 spending leaks and provide actionable recommendations to save money. Estimate potential monthly savings."
                + self._json_instructions(schema)
            )
            
            response = await self._call_llm(prompt)
            return self._parse_budget_analysis(response)
        except Exception as e:
            print(f"AI Service error in analyze_budget: {e}")
            return self._parse_budget_analysis("")
    
    async def provide_investment_advice(self, financial_level: str, risk_tolerance: str, monthly_savings: float) -> Dict[str, Any]:
        try:
            schema = "{ level: string, recommendations: Array<{ type: string, allocation: number, description: string, risk: string }>, risk_assessment: string, portfolio_suggestion: { strategy: string, rebalance_frequency: string, expected_return: string } }"
            prompt = (
                "You are a financial advisor. Provide investment advice for:\n"
                f"Level: {financial_level}\n"
                f"Risk: {risk_tolerance}\n"
                f"Monthly savings: ${monthly_savings}\n\n"
                "Include specific investment recommendations with allocations, portfolio strategy, and risk assessment."
                + self._json_instructions(schema)
            )
            
            response = await self._call_llm(prompt)
            return self._parse_investment_advice(response)
        except Exception as e:
            print(f"AI Service error in provide_investment_advice: {e}")
            return self._parse_investment_advice("")
    
    async def scan_opportunities(self, user_profile: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            schema = "{ opportunities: Array<{ type: 'Grant'|'Investment'|'Skill'|'Side-Hustle', title: string, description: string, risk_level?: string, deadline?: string }>, market_trends: string[], personalized_alerts: string[] }"
            prompt = (
                "You are a market analyst. Based on user profile and current market data, identify: \n"
                "1. Emerging market opportunities\n"
                "2. Grants or funding they may qualify for\n"
                "3. Skills they could monetize\n"
                "4. Investment opportunities\n\n"
                f"User: {user_profile.get('financial_level', 'beginner')} level, {user_profile.get('risk_tolerance', 'moderate')} risk\n"
                f"Market: {market_data.get('stocks', [])}\n"
                + self._json_instructions(schema)
            )
            
            response = await self._call_llm(prompt)
            return self._parse_opportunity_scan(response)
        except Exception as e:
            print(f"AI Service error in scan_opportunities: {e}")
            return self._parse_opportunity_scan("")
    
    async def generate_personalized_lessons(self, financial_level: str, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized education lessons based on user profile"""
        try:
            schema = "{ lessons: Array<{ title: string, category: string, content: string, duration_minutes: number, points: number }> }"
            skills = user_profile.get('skills', [])
            income = user_profile.get('monthly_income', 0)
            
            prompt = (
                f"You are a financial education expert. Generate 4 personalized financial education lessons for:\n"
                f"Level: {financial_level}\n"
                f"Skills: {', '.join(skills) if skills else 'general'}\n"
                f"Income: ${income}/month\n\n"
                "Create lessons that are practical, actionable, and relevant to their situation. "
                "Include beginner, intermediate, and advanced topics. "
                "Each lesson should have: title, category (Basics/Budgeting/Investing/Advanced), "
                "content (1-2 sentences), duration (15-45 min), points (100-300)."
                + self._json_instructions(schema)
            )
            
            response = await self._call_llm(prompt)
            return self._parse_education_lessons(response, financial_level)
        except Exception as e:
            print(f"AI Service error in generate_personalized_lessons: {e}")
            return self._parse_education_lessons("", financial_level)
    
    async def chat_with_advisor(self, user_message: str, user_profile: Dict[str, Any], chat_history: List[Dict[str, str]]) -> str:
        try:
            # Build context from profile
            profile_context = f"User: {user_profile.get('financial_level', 'beginner')} level, ${user_profile.get('monthly_income', 0)}/mo income, {user_profile.get('risk_tolerance', 'moderate')} risk tolerance."
            
            # Add recent history
            history_text = ""
            if chat_history:
                recent = list(reversed(chat_history[-4:]))  # Last 4 messages
                history_text = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in recent])
            
            prompt = f"""You are a personal financial advisor.
{profile_context}

Recent conversation:
{history_text}

User: {user_message}

Provide personalized, actionable financial advice. Be supportive and educational."""
            
            response = await self._call_llm(prompt)
            return response if response else self._fallback_chat_reply(user_message, user_profile)
        except Exception as e:
            print(f"AI Service error in chat: {e}")
            return self._fallback_chat_reply(user_message, user_profile)

    def _fallback_chat_reply(self, user_message: str, user_profile: Dict[str, Any]) -> str:
        """Deterministic, API-free response so chat keeps working without OpenAI."""
        risk = user_profile.get("risk_tolerance", "moderate") if user_profile else "moderate"
        income = user_profile.get("monthly_income", 0) if user_profile else 0
        expenses = user_profile.get("monthly_expenses", 0) if user_profile else 0
        savings = max(income - expenses, 0)
        level = user_profile.get("financial_level", "beginner") if user_profile else "beginner"

        tips = [
            "Set aside 3-6 months of expenses as an emergency fund in a high-yield savings account.",
            "Automate transfers on payday so saving happens before spending.",
            "Track top 3 spending categories weekly and cap the priciest one by 10-20% this month.",
            "Use a simple 50/30/20 budget (needs/wants/saving) and adjust by 5% toward savings if possible.",
        ]

        invest = {
            "low": "Focus on capital preservation: high-yield savings, CDs, short-term treasuries; small slice in broad bond ETF.",
            "moderate": "Blend: broad market index fund + bond fund (e.g., 60/40 or 70/30) and rebalance quarterly.",
            "high": "Heavier equity tilt: broad index core plus a small satellite in growth/sector ETFs; rebalance twice a year.",
        }

        reply_lines = [
            "Here's a quick plan you can act on now (offline mode):",
            f"- Cash flow: income ~ ${income:.2f}, expenses ~ ${expenses:.2f}, est. monthly savings ~ ${savings:.2f}.",
            f"- Budget: {tips[0]}",
            f"- Spending: {tips[2]}",
            f"- Investing ({risk} risk, level {level}): {invest.get(risk, invest['moderate'])}",
            "- Next step: pick one action today (e.g., automate a $25 transfer) and review in a week." 
        ]

        return "\n".join(reply_lines)
    
    async def _call_llm(self, prompt: str) -> str:
        """Call Groq API (fast, free, reliable)"""
        if not self.client:
            self.logger.error("Groq client is None - API key missing? Falling back to HTTP call.")
            # Fallback to direct HTTP call
            try:
                headers = {"Authorization": f"Bearer {self.groq_api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": self.groq_model,
                    "messages": [
                        {"role": "system", "content": "You are a knowledgeable financial advisor. Provide concise, actionable advice."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
                resp = await self.http_client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    text = data["choices"][0]["message"]["content"]
                    self.logger.info(f"Groq HTTP OK: {text[:120].replace(chr(10),' ')}...")
                    return text.strip()
                else:
                    self.last_error = f"Groq HTTP {resp.status_code}: {resp.text[:200]}"
                    self.logger.error(self.last_error)
                    return ""
            except Exception as e:
                self.last_error = f"Groq HTTP exception: {e}"
                self.logger.error(self.last_error)
                return ""
        
        try:
            self.logger.debug(f"Calling Groq with prompt: {prompt[:80]}...")
            response = await self.client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {"role": "system", "content": "You are a knowledgeable financial advisor. Provide concise, actionable advice."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            text = response.choices[0].message.content
            self.logger.info(f"Groq OK: {text[:120].replace(chr(10),' ')}...")
            return text.strip()
        except Exception as e:
            self.last_error = f"Groq SDK error: {type(e).__name__}: {str(e)}"
            self.logger.error(self.last_error)
            import traceback
            self.logger.error(traceback.format_exc())
            # Try HTTP fallback once
            try:
                headers = {"Authorization": f"Bearer {self.groq_api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": self.groq_model,
                    "messages": [
                        {"role": "system", "content": "You are a knowledgeable financial advisor. Provide concise, actionable advice."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
                resp = await self.http_client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    text = data["choices"][0]["message"]["content"]
                    self.logger.info(f"Groq HTTP OK(after SDK fail): {text[:120].replace(chr(10),' ')}...")
                    return text.strip()
                else:
                    self.last_error = f"Groq HTTP {resp.status_code}: {resp.text[:200]}"
                    self.logger.error(self.last_error)
            except Exception as e2:
                self.last_error = f"Groq HTTP exception: {e2}"
                self.logger.error(self.last_error)
            return ""
    
    async def close(self):
        """Close clients if needed"""
        try:
            if hasattr(self.client, "close") and callable(getattr(self.client, "close")):
                await self.client.close()
        finally:
            await self.http_client.aclose()
    
    def _parse_opportunities(self, response: str) -> List[Dict[str, Any]]:
        data = self._safe_json_load(response)
        items = []
        if isinstance(data, dict) and isinstance(data.get("opportunities"), list):
            items = data["opportunities"]
        elif isinstance(data, list):
            items = data
        if not items:
            # Fallback
            return [
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
        normalized = []
        for x in items[:3]:
            normalized.append({
                "title": x.get("title", "Opportunity"),
                "description": x.get("description", ""),
                "category": (x.get("category") or "side-hustle").lower(),
                "estimated_income": x.get("estimated_income", ""),
                "effort_level": (x.get("effort_level") or "medium").lower(),
                "time_commitment": x.get("time_commitment", ""),
                "skills_required": x.get("skills_required", []) or []
            })
        return normalized
    
    def _parse_budget_analysis(self, response: str) -> Dict[str, Any]:
        data = self._safe_json_load(response)
        if isinstance(data, dict) and data.get("spending_leaks"):
            return {
                "spending_leaks": data.get("spending_leaks", []),
                "recommendations": data.get("recommendations", []),
                "potential_savings": data.get("potential_savings", 0)
            }
        # Fallback
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
        data = self._safe_json_load(response)
        if isinstance(data, dict) and data.get("recommendations"):
            return {
                "level": data.get("level", "beginner"),
                "recommendations": data.get("recommendations", []),
                "risk_assessment": data.get("risk_assessment", ""),
                "portfolio_suggestion": data.get("portfolio_suggestion", {})
            }
        # Fallback
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
        data = self._safe_json_load(response)
        if isinstance(data, dict) and data.get("opportunities"):
            return {
                "opportunities": data.get("opportunities", []),
                "market_trends": data.get("market_trends", []),
                "personalized_alerts": data.get("personalized_alerts", [])
            }
        # Fallback
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
    def _parse_education_lessons(self, response: str, financial_level: str) -> List[Dict[str, Any]]:
        """Parse AI-generated education lessons with fallback"""
        data = self._safe_json_load(response)
        lessons = []
        
        if isinstance(data, dict) and isinstance(data.get("lessons"), list):
            lessons = data["lessons"]
        elif isinstance(data, list):
            lessons = data
        
        if not lessons:
            # Fallback lessons
            return [
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
        
        # Normalize and add IDs
        normalized = []
        for i, lesson in enumerate(lessons[:4], 1):
            normalized.append({
                "id": str(i),
                "title": lesson.get("title", f"Lesson {i}"),
                "category": lesson.get("category", "General"),
                "level": financial_level,
                "content": lesson.get("content", "Financial education content"),
                "duration_minutes": int(lesson.get("duration_minutes", 20)),
                "points": int(lesson.get("points", 100))
            })
        
        return normalized