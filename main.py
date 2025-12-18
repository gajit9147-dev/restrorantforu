#!/usr/bin/env python3
"""
Main application for Restaurant Assistant AI Agent
"""

import json
from agent import RestaurantAssistantAgent, AgentResponse

def display_response(response: AgentResponse):
    """Display agent response in a formatted way"""
    print("\n" + "="*50)
    print(f"ACTION: {response.action.upper()}")
    print("-"*50)
    print(f"MESSAGE: {response.message}")
    
    if response.data:
        print("\nDATA:")
        print(json.dumps(response.data, indent=2))
    
    if response.needs_confirmation:
        print("\n⚠️  ACTION REQUIRES CONFIRMATION")
    
    print("="*50 + "\n")

def main():
    """Main interaction loop"""
    print("🍽️  RESTAURANT ASSISTANT AI AGENT 🍽️")
    print("Type 'quit' or 'exit' to end the session\n")
    
    # Initialize agent
    agent = RestaurantAssistantAgent()
    
    # Example context (can be extended)
    context = []
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Thank you for using Restaurant Assistant. Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Process query
            response = agent.process_query(user_input, context)
            
            # Display response
            display_response(response)
            
            # Handle confirmation if needed
            if response.needs_confirmation:
                confirm = input("Confirm action? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    # Execute the action with confirmation
                    if response.action == "confirmation_required":
                        booking_id = response.data.get("booking_id")
                        if booking_id:
                            final_response = agent.delete_booking(booking_id, confirm=False)
                            display_response(final_response)
                else:
                    print("Action cancelled.")
            
            # Add to context
            context.append({
                "user": user_input,
                "agent": response.message,
                "action": response.action
            })
            
        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again or rephrase your question.")

def run_examples():
    """Run example queries to demonstrate functionality"""
    print("Running example queries...\n")
    
    agent = RestaurantAssistantAgent()
    
    examples = [
        "Can you find my booking with ID BK001?",
        "What's on the menu?",
        "What are your opening hours?",
        "I want to cancel booking BK002",
        "What's the current time?",
        "Do you offer catering services?"
    ]
    
    for query in examples:
        print(f"\nQuery: {query}")
        response = agent.process_query(query)
        display_response(response)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Restaurant Assistant AI Agent")
    parser.add_argument("--examples", action="store_true", 
                       help="Run example queries")
    
    args = parser.parse_args()
    
    if args.examples:
        run_examples()
    else:
        main()