// Shopping Cart System

class ShoppingCart {
    constructor() {
        this.items = this.loadCart();
        this.init();
    }

    init() {
        this.createCartUI();
        this.attachEventListeners();
        this.updateCartDisplay();
    }

    loadCart() {
        const saved = localStorage.getItem('restaurantCart');
        return saved ? JSON.parse(saved) : [];
    }

    saveCart() {
        localStorage.setItem('restaurantCart', JSON.stringify(this.items));
        this.updateCartDisplay();
    }

    createCartUI() {
        const cartHTML = `
            <!-- Cart Button -->
            <button class="cart-button" id="cart-button">
                🛒
                <span class="cart-badge" id="cart-badge">0</span>
            </button>

            <!-- Cart Sidebar -->
            <div class="cart-sidebar" id="cart-sidebar">
                <div class="cart-header">
                    <h3>🛒 Your Order</h3>
                    <button class="cart-close" id="cart-close">✕</button>
                </div>

                <div class="cart-items" id="cart-items">
                    <!-- Cart items will be added here -->
                </div>

                <div class="cart-summary">
                    <div class="cart-summary-row">
                        <span>Subtotal:</span>
                        <span id="cart-subtotal">$0.00</span>
                    </div>
                    <div class="cart-summary-row" id="discount-row" style="display: none;">
                        <span>Discount (10%): <span class="discount-badge">Orders > $500</span></span>
                        <span id="cart-discount" style="color: var(--success);">-$0.00</span>
                    </div>
                    <div class="cart-summary-row total">
                        <span>Total:</span>
                        <span id="cart-total">$0.00</span>
                    </div>
                    <button class="checkout-btn" id="checkout-btn">
                        Proceed to Checkout
                    </button>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', cartHTML);
    }

    attachEventListeners() {
        document.getElementById('cart-button').addEventListener('click', () => this.toggleCart());
        document.getElementById('cart-close').addEventListener('click', () => this.closeCart());
        document.getElementById('checkout-btn').addEventListener('click', () => this.checkout());
    }

    toggleCart() {
        document.getElementById('cart-sidebar').classList.toggle('active');
    }

    closeCart() {
        document.getElementById('cart-sidebar').classList.remove('active');
    }

    addItem(item) {
        const existingItem = this.items.find(i => i.id === item.id);

        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.items.push({
                ...item,
                quantity: 1
            });
        }

        this.saveCart();
        this.showNotification(`${item.name} added to cart!`);
    }

    removeItem(itemId) {
        this.items = this.items.filter(item => item.id !== itemId);
        this.saveCart();
    }

    updateQuantity(itemId, change) {
        const item = this.items.find(i => i.id === itemId);
        if (item) {
            item.quantity += change;
            if (item.quantity <= 0) {
                this.removeItem(itemId);
            } else {
                this.saveCart();
            }
        }
    }

    calculateTotals() {
        const subtotal = this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);

        // Apply 10% discount if subtotal > $500
        const discount = subtotal > 500 ? subtotal * 0.10 : 0;
        const total = subtotal - discount;

        return { subtotal, discount, total };
    }

    updateCartDisplay() {
        const itemsContainer = document.getElementById('cart-items');
        const badge = document.getElementById('cart-badge');
        const { subtotal, discount, total } = this.calculateTotals();

        // Update badge
        const totalItems = this.items.reduce((sum, item) => sum + item.quantity, 0);
        badge.textContent = totalItems;
        badge.style.display = totalItems > 0 ? 'flex' : 'none';

        // Update items display
        if (this.items.length === 0) {
            itemsContainer.innerHTML = `
                <div class="empty-cart">
                    <div class="empty-cart-icon">🛒</div>
                    <p>Your cart is empty</p>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;">Add some delicious items from our menu!</p>
                </div>
            `;
        } else {
            itemsContainer.innerHTML = this.items.map(item => `
                <div class="cart-item">
                    <img src="/images/${item.image}" alt="${item.name}" class="cart-item-image" 
                         onerror="this.style.background='linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%)'; this.src='';">
                    <div class="cart-item-details">
                        <div class="cart-item-name">${item.name}</div>
                        <div class="cart-item-price">$${item.price.toFixed(2)}</div>
                        <div class="cart-item-quantity">
                            <button class="qty-btn" onclick="cart.updateQuantity(${item.id}, -1)">−</button>
                            <span class="qty-display">${item.quantity}</span>
                            <button class="qty-btn" onclick="cart.updateQuantity(${item.id}, 1)">+</button>
                            <button class="remove-item" onclick="cart.removeItem(${item.id})">Remove</button>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        // Update summary
        document.getElementById('cart-subtotal').textContent = `$${subtotal.toFixed(2)}`;
        document.getElementById('cart-total').textContent = `$${total.toFixed(2)}`;

        // Show/hide discount
        const discountRow = document.getElementById('discount-row');
        if (discount > 0) {
            discountRow.style.display = 'flex';
            document.getElementById('cart-discount').textContent = `-$${discount.toFixed(2)}`;
        } else {
            discountRow.style.display = 'none';
        }

        // Enable/disable checkout
        document.getElementById('checkout-btn').disabled = this.items.length === 0;
    }

    showNotification(message) {
        // Create toast notification
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 100px;
            right: 30px;
            background: var(--success);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            z-index: 10001;
            animation: slideIn 0.3s ease;
        `;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    }

    checkout() {
        const { total } = this.calculateTotals();

        // Store cart data for checkout page
        localStorage.setItem('checkoutCart', JSON.stringify({
            items: this.items,
            ...this.calculateTotals()
        }));

        // Redirect to booking page with cart
        window.location.href = '/booking.html?checkout=true';
    }

    clearCart() {
        this.items = [];
        this.saveCart();
    }
}

// Initialize cart
let cart;
document.addEventListener('DOMContentLoaded', () => {
    cart = new ShoppingCart();
});
