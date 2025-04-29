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


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description="Process a text file.")
    parser.add_argument("file_path", help="Path to the text file to process")
    return parser.parse_args()


def get_barnyard_animals():
    """
    Return a dictionary of barnyard animals and their plural forms.
    
    Returns:
        dict: Dictionary mapping animal names to their replacement
    """
    animals = {
        'chicken': 'piglet',
        'chickens': 'piglets',
        'cow': 'piglet',
        'cows': 'piglets',
        'pig': 'piglet',
        'pigs': 'piglets',
        'sheep': 'piglet',
        'sheep': 'piglets',  # Note: singular and plural are the same
        'goat': 'piglet',
        'goats': 'piglets',
        'horse': 'piglet',
        'horses': 'piglets',
        'duck': 'piglet',
        'ducks': 'piglets',
        'turkey': 'piglet',
        'turkeys': 'piglets',
        'donkey': 'piglet',
        'donkeys': 'piglets',
        'rooster': 'piglet',
        'roosters': 'piglets'
    }
    return animals


def process_text_file(file_path, logger):
    """
    Process a text file, replacing barnyard animal names with 'piglet' or 'piglets'.
    
    Args:
        file_path (str): Path to the text file to process
        logger (logging.Logger): Logger instance
        
    Returns:
        str: Processed text with animal names replaced
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        animals = get_barnyard_animals()
        
        # Create a regex pattern for case-insensitive replacement
        pattern = re.compile(r'\b(' + '|'.join(re.escape(animal) for animal in animals.keys()) + r')\b', 
                            re.IGNORECASE)
        
        # Function to determine the replacement based on case
        def replace_animal(match):
            animal = match.group(0)
            replacement = animals[animal.lower()]
            
            # Preserve case of the original word
            if animal.isupper():
                return replacement.upper()
            elif animal[0].isupper():
                return replacement.capitalize()
            else:
                return replacement
                
        # Replace all occurrences of animal names
        processed_text = pattern.sub(replace_animal, content)
        
        return processed_text
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}", exc_info=True)
        raise


def main():
    """
    Main entry point for the application.
    
    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    try:
        logger = setup_logging()
        logger.debug("Parsing command-line arguments")
        args = parse_arguments()
        
        # Validate that the file exists
        if not os.path.isfile(args.file_path):
            logger.error(f"File not found: {args.file_path}")
            return 1
            
        logger.info(f"Processing file: {args.file_path}")

        logger.debug("Processing started")
        
        # Process the file and print the result to stdout
        processed_text = process_text_file(args.file_path, logger)
        print(processed_text)
        
        logger.debug("Processing completed")
        # Main application logic would go here
        
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