"""
Configuration loader utility
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration manager"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self.load_config()
    
    def load_config(self, config_path: str = None):
        """Load configuration from YAML file"""
        if config_path is None:
            # Default config path
            base_dir = Path(__file__).parent.parent.parent
            config_path = base_dir / "config" / "config.yaml"
        
        with open(config_path, 'r') as f:
            self._config = yaml.safe_load(f)
        
        # Override with environment variables if present
        self._apply_env_overrides()
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides"""
        # Override data directories
        if os.getenv('DATA_DIR'):
            self._config['storage']['base_path'] = os.getenv('DATA_DIR')
        
        if os.getenv('VECTOR_DB_DIR'):
            self._config['vector_db']['persist_directory'] = os.getenv('VECTOR_DB_DIR')
        
        # Override Ollama settings
        if os.getenv('OLLAMA_MODEL'):
            self._config['llm']['model'] = os.getenv('OLLAMA_MODEL')
        
        if os.getenv('OLLAMA_HOST'):
            self._config['llm']['host'] = os.getenv('OLLAMA_HOST')
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        Example: config.get('llm.model')
        """
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def get_all(self) -> Dict:
        """Get entire configuration"""
        return self._config.copy()
    
    @property
    def llm_config(self) -> Dict:
        """Get LLM configuration"""
        return self._config.get('llm', {})
    
    @property
    def astrology_config(self) -> Dict:
        """Get astrology configuration"""
        return self._config.get('astrology', {})
    
    @property
    def storage_config(self) -> Dict:
        """Get storage configuration"""
        return self._config.get('storage', {})
    
    @property
    def rag_config(self) -> Dict:
        """Get RAG configuration"""
        return self._config.get('rag', {})


# Singleton instance
config = Config()
