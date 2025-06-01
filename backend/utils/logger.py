
import logging
import sys
from pathlib import Path

def setup_logger():
    """Setup main application logger"""
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "moengage_analyzer.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger("MoEngageAnalyzer")
    logger.info("Logger initialized successfully")
    
    return logger

def get_logger(name):
    """Get logger for specific module"""
    
    return logging.getLogger(name)
