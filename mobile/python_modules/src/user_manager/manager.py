"""
User and Family Profile Management
File-based storage system
"""
import json
import jsonlines
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from src.utils import logger, config


def chart_encoder(obj):
    """Custom JSON encoder for chart objects"""
    # Handle dataclass objects (like PlanetPosition, BirthDetails)
    if hasattr(obj, '__dataclass_fields__'):
        return asdict(obj)
    # Handle datetime objects
    if isinstance(obj, datetime):
        return obj.isoformat()
    # Default to string for other types
    return str(obj)


@dataclass
class UserProfile:
    """User profile data"""
    user_id: str
    name: str
    birth_date: str  # ISO format
    birth_time: str  # HH:MM format
    birth_place: str
    latitude: float
    longitude: float
    timezone: str
    owner_email: str = ""  # Email of the user who created this profile
    relationship: str = "Self"  # Self, Spouse, Child, Parent, etc.
    gender: str = ""
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""


class UserManager:
    """Manage user profiles and history using file-based storage"""
    
    def __init__(self):
        self.logger = logger
        
        # Setup directories
        base_path = Path(config.get('storage.base_path', './data/user_data'))
        self.profiles_dir = base_path / config.get('storage.profiles_dir', 'profiles')
        self.charts_dir = base_path / config.get('storage.charts_dir', 'charts')
        self.history_dir = base_path / config.get('storage.history_dir', 'history')
        
        # Create directories
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.charts_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"User data directory: {base_path}")
    
    def create_profile(self, profile_data: Dict, owner_email: str = "") -> UserProfile:
        """
        Create a new user profile
        
        Args:
            profile_data: Dict with profile information
            owner_email: Email of the user creating this profile
        
        Returns:
            UserProfile object
        """
        # Generate user_id if not provided
        if 'user_id' not in profile_data:
            profile_data['user_id'] = self._generate_user_id(profile_data['name'])
        
        # Add owner email
        profile_data['owner_email'] = owner_email
        
        # Add timestamps
        now = datetime.now().isoformat()
        profile_data['created_at'] = now
        profile_data['updated_at'] = now
        
        profile = UserProfile(**profile_data)
        
        # Save to file
        self._save_profile(profile)
        
        # Create charts directory for this user
        user_charts_dir = self.charts_dir / profile.user_id
        user_charts_dir.mkdir(exist_ok=True)
        
        self.logger.info(f"Created profile: {profile.name} ({profile.user_id})")
        
        return profile
    
    def _generate_user_id(self, name: str) -> str:
        """Generate unique user ID from name"""
        base_id = name.lower().replace(' ', '_')
        
        # Check if exists, append number if needed
        counter = 1
        user_id = base_id
        
        while (self.profiles_dir / f"{user_id}.json").exists():
            user_id = f"{base_id}_{counter}"
            counter += 1
        
        return user_id
    
    def _save_profile(self, profile: UserProfile) -> None:
        """Save profile to JSON file"""
        profile_file = self.profiles_dir / f"{profile.user_id}.json"
        
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(profile), f, indent=2, ensure_ascii=False)
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Load user profile by ID"""
        profile_file = self.profiles_dir / f"{user_id}.json"
        
        if not profile_file.exists():
            self.logger.warning(f"Profile not found: {user_id}")
            return None
        
        with open(profile_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return UserProfile(**data)
    
    def update_profile(self, user_id: str, updates: Dict) -> Optional[UserProfile]:
        """Update user profile"""
        profile = self.get_profile(user_id)
        
        if not profile:
            return None
        
        # Update fields
        for key, value in updates.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        # Update timestamp
        profile.updated_at = datetime.now().isoformat()
        
        # Save
        self._save_profile(profile)
        
        self.logger.info(f"Updated profile: {user_id}")
        
        return profile
    
    def delete_profile(self, user_id: str, owner_email: str = "") -> bool:
        """Delete user profile with ownership verification"""
        profile_file = self.profiles_dir / f"{user_id}.json"
        
        if profile_file.exists():
            try:
                # Verify ownership before deleting
                with open(profile_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    profile_owner = data.get('owner_email', "")
                
                # Only delete if owner matches or both are empty (guest mode)
                if owner_email == profile_owner:
                    # Ensure file is closed before deletion
                    import time
                    time.sleep(0.1)  # Small delay to ensure file handle is released
                    profile_file.unlink()
                    self.logger.info(f"Deleted profile: {user_id}")
                    return True
                else:
                    self.logger.warning(f"Unauthorized delete attempt for profile: {user_id}")
                    return False
            except Exception as e:
                self.logger.error(f"Error deleting profile {user_id}: {e}")
                return False
        
        return False
    
    def list_profiles(self, owner_email: str = "") -> List[UserProfile]:
        """List user profiles, optionally filtered by owner email"""
        profiles = []
        
        for profile_file in self.profiles_dir.glob("*.json"):
            with open(profile_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Add owner_email if missing (for backward compatibility)
                if 'owner_email' not in data:
                    data['owner_email'] = ""
                profile = UserProfile(**data)
                
                # Filter by owner_email if provided
                if owner_email == "" or profile.owner_email == owner_email:
                    profiles.append(profile)
        
        # Sort by relationship (Self first, then others)
        profiles.sort(key=lambda p: (p.relationship != "Self", p.name))
        
        return profiles
    
    def save_chart(self, user_id: str, chart_data: Dict, 
                   chart_type: str = "birth_chart") -> str:
        """
        Save calculated chart data
        
        Args:
            user_id: User ID
            chart_data: Chart calculation results
            chart_type: Type of chart (birth_chart, transit, etc.)
        
        Returns:
            Path to saved chart file
        """
        user_charts_dir = self.charts_dir / user_id
        user_charts_dir.mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_file = user_charts_dir / f"{chart_type}_{timestamp}.json"
        
        # Add metadata
        chart_data['saved_at'] = datetime.now().isoformat()
        chart_data['chart_type'] = chart_type
        
        with open(chart_file, 'w', encoding='utf-8') as f:
            json.dump(chart_data, f, indent=2, default=chart_encoder)
        
        self.logger.info(f"Saved chart: {chart_file}")
        
        return str(chart_file)
    
    def get_latest_chart(self, user_id: str, 
                        chart_type: str = "birth_chart") -> Optional[Dict]:
        """Get the most recent chart for a user"""
        user_charts_dir = self.charts_dir / user_id
        
        if not user_charts_dir.exists():
            return None
        
        # Find matching charts
        chart_files = sorted(
            user_charts_dir.glob(f"{chart_type}_*.json"),
            reverse=True
        )
        
        if not chart_files:
            return None
        
        # Load most recent
        with open(chart_files[0], 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def log_query(self, user_id: str, query: str, answer: str, 
                  sources: List[Dict] = None) -> None:
        """Log user query to history"""
        log_file = self.history_dir / f"queries_{datetime.now().strftime('%Y%m')}.jsonl"
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'query': query,
            'answer': answer,
            'num_sources': len(sources) if sources else 0
        }
        
        with jsonlines.open(log_file, mode='a') as writer:
            writer.write(log_entry)
    
    def log_remedy(self, user_id: str, remedy: Dict) -> None:
        """Log suggested remedy"""
        log_file = self.history_dir / f"remedies_{datetime.now().strftime('%Y%m')}.jsonl"
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'remedy': remedy
        }
        
        with jsonlines.open(log_file, mode='a') as writer:
            writer.write(log_entry)
    
    def get_query_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recent query history for user"""
        queries = []
        
        # Read from all monthly log files
        for log_file in sorted(self.history_dir.glob("queries_*.jsonl"), reverse=True):
            with jsonlines.open(log_file) as reader:
                for entry in reader:
                    if entry['user_id'] == user_id:
                        queries.append(entry)
                        
                        if len(queries) >= limit:
                            return queries
        
        return queries
