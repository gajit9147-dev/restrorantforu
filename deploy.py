#!/usr/bin/env python3
"""
Deployment script for the AI Agent
"""

import os
import sys
from typing import Optional

class AgentDeployer:
    """Deploy and configure the AI Agent"""
    
    @staticmethod
    def check_dependencies():
        """Check if all dependencies are installed"""
        required = ['openai', 'python-dotenv']
        missing = []
        
        for package in required:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing.append(package)
        
        if missing:
            print(f"Missing packages: {', '.join(missing)}")
            print("Install with: pip install " + " ".join(missing))
            return False
        return True
    
    @staticmethod
    def setup_environment():
        """Setup environment variables"""
        from dotenv import load_dotenv
        load_dotenv()
        
        if not os.getenv("OPENAI_API_KEY"):
            print("Warning: OPENAI_API_KEY not found in environment")
            print("Please add it to .env file or set as environment variable")
            return False
        return True
    
    @staticmethod
    def run_tests():
        """Run basic tests"""
        from agent import RestaurantAssistantAgent
        
        print("Running basic tests...")
        
        agent = RestaurantAssistantAgent()
        
        test_cases = [
            ("Get booking BK001", "booking_retrieval"),
            ("What's on menu?", "general_inquiry"),
            ("Cancel booking", "booking_deletion"),
        ]
        
        all_passed = True
        for query, expected_intent in test_cases:
            intent = agent._classify_intent(query)
            status = "✓" if intent == expected_intent else "✗"
            print(f"{status} Query: '{query}' -> Intent: {intent}")
            
            if intent != expected_intent:
                all_passed = False
        
        return all_passed

def main():
    """Main deployment routine"""
    print("🔧 AI Agent Deployment Setup 🔧")
    
    deployer = AgentDeployer()
    
    # Check dependencies
    if not deployer.check_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not deployer.setup_environment():
        print("Continuing with limited functionality...")
    
    # Run tests
    if deployer.run_tests():
        print("\n✅ All tests passed!")
        print("\nTo run the agent:")
        print("1. python main.py (for interactive mode)")
        print("2. python main.py --examples (for demo)")
        print("\nTo use enhanced LLM version:")
        print("1. Set OPENAI_API_KEY in .env file")
        print("2. python llm_agent.py")
    else:
        print("\n❌ Some tests failed. Please check implementation.")
        sys.exit(1)

if __name__ == "__main__":
    main()