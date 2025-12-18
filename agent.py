import json
import datetime
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class AgentResponse:
    """Structure for agent responses"""
    action: str
    message: str
    data: Optional[Dict] = None
    needs_confirmation: bool = False

class GastroGuideAgent:
    """
    GastroGuide - Your Friendly Restaurant AI Assistant
    
    Personality: Warm, knowledgeable, solution-oriented, subtly persuasive
    Core Principles: Empathy first, proactive, memory-aware, action-oriented
    """
    
    def __init__(self):
        """Initialize GastroGuide with conversation context"""
        self.context = {
            'guest_name': None,
            'dietary_restrictions': [],
            'celebration': None,
            'conversation_history': [],
            'current_order': [],
            'preferences': {}
        }
        self.restaurant_name = "Mediterranean Delight"
        
    def process_query(self, user_input: str, context: dict = None) -> AgentResponse:
        """
        Process user query with warm, conversational responses
        
        Args:
            user_input: User's message
            context: Previous conversation context
            
        Returns:
            AgentResponse with natural, empathetic reply
        """
        user_input_lower = user_input.lower()
        
        # Extract and remember guest name
        self._extract_guest_name(user_input)
        
        # Detect special occasions
        self._detect_celebration(user_input_lower)
        
        # Detect dietary restrictions
        self._detect_dietary_restrictions(user_input_lower)
        
        # Store conversation
        self.context['conversation_history'].append({
            'user': user_input,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        # Route to appropriate handler
        if self._is_greeting(user_input_lower):
            return self._handle_greeting()
        
        elif 'menu' in user_input_lower or 'food' in user_input_lower or 'dish' in user_input_lower or 'recommend' in user_input_lower:
            return self._handle_menu_inquiry(user_input_lower)
        
        elif 'booking' in user_input_lower or 'reservation' in user_input_lower or 'table' in user_input_lower:
            return self._handle_booking_inquiry(user_input_lower)
        
        elif 'hour' in user_input_lower or 'open' in user_input_lower or 'close' in user_input_lower:
            return self._handle_hours_inquiry()
        
        elif any(word in user_input_lower for word in ['problem', 'issue', 'complaint', 'wrong', 'late', 'cold', 'bad']):
            return self._handle_complaint(user_input_lower)
        
        elif any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate']):
            return self._handle_gratitude()
        
        else:
            return self._handle_general_query()
    
    def _extract_guest_name(self, text: str):
        """Extract guest name from conversation"""
        patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"this is (\w+)",
            r"i am (\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                self.context['guest_name'] = match.group(1).capitalize()
                break
    
    def _detect_celebration(self, text: str):
        """Detect special occasions"""
        celebrations = {
            'anniversary': ['anniversary', 'anniversaries'],
            'birthday': ['birthday', 'bday', 'b-day'],
            'graduation': ['graduation', 'graduated'],
            'engagement': ['engagement', 'engaged', 'proposal'],
            'celebration': ['celebrating', 'celebrate', 'special occasion']
        }
        
        for event, keywords in celebrations.items():
            if any(keyword in text for keyword in keywords):
                self.context['celebration'] = event
                break
    
    def _detect_dietary_restrictions(self, text: str):
        """Detect and remember dietary restrictions"""
        restrictions = {
            'vegetarian': ['vegetarian', 'veggie', 'no meat'],
            'vegan': ['vegan'],
            'gluten-free': ['gluten free', 'gluten-free', 'celiac'],
            'nut allergy': ['nut allergy', 'allergic to nuts', 'no nuts'],
            'dairy-free': ['dairy free', 'dairy-free', 'lactose', 'no dairy'],
            'halal': ['halal'],
            'kosher': ['kosher']
        }
        
        for restriction, keywords in restrictions.items():
            if any(keyword in text for keyword in keywords):
                if restriction not in self.context['dietary_restrictions']:
                    self.context['dietary_restrictions'].append(restriction)
    
    def _is_greeting(self, text: str) -> bool:
        """Check if message is a greeting"""
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings']
        return any(greet in text for greet in greetings)
    
    def _handle_greeting(self) -> AgentResponse:
        """Warm, personalized greeting"""
        greeting = self._get_time_based_greeting()
        
        if self.context['guest_name']:
            name_part = f"{self.context['guest_name']}! "
        else:
            name_part = ""
        
        if self.context['celebration']:
            celebration_msg = self._get_celebration_greeting()
            message = f"{greeting} {name_part}{celebration_msg}\n\n"
        else:
            message = f"{greeting} {name_part}Welcome to {self.restaurant_name}! I'm GastroGuide, your personal dining assistant, and I'm delighted to help you today.\n\n"
        
        message += "I can assist you with:\n"
        message += "✨ **Personalized menu recommendations** - Our chef's specials are extraordinary today!\n"
        message += "🍷 **Wine pairings** - Perfect complements to elevate your meal\n"
        message += "📅 **Reservations** - Securing your ideal table\n"
        message += "🎉 **Special occasions** - Making your celebration unforgettable\n\n"
        message += "What brings you to us today?"
        
        return AgentResponse(
            action="greeting",
            message=message,
            data=self.context
        )
    
    def _get_time_based_greeting(self) -> str:
        """Get greeting based on time of day"""
        hour = datetime.datetime.now().hour
        if hour < 12:
            return "Good morning!"
        elif hour < 17:
            return "Good afternoon!"
        else:
            return "Good evening!"
    
    def _get_celebration_greeting(self) -> str:
        """Generate celebration-specific greeting"""
        celebration = self.context['celebration']
        
        messages = {
            'anniversary': "Happy Anniversary! 💕 What a joy to celebrate this special milestone with you. We're honored you've chosen us for such a meaningful occasion.",
            'birthday': "Happy Birthday! 🎂 This is wonderful! Let's make your birthday dining experience absolutely memorable.",
            'graduation': "Congratulations on your graduation! 🎓 What an amazing achievement! We'd be thrilled to help you celebrate this exciting chapter.",
            'engagement': "Congratulations on your engagement! 💍 How exciting! We're honored to be part of your celebration.",
            'celebration': "I see you're celebrating something special! 🎉 We love being part of life's beautiful moments."
        }
        
        return messages.get(celebration, messages['celebration'])
    
    def _handle_menu_inquiry(self, query: str) -> AgentResponse:
        """Handle menu questions with vivid descriptions and upselling"""
        from database import get_all_menu_items
        
        menu_items = get_all_menu_items()
        
        # Check for specific dietary needs
        dietary_filter = ""
        if self.context['dietary_restrictions']:
            dietary_filter = f"\n\n*I've noted you're looking for {', '.join(self.context['dietary_restrictions'])} options. Let me highlight those for you!*\n"
        
        greeting = f"Wonderful question! Let me share some of our most exquisite offerings with you.{dietary_filter}\n\n"
        
        # Organize by category with vivid descriptions
        categories = {}
        for item in menu_items:
            cat = item['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        message = greeting
        
        # Highlight chef's specials and popular items
        message += "**🌟 Chef's Recommendations:**\n\n"
        
        for category, items in categories.items():
            message += f"**{category}:**\n"
            # Show top 2 from each category with descriptions
            for item in items[:2]:
                message += f"• **{item['name']}** (${item['price']:.2f}) - {item['description']}\n"
                
                # Add pairing suggestion for mains
                if category == 'Main Course':
                    message += f"  *Perfect with our {self._suggest_pairing(item['name'])}*\n"
            message += "\n"
        
        # Upselling suggestion
        message += "💡 **My Suggestion:** The Seafood Paella paired with our house Pinot Grigio is absolutely divine. "
        message += "May I also recommend starting with our Hummus Platter? It's a guest favorite!\n\n"
        
        message += "Which of these tempts your palate, or would you like me to tell you more about a specific dish?"
        
        return AgentResponse(
            action="menu_inquiry",
            message=message,
            data={'menu_items': menu_items}
        )
    
    def _suggest_pairing(self, main_dish: str) -> str:
        """Suggest wine or side pairing"""
        pairings = {
            'paella': 'crisp Albariño wine and saffron aioli',
            'lamb': 'robust Malbec and truffle mashed potatoes',
            'sea bass': 'Chardonnay and roasted Mediterranean vegetables',
            'chicken': 'Sauvignon Blanc and herb-crusted focaccia',
            'beef': 'Cabernet Sauvignon and garlic butter asparagus'
        }
        
        main_lower = main_dish.lower()
        for key, pairing in pairings.items():
            if key in main_lower:
                return pairing
        
        return "our sommelier's wine selection"
    
    def _handle_booking_inquiry(self, query: str) -> AgentResponse:
        """Handle reservation requests warmly"""
        # Check for booking ID in query
        booking_id_match = re.search(r'BK\d+', query.upper())
        
        if booking_id_match:
            return self._get_booking_details(booking_id_match.group())
        
        # New reservation request
        name_part = f"{self.context['guest_name']}, " if self.context['guest_name'] else ""
        
        message = f"Certainly, {name_part}I'd be delighted to help you reserve a table!\n\n"
        
        if self.context['celebration']:
            message += f"I've noted this is for your {self.context['celebration']} - how special! "
            message += "Would you like me to arrange something extra to make it memorable? "
            message += "Perhaps a complimentary champagne toast or a quieter corner table for intimacy?\n\n"
        
        message += "To secure the perfect table for you, I'll need just a few details:\n"
        message += "📅 What date works best for you?\n"
        message += "🕐 What time would you prefer?\n"
        message += "👥 How many guests will be joining you?\n\n"
        
        message += "Also, do you have any seating preferences? We have:\n"
        message += "• Cozy booths perfect for intimate conversations\n"
        message += "• Window tables with beautiful city views\n"
        message += "• Outdoor patio for a lovely Mediterranean ambiance\n\n"
        
        message += "You can provide these details here, or I can direct you to our quick booking form!"
        
        return AgentResponse(
            action="booking_inquiry",
            message=message,
            data=self.context
        )
    
    def _get_booking_details(self, booking_id: str) -> AgentResponse:
        """Retrieve booking with warm, conversational tone"""
        from database import get_booking
        
        booking = get_booking(booking_id)
        
        if booking:
            message = f"Wonderful! I found your reservation!\n\n"
            message += f"**Booking #{booking['id']}**\n\n"
            message += f"👤 **Guest:** {booking['customer']}\n"
            message += f"📅 **Date:** {booking['date']}\n"
            message += f"🕐 **Time:** {booking['time']}\n"
            message += f"👥 **Party size:** {booking['guests']} guests\n"
            message += f"🪑 **Table:** {booking.get('table_pref', 'Any available')}\n"
            message += f"✨ **Status:** {booking['status'].title()}\n\n"
            
            if booking['status'] == 'confirmed':
                message += "Everything looks perfect! We're looking forward to welcoming you. "
                message += "Is there anything special you'd like us to prepare for your visit? "
                message += "Any dietary preferences or special requests?\n\n"
                message += "*We send a reminder 24 hours before your reservation.*"
            else:
                message += "I see this booking has been cancelled. "
                message += "Would you like me to help you make a new reservation? "
                message += "I'd be happy to find you the perfect table!"
            
            return AgentResponse(
                action="booking_found",
                message=message,
                data=booking
            )
        else:
            message = f"Hmm, I'm not finding booking {booking_id} in our system at the moment.\n\n"
            message += "This could mean:\n"
            message += "• The booking ID might have a small typo\n"
            message += "• It may have been made under a different confirmation number\n\n"
            message += "No worries though! I'm here to help. You could:\n"
            message += "1️⃣ Double-check the booking ID from your confirmation email\n"
            message += "2️⃣ Let me know your name and date, and I can search that way\n"
            message += "3️⃣ Call us at +1 (555) 123-4567 and our team will locate it immediately\n\n"
            message += "What works best for you?"
            
            return AgentResponse(
                action="booking_not_found",
                message=message,
                data=None
            )
    
    def _handle_hours_inquiry(self) -> AgentResponse:
        """Provide hours with inviting tone"""
        message = "I'm so glad you asked! We're open and ready to serve you:\n\n"
        message += "**🕐 Our Hours:**\n"
        message += "• Monday - Thursday: 11:00 AM - 10:00 PM\n"
        message += "• Friday - Saturday: 11:00 AM - 11:00 PM *(Perfect for weekend celebrations!)*\n"
        message += "• Sunday: 12:00 PM - 9:00 PM *(Lovely for family brunch)*\n\n"
        message += "📍 **Location:** 123 Restaurant Street, Food City\n"
        message += "📞 **Phone:** +1 (555) 123-4567\n\n"
        message += "We're especially lively during our happy hour (4-6 PM, weekdays) where our bar menu shines!\n\n"
        message += "Would you like to make a reservation, or can I help you with anything else?"
        
        return AgentResponse(
            action="hours_inquiry",
            message=message,
            data=None
        )
    
    def _handle_complaint(self, query: str) -> AgentResponse:
        """Handle complaints with empathy and solutions"""
        message = "I'm truly sorry to hear you're experiencing an issue. Your satisfaction means everything to us, and I want to make this right immediately.\n\n"
        message += "Please know that I'm taking your concern very seriously. Could you share a bit more detail about what happened? "
        message += "This will help me find the best solution for you.\n\n"
        message += "**What I can do right now:**\n"
        message += "• Connect you with our manager for immediate assistance\n"
        message += "• Arrange for a fresh preparation of your dish\n"
        message += "• Apply a courtesy adjustment to your bill\n"
        message += "• Ensure this is documented so it never happens again\n\n"
        message += "Your feedback helps us improve, and I genuinely appreciate you bringing this to our attention. "
        message += "How can I make this better for you right now?"
        
        return AgentResponse(
            action="complaint_handling",
            message=message,
            data={'escalate': True}
        )
    
    def _handle_gratitude(self) -> AgentResponse:
        """Respond warmly to thanks"""
        responses = [
            "My absolute pleasure! It's been wonderful assisting you.",
            "You're so welcome! I'm delighted I could help.",
            "The pleasure is all mine! That's what I'm here for.",
        ]
        
        import random
        base_message = random.choice(responses)
        
        message = f"{base_message}\n\n"
        
        if self.context['guest_name']:
            message += f"{self.context['guest_name']}, "
        
        message += "is there anything else I can help you with today? "
        message += "I'm always here to make your {self.restaurant_name} experience exceptional! 😊"
        
        return AgentResponse(
            action="gratitude_response",
            message=message,
            data=None
        )
    
    def _handle_general_query(self) -> AgentResponse:
        """Handle unclear queries with helpful guidance"""
        message = "I want to make sure I give you exactly the information you need!\n\n"
        message += "I'm your personal dining assistant, and I can help you with:\n\n"
        message += "**🍽️ Menu & Recommendations**\n"
        message += "Ask me: *'What do you recommend?'* or *'Tell me about your specials'*\n\n"
        message += "**📅 Reservations**\n"
        message += "Say: *'I'd like to book a table'* or *'Check my booking BK123456'*\n\n"
        message += "**🎉 Special Occasions**\n"
        message += "Let me know: *'It's our anniversary'* and I'll make it magical\n\n"
        message += "**ℹ️ Restaurant Information**\n"
        message += "Ask: *'What are your hours?'* or *'Where are you located?'*\n\n"
        message += "What can I help you with today?"
        
        return AgentResponse(
            action="general_response",
            message=message,
            data=None
        )

# Maintain backward compatibility
RestaurantAssistantAgent = GastroGuideAgent