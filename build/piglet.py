#!/usr/bin/env python3
"""
Entry point for the console application.
"""
import sys
import os
import argparse
import re
import logging


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger(__name__)


def parse_arguments(args=None):
    """
    Parse command line arguments.
    
    Args:
        args: List of command line arguments to parse. If None, sys.argv is used.
        
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description="Process a text file.")
    parser.add_argument("file_path", help="Path to the text file to process")
    return parser.parse_args(args)


def get_barnyard_animals():
    """
    Returns a dictionary of barnyard animals with their singular and plural forms.
    
    Returns:
        dict: Dictionary with animal names as keys and their replacement as values
    """
    animals = {
        'pig': 'piglet',
        'pigs': 'piglets',
        'cow': 'piglet',
        'cows': 'piglets',
        'chicken': 'piglet',
        'chickens': 'piglets',
        'rooster': 'piglet',
        'roosters': 'piglets',
        'horse': 'piglet',
        'horses': 'piglets',
        'sheep': 'piglet',
        'sheep': 'piglets',  # Note: singular and plural are the same
        'goat': 'piglet',
        'goats': 'piglets',
        'duck': 'piglet',
        'ducks': 'piglets',
        'turkey': 'piglet',
        'turkeys': 'piglets',
        'donkey': 'piglet',
        'donkeys': 'piglets'
    }
    return animals


def process_text_file(file_path, logger):
    """
    Process the text file, replacing barnyard animals with 'piglet' or 'piglets'.
    
    Args:
        file_path (str): Path to the text file to process
        logger (logging.Logger): Logger instance
        
    Returns:
        str: Processed text with animal names replaced
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    animals = get_barnyard_animals()
    
    # Create a regex pattern for case-insensitive word boundary matches
    pattern = r'\b(' + '|'.join(re.escape(animal) for animal in animals.keys()) + r')\b'
    
    def replace_animal(match):
        animal = match.group(0).lower()
        replacement = animals.get(animal)
        
        # Preserve the original case pattern (all caps, title case, etc.)
        if match.group(0).isupper():
            return replacement.upper()
        elif match.group(0)[0].isupper():
            return replacement.title()
        return replacement
    
    # Replace all occurrences of animals with piglet/piglets
    processed_text = re.sub(pattern, replace_animal, content, flags=re.IGNORECASE)
    return processed_text


def main():
    """
    Main entry point for the application.
    
    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    try:
        logger = setup_logging()
        logger.debug("Parsing command line arguments")
        args = parse_arguments()
        
        # Validate that the file exists
        if not os.path.isfile(args.file_path):
            logger.error(f"File not found: {args.file_path}")
            return 1
            
        logger.info(f"Processing file: {args.file_path}")
        
        try:
            processed_text = process_text_file(args.file_path, logger)
            # Output the processed text to stdout
            print(processed_text, end='')
            logger.debug("File processed successfully")
        except Exception as e:
            logger.error(f"Error processing file: {e}", exc_info=True)
            return 1
        
        logger.debug("Application completed successfully")
        return 0
    except Exception as e:
        # If logger is not defined (e.g., setup_logging failed), use root logger
        try:
            logger.error(f"An error occurred: {e}", exc_info=True)
        except UnboundLocalError:
            # Fallback to root logger if logger is not defined
            logging.error(f"An error occurred during application startup: {e}", exc_info=True)
        
        return 1


if __name__ == "__main__":
    sys.exit(main())