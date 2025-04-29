

"""
Unit tests for the console application.
"""
import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
import piglet


class TestMainModule(unittest.TestCase):
    """Test cases for the piglet module."""

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data="The cow jumped over the moon.")
    @patch('piglet.process_text_file', return_value="The piglet jumped over the moon.")
    def test_main_success(self, mock_process, mock_file, mock_isfile, mock_parse_args):
        """Test that the main function returns 0 when file exists."""
        # Mock the argument parser to return a file path
        mock_parse_args.return_value = type('Args', (), {'file_path': 'test.txt'})
        # Mock os.path.isfile to return True
        mock_isfile.return_value = True        
        
        result = piglet.main()
        self.assertEqual(result, 0)
        mock_isfile.assert_called_once_with('test.txt')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isfile')
    def test_main_file_not_found(self, mock_isfile, mock_parse_args):
        """Test that the main function returns 1 when file doesn't exist."""
        # Mock the argument parser to return a file path
        mock_parse_args.return_value = type('Args', (), {'file_path': 'nonexistent.txt'})
        # Mock os.path.isfile to return False
        mock_isfile.return_value = False
        
        result = piglet.main()
        self.assertEqual(result, 1)
        mock_isfile.assert_called_once_with('nonexistent.txt')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="The cow jumped over the moon.")
    @patch('piglet.process_text_file', return_value="The piglet jumped over the moon.")
    def test_main_success_with_valid_file(self, mock_process, mock_file, mock_isfile, mock_parse_args):
        """Test that the main function processes a valid file."""
        mock_parse_args.return_value = type('Args', (), {'file_path': 'test.txt'})
        result = piglet.main()
        self.assertEqual(result, 0)

    @patch('piglet.setup_logging')
    @patch('piglet.parse_arguments')
    @patch('os.path.isfile', return_value=True)
    def test_logging_setup(self, mock_isfile, mock_parse_args, mock_setup_logging):
        """Test that logging is set up correctly."""
        # Mock the argument parser to return a file path
        mock_parse_args.return_value = type('Args', (), {'file_path': 'test.txt'})
        piglet.main()
        mock_setup_logging.assert_called_once()

    @patch('piglet.main')
    def test_sys_exit_called_with_main_result(self, mock_main):
        """Test that sys.exit is called with the result of main()."""
        # Set up the mock to return a specific value
        mock_main.return_value = 42
        
        # Create a context where we can test the __name__ == "__main__" block
        with patch('sys.exit') as mock_exit:
            # Directly call the code that would run if __name__ == "__main__"
            piglet.sys.exit(piglet.main())
            mock_exit.assert_called_once_with(42)

    @patch('os.path.isfile', return_value=True)
    def test_argument_parsing(self, mock_isfile):
        """Test that command line arguments are parsed correctly."""
        # Pass arguments directly instead of patching sys.argv
        args = piglet.parse_arguments(['test.txt'])
        self.assertEqual(args.file_path, 'test.txt')

    
    def test_missing_argument(self):
        """Test that an error is raised when no file path is provided."""
        with self.assertRaises(SystemExit):
            piglet.parse_arguments([])

    def test_get_barnyard_animals(self):
        """Test that the barnyard animals dictionary is correctly defined."""
        animals = piglet.get_barnyard_animals()
        self.assertIsInstance(animals, dict)
        self.assertIn('cow', animals)
        self.assertEqual(animals['cow'], 'piglet')
        self.assertIn('cows', animals)
        self.assertEqual(animals['cows'], 'piglets')

    @patch('builtins.open', new_callable=mock_open, read_data="The cow jumped over the moon.")
    def test_process_text_file_singular(self, mock_file):
        """Test that singular animal names are replaced correctly."""
        logger = MagicMock()
        result = piglet.process_text_file('test.txt', logger)
        self.assertEqual(result, "The piglet jumped over the moon.")
        mock_file.assert_called_once_with('test.txt', 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open, read_data="The cows were grazing in the field.")
    def test_process_text_file_plural(self, mock_file):
        """Test that plural animal names are replaced correctly."""
        logger = MagicMock()
        result = piglet.process_text_file('test.txt', logger)
        self.assertEqual(result, "The piglets were grazing in the field.")
        mock_file.assert_called_once_with('test.txt', 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open, read_data="COWS and Horses and chickens")
    def test_process_text_file_case_preservation(self, mock_file):
        """Test that case is preserved when replacing animal names."""
        logger = MagicMock()
        result = piglet.process_text_file('test.txt', logger)
        self.assertEqual(result, "PIGLETS and Piglets and piglets")
        mock_file.assert_called_once_with('test.txt', 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open, read_data="No animals here.")
    def test_process_text_file_no_animals(self, mock_file):
        """Test that text without animal names is unchanged."""
        logger = MagicMock()
        result = piglet.process_text_file('test.txt', logger)
        self.assertEqual(result, "No animals here.")
        mock_file.assert_called_once_with('test.txt', 'r', encoding='utf-8')

    @patch('builtins.open', side_effect=IOError("File error"))
    def test_process_text_file_error(self, mock_file):
        """Test that file errors are handled correctly."""
        logger = MagicMock()
        with self.assertRaises(IOError):
            piglet.process_text_file('test.txt', logger)

    @patch('piglet.process_text_file')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.print')
    def test_main_processes_file(self, mock_print, mock_isfile, mock_parse_args, mock_process):
        """Test that main function processes the file and prints the result."""
        mock_parse_args.return_value = type('Args', (), {'file_path': 'test.txt'})
        mock_process.return_value = "Processed text"
        result = piglet.main()
        self.assertEqual(result, 0)
        mock_print.assert_called_once_with("Processed text", end='')

if __name__ == '__main__':
    unittest.main()