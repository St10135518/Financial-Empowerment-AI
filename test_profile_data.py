"""Test what AI returns for the actual user profile"""
import sys
sys.path.insert(0, 'backend')

import asyncio
from backend.ai_service import AIFinancialAdvisor

async def test_with_real_profile():
    """Test with Junior's actual profile from Johannesburg"""
    advisor = AIFinancialAdvisor()
    
    print("Testing with Junior's Profile:")
    print("=" * 60)
    print("Skills: Coding, Requirements Gathering, CRM Systems")
    print("Location: Johannesburg, Gauteng, South Africa")
    print("Time: full time")
    print("Level: beginner")
    print("Income: $10000, Expenses: $7500")
    print("Risk: low")
    print("=" * 60)
    
    # Test Income Generation
    print("\n1. INCOME GENERATION TEST:")
    print("-" * 60)
    income_opps = await advisor.generate_income_opportunities(
        skills=["Coding", "Requirements Gathering & Elicitation", "CRM Systems"],
        location="Johannesburg, Gauteng, South Africa",
        time_availability="full time",
        financial_level="beginner"
    )
    
    for i, opp in enumerate(income_opps, 1):
        print(f"\n{i}. {opp['title']}")
        print(f"   Category: {opp['category']}")
        print(f"   Income: {opp['estimated_income']}")
        print(f"   Description: {opp['description']}")
        print(f"   Skills: {opp['skills_required']}")
    
    # Check if fallback
    if income_opps[0]['title'] == "Freelance Consulting":
        print("\n❌ FALLBACK DATA - AI not generating properly!")
    else:
        print("\n✅ Real AI data generated!")
    
    # Test Budget Analysis
    print("\n\n2. BUDGET ANALYSIS TEST:")
    print("-" * 60)
    budget = await advisor.analyze_budget(
        monthly_income=10000,
        monthly_expenses=7500,
        spending_patterns={}
    )
    
    print(f"Spending Leaks: {len(budget['spending_leaks'])}")
    for leak in budget['spending_leaks']:
        print(f"  - {leak['category']}: ${leak['amount']} - {leak['description']}")
    
    print(f"\nPotential Savings: ${budget['potential_savings']}")
    
    if budget['spending_leaks'][0]['category'] == "Subscriptions":
        print("\n❌ FALLBACK DATA")
    else:
        print("\n✅ Real AI data")
    
    # Test Investment Advice
    print("\n\n3. INVESTMENT ADVICE TEST:")
    print("-" * 60)
    investment = await advisor.provide_investment_advice(
        financial_level="beginner",
        risk_tolerance="low",
        monthly_savings=2500
    )
    
    print(f"Risk Assessment: {investment['risk_assessment']}")
    print(f"\nRecommendations:")
    for rec in investment['recommendations']:
        print(f"  - {rec['type']}: {rec['allocation']}%")
    
    if investment['recommendations'][0]['allocation'] == 60:
        print("\n❌ FALLBACK DATA")
    else:
        print("\n✅ Real AI data")
    
    # Test Education
    print("\n\n4. EDUCATION LESSONS TEST:")
    print("-" * 60)
    lessons = await advisor.generate_personalized_lessons(
        financial_level="beginner",
        user_profile={
            "skills": ["Coding", "Requirements Gathering & Elicitation", "CRM Systems"],
            "monthly_income": 10000,
            "location": "Johannesburg, Gauteng, South Africa"
        }
    )
    
    for i, lesson in enumerate(lessons, 1):
        print(f"\n{i}. {lesson['title']}")
        print(f"   Category: {lesson['category']}")
        print(f"   Duration: {lesson['duration_minutes']} min")
        print(f"   Content: {lesson['content']}")
    
    if lessons[0]['title'] == "Understanding Compound Interest":
        print("\n❌ FALLBACK DATA")
    else:
        print("\n✅ Real AI data")

if __name__ == "__main__":
    asyncio.run(test_with_real_profile())
