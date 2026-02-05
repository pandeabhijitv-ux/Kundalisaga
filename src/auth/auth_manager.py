"""
Authentication Manager
Handles user registration, login, email OTP, and Google OAuth
"""
import json
import hashlib
import secrets
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import bcrypt

from src.utils import logger


@dataclass
class User:
    """User account data"""
    email: str
    name: str
    password_hash: str
    created_at: str
    last_login: Optional[str] = None
    email_verified: bool = False
    google_id: Optional[str] = None


@dataclass
class OTPCode:
    """OTP code data"""
    email: str
    code: str
    expires_at: str
    created_at: str


class AuthManager:
    """Manages user authentication"""
    
    def __init__(self, users_dir: str = "data/users"):
        self.users_dir = Path(users_dir)
        self.users_dir.mkdir(parents=True, exist_ok=True)
        
        self.users_file = self.users_dir / "users.json"
        self.otp_file = self.users_dir / "otp_codes.json"
        self.sessions_file = self.users_dir / "sessions.json"
        
        self.logger = logger
        
        # Initialize files if they don't exist
        self._init_storage()
    
    def _init_storage(self):
        """Initialize storage files"""
        if not self.users_file.exists():
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not self.otp_file.exists():
            with open(self.otp_file, 'w') as f:
                json.dump({}, f)
        
        if not self.sessions_file.exists():
            with open(self.sessions_file, 'w') as f:
                json.dump({}, f)
    
    def _load_users(self) -> Dict[str, Dict]:
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_users(self, users: Dict[str, Dict]):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def _load_otps(self) -> Dict[str, Dict]:
        """Load OTP codes from file"""
        try:
            with open(self.otp_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_otps(self, otps: Dict[str, Dict]):
        """Save OTP codes to file"""
        with open(self.otp_file, 'w') as f:
            json.dump(otps, f, indent=2)
    
    def _load_sessions(self) -> Dict[str, Dict]:
        """Load sessions from file"""
        try:
            with open(self.sessions_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_sessions(self, sessions: Dict[str, Dict]):
        """Save sessions to file"""
        with open(self.sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def _generate_otp(self) -> str:
        """Generate 6-digit OTP"""
        return str(secrets.randbelow(1000000)).zfill(6)
    
    def _generate_session_token(self) -> str:
        """Generate unique session token"""
        return secrets.token_urlsafe(32)
    
    def register_user(self, email: str, password: str, name: str) -> Tuple[bool, str]:
        """
        Register a new user
        
        Returns:
            Tuple of (success, message)
        """
        # Validate email
        if not self._validate_email(email):
            return False, "Invalid email format"
        
        # Validate password strength
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Check if user exists
        users = self._load_users()
        if email.lower() in users:
            return False, "Email already registered"
        
        # Create user
        user = User(
            email=email.lower(),
            name=name,
            password_hash=self._hash_password(password),
            created_at=datetime.now().isoformat(),
            email_verified=False
        )
        
        users[email.lower()] = asdict(user)
        self._save_users(users)
        
        self.logger.info(f"User registered: {email}")
        return True, "Registration successful! Please login."
    
    def login_with_password(self, email: str, password: str) -> Tuple[bool, str, Optional[str]]:
        """
        Login with email and password
        
        Returns:
            Tuple of (success, message, session_token)
        """
        users = self._load_users()
        
        email = email.lower()
        if email not in users:
            return False, "Email not found", None
        
        user = users[email]
        
        if not self._verify_password(password, user['password_hash']):
            return False, "Incorrect password", None
        
        # Create session
        session_token = self._generate_session_token()
        sessions = self._load_sessions()
        
        sessions[session_token] = {
            'email': email,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(minutes=30)).isoformat()
        }
        self._save_sessions(sessions)
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        users[email] = user
        self._save_users(users)
        
        self.logger.info(f"User logged in: {email}")
        return True, "Login successful!", session_token
    
    def send_otp(self, email: str) -> Tuple[bool, str]:
        """
        Generate and send OTP to email
        
        Returns:
            Tuple of (success, message/otp_code)
        """
        users = self._load_users()
        
        email = email.lower()
        if email not in users:
            return False, "Email not found"
        
        # Generate OTP
        otp_code = self._generate_otp()
        
        otps = self._load_otps()
        otps[email] = {
            'code': otp_code,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(minutes=5)).isoformat()
        }
        self._save_otps(otps)
        
        self.logger.info(f"OTP generated for {email}: {otp_code}")
        
        # In production, send email here
        # For now, return the OTP code for testing
        return True, otp_code
    
    def verify_otp(self, email: str, otp_code: str) -> Tuple[bool, str, Optional[str]]:
        """
        Verify OTP and create session
        
        Returns:
            Tuple of (success, message, session_token)
        """
        otps = self._load_otps()
        
        email = email.lower()
        if email not in otps:
            return False, "No OTP found for this email", None
        
        otp_data = otps[email]
        
        # Check expiration
        expires_at = datetime.fromisoformat(otp_data['expires_at'])
        if datetime.now() > expires_at:
            del otps[email]
            self._save_otps(otps)
            return False, "OTP expired", None
        
        # Verify code
        if otp_data['code'] != otp_code:
            return False, "Incorrect OTP", None
        
        # OTP valid - create session
        session_token = self._generate_session_token()
        sessions = self._load_sessions()
        
        sessions[session_token] = {
            'email': email,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(minutes=30)).isoformat()
        }
        self._save_sessions(sessions)
        
        # Update last login
        users = self._load_users()
        if email in users:
            users[email]['last_login'] = datetime.now().isoformat()
            self._save_users(users)
        
        # Remove used OTP
        del otps[email]
        self._save_otps(otps)
        
        self.logger.info(f"OTP verified for {email}")
        return True, "Login successful!", session_token
    
    def register_with_google(self, email: str, name: str, google_id: str) -> Tuple[bool, str, Optional[str]]:
        """
        Register or login user with Google OAuth
        
        Returns:
            Tuple of (success, message, session_token)
        """
        users = self._load_users()
        email = email.lower()
        
        # Check if user exists
        if email in users:
            user = users[email]
            # Update Google ID if not set
            if not user.get('google_id'):
                user['google_id'] = google_id
                users[email] = user
                self._save_users(users)
        else:
            # Create new user
            user = User(
                email=email,
                name=name,
                password_hash="",  # No password for OAuth users
                created_at=datetime.now().isoformat(),
                email_verified=True,  # Google emails are verified
                google_id=google_id
            )
            users[email] = asdict(user)
            self._save_users(users)
        
        # Create session
        session_token = self._generate_session_token()
        sessions = self._load_sessions()
        
        sessions[session_token] = {
            'email': email,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(minutes=30)).isoformat()
        }
        self._save_sessions(sessions)
        
        # Update last login
        users[email]['last_login'] = datetime.now().isoformat()
        self._save_users(users)
        
        self.logger.info(f"Google OAuth login: {email}")
        return True, "Login successful!", session_token
    
    def validate_session(self, session_token: str) -> Tuple[bool, Optional[str]]:
        """
        Validate session token and return user email
        
        Returns:
            Tuple of (valid, email)
        """
        sessions = self._load_sessions()
        
        if session_token not in sessions:
            return False, None
        
        session = sessions[session_token]
        
        # Check expiration
        expires_at = datetime.fromisoformat(session['expires_at'])
        if datetime.now() > expires_at:
            del sessions[session_token]
            self._save_sessions(sessions)
            return False, None
        
        return True, session['email']
    
    def logout(self, session_token: str) -> bool:
        """Logout user and invalidate session"""
        sessions = self._load_sessions()
        
        if session_token in sessions:
            email = sessions[session_token]['email']
            del sessions[session_token]
            self._save_sessions(sessions)
            self.logger.info(f"User logged out: {email}")
            return True
        
        return False
    
    def get_user(self, email: str) -> Optional[Dict]:
        """Get user data by email"""
        users = self._load_users()
        return users.get(email.lower())
    
    def update_user(self, email: str, user_data: Dict) -> Tuple[bool, str]:
        """
        Update user data
        
        Args:
            email: User email
            user_data: Updated user data dictionary
        
        Returns:
            Tuple of (success, message)
        """
        users = self._load_users()
        email_lower = email.lower()
        
        if email_lower not in users:
            return False, "User not found"
        
        # Update user data
        users[email_lower].update(user_data)
        self._save_users(users)
        
        self.logger.info(f"Updated user data for: {email}")
        return True, "User updated successfully"
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        sessions = self._load_sessions()
        now = datetime.now()
        
        expired = [
            token for token, session in sessions.items()
            if datetime.fromisoformat(session['expires_at']) < now
        ]
        
        for token in expired:
            del sessions[token]
        
        if expired:
            self._save_sessions(sessions)
            self.logger.info(f"Cleaned up {len(expired)} expired sessions")
