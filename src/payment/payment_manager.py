"""
Payment Manager for AstroKnowledge
Handles credits, transactions, and UPI payment generation
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import qrcode
from io import BytesIO


class PaymentManager:
    """Manage user credits and payments"""
    
    def __init__(self, data_dir: str = "data/payments", config: dict = None):
        """Initialize payment manager"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.credits_file = self.data_dir / "user_credits.json"
        self.transactions_file = self.data_dir / "transactions.json"
        self.coupon_usage_file = self.data_dir / "coupon_usage.json"
        self.config = config or {}
        
        # Load existing data
        self.credits = self._load_credits()
        self.transactions = self._load_transactions()
        self.coupon_usage = self._load_coupon_usage()
    
    def _load_credits(self) -> Dict:
        """Load user credits from file"""
        if self.credits_file.exists():
            with open(self.credits_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_credits(self):
        """Save user credits to file"""
        with open(self.credits_file, 'w', encoding='utf-8') as f:
            json.dump(self.credits, f, indent=2, ensure_ascii=False)
    
    def _load_transactions(self) -> List:
        """Load transaction history from file"""
        if self.transactions_file.exists():
            with open(self.transactions_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_transactions(self):
        """Save transaction history to file"""
        with open(self.transactions_file, 'w', encoding='utf-8') as f:
            json.dump(self.transactions, f, indent=2, ensure_ascii=False)
    
    def _load_coupon_usage(self) -> Dict:
        """Load coupon usage tracking from file"""
        if self.coupon_usage_file.exists():
            with open(self.coupon_usage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_coupon_usage(self):
        """Save coupon usage tracking to file"""
        with open(self.coupon_usage_file, 'w', encoding='utf-8') as f:
            json.dump(self.coupon_usage, f, indent=2, ensure_ascii=False)
    
    def get_user_credits(self, user_email: str) -> int:
        """Get credits balance for a user"""
        return self.credits.get(user_email, 0)
    
    def add_credits(self, user_email: str, amount: int, transaction_id: str, 
                   payment_method: str = "UPI", notes: str = ""):
        """Add credits to user account"""
        current_credits = self.get_user_credits(user_email)
        new_credits = current_credits + amount
        
        self.credits[user_email] = new_credits
        self._save_credits()
        
        # Record transaction
        transaction = {
            'transaction_id': transaction_id,
            'user_email': user_email,
            'credits_added': amount,
            'payment_method': payment_method,
            'timestamp': datetime.now().isoformat(),
            'notes': notes,
            'status': 'completed'
        }
        self.transactions.append(transaction)
        self._save_transactions()
        
        return new_credits
    
    def deduct_credits(self, user_email: str, amount: int, reason: str = ""):
        """Deduct credits from user account"""
        current_credits = self.get_user_credits(user_email)
        
        if current_credits < amount:
            return False, "Insufficient credits"
        
        new_credits = current_credits - amount
        self.credits[user_email] = new_credits
        self._save_credits()
        
        # Record usage
        transaction = {
            'transaction_id': f"USE_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'user_email': user_email,
            'credits_used': amount,
            'timestamp': datetime.now().isoformat(),
            'reason': reason,
            'status': 'completed'
        }
        self.transactions.append(transaction)
        self._save_transactions()
        
        return True, new_credits
    
    def get_user_transactions(self, user_email: str) -> List:
        """Get transaction history for a user"""
        return [t for t in self.transactions if t.get('user_email') == user_email]
    
    def generate_upi_payment_string(self, upi_id: str, name: str, amount: float, 
                                   transaction_note: str = "") -> str:
        """Generate UPI payment string"""
        # UPI URI format: upi://pay?pa=UPI_ID&pn=NAME&am=AMOUNT&cu=INR&tn=NOTE
        upi_string = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
        if transaction_note:
            upi_string += f"&tn={transaction_note.replace(' ', '%20')}"
        return upi_string
    
    def generate_upi_qr_code(self, upi_id: str, name: str, amount: float, 
                            transaction_note: str = "") -> BytesIO:
        """Generate UPI QR code for payment"""
        upi_string = self.generate_upi_payment_string(upi_id, name, amount, transaction_note)
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(upi_string)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes
    
    def verify_transaction(self, transaction_id: str, user_email: str, 
                          credits: int, admin_verified: bool = False):
        """Verify and complete a pending transaction"""
        # Check if transaction already exists
        existing = [t for t in self.transactions 
                   if t.get('transaction_id') == transaction_id]
        
        if existing:
            return False, "Transaction ID already used"
        
        # Add credits
        new_balance = self.add_credits(
            user_email=user_email,
            amount=credits,
            transaction_id=transaction_id,
            payment_method="UPI",
            notes="Verified" if admin_verified else "Self-reported"
        )
        
        return True, new_balance
    
    def validate_coupon(self, coupon_code: str, user_email: str, 
                       feature: str = None) -> Tuple[bool, str, int]:
        """
        Validate a coupon code
        Returns: (is_valid, message, discount_percent)
        """
        # Check if coupon system is enabled
        coupons_config = self.config.get('payment', {}).get('coupons', {})
        if not coupons_config.get('enabled', False):
            return False, "Coupon system is disabled", 0
        
        # Find coupon
        coupon = None
        for c in coupons_config.get('codes', []):
            if c.get('code', '').upper() == coupon_code.upper():
                coupon = c
                break
        
        if not coupon:
            return False, "Invalid coupon code", 0
        
        # Check max uses
        coupon_id = coupon['code']
        usage_count = self.coupon_usage.get(coupon_id, {}).get('total_uses', 0)
        max_uses = coupon.get('max_uses')
        if max_uses and usage_count >= max_uses:
            return False, "Coupon usage limit reached", 0
        
        # Check user-specific usage
        user_usage = self.coupon_usage.get(coupon_id, {}).get('users', {}).get(user_email, [])
        
        # Check first purchase only
        if coupon.get('first_purchase_only', False):
            user_transactions = [t for t in self.transactions if t.get('user_email') == user_email]
            if len(user_transactions) > 0:
                return False, "This coupon is only valid for first purchase", 0
        
        # Check date range
        valid_from = coupon.get('valid_from')
        valid_until = coupon.get('valid_until')
        now = datetime.now()
        
        if valid_from:
            from_date = datetime.strptime(valid_from, '%Y-%m-%d')
            if now < from_date:
                return False, f"Coupon valid from {valid_from}", 0
        
        if valid_until:
            until_date = datetime.strptime(valid_until, '%Y-%m-%d')
            if now > until_date:
                return False, "Coupon expired", 0
        
        # Check valid days
        valid_days = coupon.get('valid_days')
        if valid_days:
            current_day = now.strftime('%A')
            if current_day not in valid_days:
                return False, f"Coupon valid only on: {', '.join(valid_days)}", 0
        
        # Check feature restriction
        restricted_features = coupon.get('features')
        if restricted_features and feature:
            if feature not in restricted_features:
                return False, f"Coupon valid only for: {', '.join(restricted_features)}", 0
        
        discount = coupon.get('discount_percent', 0)
        description = coupon.get('description', 'Discount applied')
        
        return True, description, discount
    
    def apply_coupon(self, coupon_code: str, user_email: str, 
                    original_price: int, feature: str = None) -> Tuple[bool, int, str]:
        """
        Apply coupon and return discounted price
        Returns: (success, final_price, message)
        """
        is_valid, message, discount_percent = self.validate_coupon(
            coupon_code, user_email, feature
        )
        
        if not is_valid:
            return False, original_price, message
        
        # Calculate discounted price
        discount_amount = int((original_price * discount_percent) / 100)
        final_price = original_price - discount_amount
        
        # Track coupon usage
        coupon_id = coupon_code.upper()
        if coupon_id not in self.coupon_usage:
            self.coupon_usage[coupon_id] = {
                'total_uses': 0,
                'users': {}
            }
        
        self.coupon_usage[coupon_id]['total_uses'] += 1
        
        if user_email not in self.coupon_usage[coupon_id]['users']:
            self.coupon_usage[coupon_id]['users'][user_email] = []
        
        self.coupon_usage[coupon_id]['users'][user_email].append({
            'timestamp': datetime.now().isoformat(),
            'feature': feature,
            'original_price': original_price,
            'discount_percent': discount_percent,
            'final_price': final_price
        })
        
        self._save_coupon_usage()
        
        success_msg = f"{message} - {discount_percent}% off! Pay ₹{final_price} instead of ₹{original_price}"
        return True, final_price, success_msg
    
    def get_active_coupons(self) -> List[Dict]:
        """Get list of currently active coupons"""
        coupons_config = self.config.get('payment', {}).get('coupons', {})
        if not coupons_config.get('enabled', False):
            return []
        
        active_coupons = []
        now = datetime.now()
        
        for coupon in coupons_config.get('codes', []):
            # Check date validity
            valid_from = coupon.get('valid_from')
            valid_until = coupon.get('valid_until')
            
            is_valid = True
            if valid_from:
                from_date = datetime.strptime(valid_from, '%Y-%m-%d')
                if now < from_date:
                    is_valid = False
            
            if valid_until:
                until_date = datetime.strptime(valid_until, '%Y-%m-%d')
                if now > until_date:
                    is_valid = False
            
            # Check usage limits
            coupon_id = coupon['code']
            usage_count = self.coupon_usage.get(coupon_id, {}).get('total_uses', 0)
            max_uses = coupon.get('max_uses')
            if max_uses and usage_count >= max_uses:
                is_valid = False
            
            if is_valid:
                active_coupons.append({
                    'code': coupon['code'],
                    'discount': coupon.get('discount_percent', 0),
                    'description': coupon.get('description', ''),
                    'features': coupon.get('features', []),
                    'valid_days': coupon.get('valid_days', []),
                    'remaining_uses': max_uses - usage_count if max_uses else None
                })
        
        return active_coupons
