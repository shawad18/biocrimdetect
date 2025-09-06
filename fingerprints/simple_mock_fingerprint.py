import os
import random
import time
from datetime import datetime

def match_fingerprint(fingerprint_path):
    """
    Simple mock fingerprint matching that works without external dependencies
    Returns a tuple of (match_result, matched_name)
    """
    
    # Mock criminal names for fingerprint matching
    criminal_names = [
        'John Doe',
        'Jane Smith', 
        'Robert Johnson',
        'Maria Garcia',
        'David Wilson',
        'Sarah Brown',
        'Michael Davis',
        'Lisa Anderson'
    ]
    
    # Simulate processing time
    time.sleep(random.uniform(1.0, 3.0))
    
    # Simulate fingerprint matching with realistic probabilities
    match_probability = random.random()
    
    if match_probability < 0.3:  # 30% chance of finding a match
        matched_name = random.choice(criminal_names)
        confidence = random.uniform(0.75, 0.95)
        
        result = {
            'match_found': True,
            'confidence': confidence,
            'matched_name': matched_name,
            'match_score': confidence * 100,
            'processing_time': random.uniform(1.5, 2.8),
            'timestamp': datetime.now().isoformat(),
            'fingerprint_quality': random.choice(['Good', 'Excellent', 'Fair']),
            'match_type': 'Criminal Database',
            'database_size': len(criminal_names)
        }
        
        return f"MATCH FOUND: {matched_name} (Confidence: {confidence:.1%})", matched_name
        
    else:  # 70% chance of no match
        result = {
            'match_found': False,
            'confidence': 0.0,
            'matched_name': None,
            'match_score': 0,
            'processing_time': random.uniform(1.0, 2.5),
            'timestamp': datetime.now().isoformat(),
            'fingerprint_quality': random.choice(['Good', 'Fair', 'Poor']),
            'match_type': 'Criminal Database',
            'database_size': len(criminal_names),
            'searched_records': len(criminal_names)
        }
        
        return "NO MATCH FOUND: Fingerprint not found in criminal database", None

def analyze_fingerprint_quality(fingerprint_path):
    """
    Analyze fingerprint image quality
    Returns quality assessment
    """
    
    # Simulate quality analysis
    time.sleep(random.uniform(0.5, 1.5))
    
    quality_scores = {
        'overall_quality': random.uniform(0.6, 0.95),
        'clarity': random.uniform(0.7, 0.9),
        'ridge_definition': random.uniform(0.65, 0.85),
        'minutiae_count': random.randint(25, 45),
        'image_resolution': random.choice(['300 DPI', '500 DPI', '1000 DPI']),
        'usable_area': random.uniform(0.75, 0.95)
    }
    
    overall = quality_scores['overall_quality']
    
    if overall >= 0.8:
        quality_rating = 'Excellent'
    elif overall >= 0.7:
        quality_rating = 'Good'
    elif overall >= 0.6:
        quality_rating = 'Fair'
    else:
        quality_rating = 'Poor'
    
    return {
        'quality_rating': quality_rating,
        'quality_score': overall,
        'details': quality_scores,
        'suitable_for_matching': overall >= 0.6
    }

def get_fingerprint_statistics():
    """
    Get mock statistics about the fingerprint database
    """
    
    return {
        'total_records': 8,
        'last_updated': datetime.now().isoformat(),
        'database_version': '1.0',
        'matching_algorithm': 'Mock Minutiae Matching',
        'average_match_time': '2.1 seconds',
        'success_rate': '30%'
    }

def validate_fingerprint_image(fingerprint_path):
    """
    Validate if the uploaded file is a valid fingerprint image
    """
    
    if not os.path.exists(fingerprint_path):
        return False, "File does not exist"
    
    # Check file size (should be reasonable for an image)
    file_size = os.path.getsize(fingerprint_path)
    if file_size < 1024:  # Less than 1KB
        return False, "File too small to be a valid image"
    
    if file_size > 10 * 1024 * 1024:  # More than 10MB
        return False, "File too large"
    
    # Check file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    file_ext = os.path.splitext(fingerprint_path)[1].lower()
    
    if file_ext not in valid_extensions:
        return False, f"Invalid file type. Supported: {', '.join(valid_extensions)}"
    
    return True, "Valid fingerprint image"