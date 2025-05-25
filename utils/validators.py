"""
Validation utilities for stock codes and input data
"""

import re
from typing import List, Tuple
from datetime import date

from config import VALID_CODE_PATTERN


class CodeValidator:
    """Handles validation of stock codes and related inputs"""
    
    @staticmethod
    def validate_stock_code(code: str) -> bool:
        """
        Validate stock code format
        
        Args:
            code: Stock code to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not code:
            return False
            
        code = code.strip()
        return bool(re.match(VALID_CODE_PATTERN, code))
    
    @staticmethod
    def validate_multiple_codes(codes_input: str) -> Tuple[List[str], List[str]]:
        """
        Validate multiple stock codes from comma-separated input
        
        Args:
            codes_input: Comma-separated string of codes
            
        Returns:
            Tuple of (valid_codes, invalid_codes)
        """
        if not codes_input:
            return [], []
            
        # Split and clean codes
        codes = [code.strip() for code in codes_input.split(',') if code.strip()]
        
        valid_codes = []
        invalid_codes = []
        
        for code in codes:
            if CodeValidator.validate_stock_code(code):
                valid_codes.append(code)
            else:
                invalid_codes.append(code)
        
        return valid_codes, invalid_codes
    
    @staticmethod
    def validate_date_range(start_date: date, end_date: date) -> Tuple[bool, str]:
        """
        Validate date range
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if start_date > end_date:
            return False, "Start date must be before end date"
        
        if end_date > date.today():
            return False, "End date cannot be in the future"
        
        # Check if date range is reasonable (not too far back)
        from datetime import timedelta
        max_history = date.today() - timedelta(days=365 * 25)  # 25 years
        if start_date < max_history:
            return False, f"Start date cannot be earlier than {max_history.strftime('%Y-%m-%d')}"
        
        return True, ""
    
    @staticmethod
    def sanitize_codes(codes: List[str]) -> List[str]:
        """
        Sanitize and deduplicate stock codes
        
        Args:
            codes: List of stock codes
            
        Returns:
            List of sanitized unique codes
        """
        sanitized = []
        seen = set()
        
        for code in codes:
            clean_code = code.strip().upper()
            if clean_code and clean_code not in seen:
                sanitized.append(clean_code)
                seen.add(clean_code)
        
        return sanitized 