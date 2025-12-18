#!/usr/bin/env python3
"""
Flask Web Application for Restaurant with AI Agent
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from agent import RestaurantAssistantAgent
from database import init_database, get_booking, create_booking, delete_booking, get_all_menu_items

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Initialize AI Agent
ai_agent = RestaurantAssistantAgent()

# Initialize database on first run
if not os.path.exists('restaurant.db'):
    init_database()

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# API Routes

@app.route('/api/menu', methods=['GET'])
def get_menu():
    """Get all menu items"""
    try:
        items = get_all_menu_items()
        return jsonify({
            'success': True,
            'menu': items
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bookings/<booking_id>', methods=['GET'])
def get_booking_details(booking_id):
    """Get booking by ID"""
    try:
        booking = get_booking(booking_id)
        if booking:
            return jsonify({
                'success': True,
                'booking': booking
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Booking not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bookings', methods=['POST'])
def create_new_booking():
    """Create new booking"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer', 'date', 'time', 'guests']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        booking = create_booking(data)
        return jsonify({
            'success': True,
            'booking': booking,
            'message': 'Booking created successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/bookings', methods=['GET'])
def get_all_bookings():
    """Get all bookings for admin dashboard"""
    try:
        from database import get_db_connection
        conn = get_db_connection()
        bookings = conn.execute(
            'SELECT * FROM bookings ORDER BY created_at DESC'
        ).fetchall()
        conn.close()
        
        bookings_list = [dict(booking) for booking in bookings]
        
        return jsonify({
            'success': True,
            'bookings': bookings_list,
            'count': len(bookings_list)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bookings/<booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    """Cancel booking"""
    try:
        success = delete_booking(booking_id)
        if success:
            return jsonify({
                'success': True,
                'message': f'Booking {booking_id} cancelled successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Booking not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_agent():
    """Chat with AI Agent"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        context = data.get('context', [])
        
        # Process query with AI agent
        response = ai_agent.process_query(user_message, context)
        
        return jsonify({
            'success': True,
            'response': {
                'action': response.action,
                'message': response.message,
                'data': response.data,
                'needs_confirmation': response.needs_confirmation
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'response': {
                'action': 'error',
                'message': 'Sorry, I encountered an error. Please try again.',
                'data': None,
                'needs_confirmation': False
            }
        }), 500

@app.route('/api/info', methods=['GET'])
def get_info():
    """Get restaurant information"""
    info = {
        'name': 'Mediterranean Delight',
        'description': 'Authentic Mediterranean cuisine with a modern twist',
        'hours': {
            'monday_thursday': '11:00 AM - 10:00 PM',
            'friday_saturday': '11:00 AM - 11:00 PM',
            'sunday': '12:00 PM - 9:00 PM'
        },
        'location': '123 Restaurant Street, Food City',
        'phone': '+1 (555) 123-4567',
        'email': 'info@mediterraneandelight.com'
    }
    return jsonify({
        'success': True,
        'info': info
    })

if __name__ == '__main__':
    print("Starting Restaurant Web Application...")
    print("Server running at: http://localhost:5000")
    print("AI Agent (GastroGuide) enabled and ready!")
    app.run(debug=True, host='0.0.0.0', port=5000)
