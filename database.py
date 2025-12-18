import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

DATABASE_PATH = 'restaurant.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with tables and sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id TEXT PRIMARY KEY,
            customer TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            guests INTEGER NOT NULL,
            table_pref TEXT,
            status TEXT DEFAULT 'confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create menu items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image TEXT,
            available BOOLEAN DEFAULT 1
        )
    ''')
    
    # Insert sample bookings
    sample_bookings = [
        ("BK001", "Ajeet Gupta", "ajeetgupta80045@gmail.com", "+91 8787095611", "2025-12-18", "19:00", 4, "Window-5", "confirmed"),
        ("BK002", "Shiv Bhukta", "shivbhukta@gmail.com", "+91 9876565463", "2025-12-18", "20:30", 2, "Booth-3", "confirmed"),
    ]
    
    for booking in sample_bookings:
        cursor.execute('''
            INSERT OR IGNORE INTO bookings 
            (id, customer, email, phone, date, time, guests, table_pref, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', booking)
    
    # Insert sample menu items
    sample_menu = [
        # Appetizers
        ("Mediterranean Mezze Platter", "Appetizers", "Hummus, baba ganoush, tzatziki, olives, and pita bread", 12.99, "mezze.jpg"),
        ("Crispy Calamari", "Appetizers", "Lightly fried squid rings with aioli dipping sauce", 14.99, "mezze.jpg"),
        ("Bruschetta Trio", "Appetizers", "Classic tomato, mushroom pâté, and olive tapenade", 10.99, "mezze.jpg"),
        
        # Main Course
        ("Seafood Paella", "Main Course", "Traditional Spanish rice dish with prawns, mussels, and saffron", 28.99, "paella.jpg"),
        ("Lamb Tagine", "Main Course", "Slow-cooked Moroccan lamb with apricots and almonds", 26.99, "tagine.jpg"),
        ("Grilled Sea Bass", "Main Course", "Fresh Mediterranean sea bass with lemon herb butter", 32.99, "seabass.jpg"),
        ("Mushroom Risotto", "Main Course", "Creamy arborio rice with wild mushrooms and parmesan", 22.99, "risotto.jpg"),
        
        # Desserts
        ("Baklava", "Desserts", "Layered phyllo pastry with honey and pistachios", 8.99, "baklava.jpg"),
        ("Tiramisu", "Desserts", "Classic Italian coffee-flavored dessert", 9.99, "baklava.jpg"),
        ("Chocolate Lava Cake", "Desserts", "Warm chocolate cake with molten center and vanilla ice cream", 10.99, "baklava.jpg"),
        
        # Drinks
        ("Fresh Lemonade", "Drinks", "Homemade mint lemonade", 4.99, "mezze.jpg"),
        ("Turkish Coffee", "Drinks", "Traditional strong coffee", 5.99, "mezze.jpg"),
        ("House Sangria", "Drinks", "Red wine with fresh fruits", 8.99, "mezze.jpg"),
    ]
    
    for item in sample_menu:
        cursor.execute('''
            INSERT OR IGNORE INTO menu_items 
            (name, category, description, price, image)
            VALUES (?, ?, ?, ?, ?)
        ''', item)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

# Booking operations
def get_booking(booking_id: str) -> Optional[Dict]:
    """Get booking by ID"""
    conn = get_db_connection()
    booking = conn.execute(
        'SELECT * FROM bookings WHERE id = ?', (booking_id,)
    ).fetchone()
    conn.close()
    return dict(booking) if booking else None

def create_booking(booking_data: Dict) -> Dict:
    """Create new booking"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate UNIQUE booking ID using timestamp and random number
    import random
    import time
    timestamp = int(time.time() * 1000) % 10000  # Last 4 digits of millisecond timestamp
    random_num = random.randint(100, 999)
    booking_id = f"BK{timestamp}{random_num}"
    
    # Ensure uniqueness by checking database
    while cursor.execute('SELECT id FROM bookings WHERE id = ?', (booking_id,)).fetchone():
        random_num = random.randint(100, 999)
        booking_id = f"BK{timestamp}{random_num}"
    
    cursor.execute('''
        INSERT INTO bookings 
        (id, customer, email, phone, date, time, guests, table_pref, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        booking_id,
        booking_data.get('customer'),
        booking_data.get('email'),
        booking_data.get('phone'),
        booking_data.get('date'),
        booking_data.get('time'),
        booking_data.get('guests'),
        booking_data.get('table_pref', 'Any'),
        'confirmed'
    ))
    
    conn.commit()
    conn.close()
    
    # Get the created booking
    booking = get_booking(booking_id)
    
    # Send confirmation email
    try:
        from email_service import email_service
        email_service.send_booking_confirmation(booking)
    except Exception as e:
        print(f"Warning: Could not send confirmation email: {e}")
    
    return booking

def delete_booking(booking_id: str) -> bool:
    """Cancel/delete booking"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE bookings SET status = 'cancelled' WHERE id = ?", 
        (booking_id,)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

# Menu operations
def get_all_menu_items() -> List[Dict]:
    """Get all menu items"""
    conn = get_db_connection()
    items = conn.execute(
        'SELECT * FROM menu_items WHERE available = 1 ORDER BY category, name'
    ).fetchall()
    conn.close()
    return [dict(item) for item in items]

def get_menu_by_category(category: str) -> List[Dict]:
    """Get menu items by category"""
    conn = get_db_connection()
    items = conn.execute(
        'SELECT * FROM menu_items WHERE category = ? AND available = 1',
        (category,)
    ).fetchall()
    conn.close()
    return [dict(item) for item in items]

if __name__ == "__main__":
    init_database()
