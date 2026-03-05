"""
Firebase Configuration Module
MANDATORY: All state must be managed through Firebase per Ecosystem directive.
This ensures persistence across crashes and distributed execution.
"""
import os
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from firebase_admin.exceptions import FirebaseError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FirebaseStateManager:
    """Centralized state management using Firestore."""
    
    def __init__(self, credential_path: str = None):
        """
        Initialize Firebase connection.
        
        Args:
            credential_path: Path to Firebase service account JSON.
                           Defaults to FIREBASE_CREDENTIALS_PATH env var.
        
        Raises:
            FileNotFoundError: If credentials file doesn't exist
            FirebaseError: If Firebase initialization fails
        """
        self.db = None
        self.initialized = False
        
        # Validate credential path
        if credential_path is None:
            credential_path = os.getenv('FIREBASE_