"""Test AI service to see if it returns real data or mock data"""
import sys
sys.path.insert(0, 'backend')

import asyncio
from backend.ai_service import AIFinancialAdvisor

async def test_income_opportunities():
    print("Testing Income Generation...")
    advisor = AIFinancialAdvisor()
    
    # Test with user profile similar to "Junior"
    result = await advisor.generate_income_opportunities(
        skills=["writing", "social media"],
        location="New York",
        time_availability="part-time",
        financial_level="beginner"
    )
    
    print("\n=== Income Opportunities Result ===")
    for i, opp in enumerate(result, 1):
        print(f"\n{i}. {opp['title']}")
        print(f"   Category: {opp['category']}")
        print(f"   Income: {opp['estimated_income']}")
        print(f"   Effort: {opp['effort_level']}")
        print(f"   Description: {opp['description'][:100]}...")
        print(f"   Skills: {opp['skills_required']}")
    
    # Check if it's the fallback data
    if result[0]['title'] == "Freelance Consulting":
        print("\n⚠️ FALLBACK DATA DETECTED - LLM not returning valid JSON")
    else:
        print("\n✅ Real AI-generated data")

async def test_budget_analysis():
    print("\n\nTesting Budget Analysis...")
    advisor = AIFinancialAdvisor()
    
    result = await advisor.analyze_budget(
        monthly_income=5000,
        monthly_expenses=4200,
        spending_patterns={}
    )
    
    print("\n=== Budget Analysis Result ===")
    print(f"Spending Leaks: {len(result['spending_leaks'])} items")
    for leak in result['spending_leaks']:
        print(f"  - {leak['category']}: ${leak['amount']} - {leak['description']}")
    
    print(f"\nRecommendations: {len(result['recommendations'])} items")
    for rec in result['recommendations'][:3]:
        print(f"  - {rec}")
    
    print(f"\nPotential Savings: ${result['potential_savings']}")
    
    # Check if it's fallback
    if result['spending_leaks'][0]['category'] == "Subscriptions":
        print("\n⚠️ FALLBACK DATA DETECTED")
    else:
        print("\n✅ Real AI-generated data")

async def test_investment_advice():
    print("\n\nTesting Investment Advice...")
    advisor = AIFinancialAdvisor()
    
    result = await advisor.provide_investment_advice(
        financial_level="beginner",
        risk_tolerance="moderate",
        monthly_savings=800
    )
    
    print("\n=== Investment Advice Result ===")
    print(f"Level: {result['level']}")
    print(f"Risk Assessment: {result['risk_assessment']}")
    
    print(f"\nRecommendations: {len(result['recommendations'])} items")
    for rec in result['recommendations']:
        print(f"  - {rec['type']}: {rec['allocation']}% - {rec['description']}")
    
    print(f"\nPortfolio: {result['portfolio_suggestion']}")
    
    # Check if fallback
    if result['recommendations'][0]['type'] == "Index Funds" and result['recommendations'][0]['allocation'] == 60:
        print("\n⚠️ FALLBACK DATA DETECTED")
    else:
        print("\n✅ Real AI-generated data")

async def main():
    await test_income_opportunities()
    await test_budget_analysis()
    await test_investment_advice()

if __name__ == "__main__":
    asyncio.run(main())
