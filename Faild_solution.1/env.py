#!/usr/bin/env python3
"""
Parse .env file and convert to dictionary.
"""

import os
from pathlib import Path


def parse_env_file(env_file: str | Path) -> dict[str, str]:
    """
    Parse a .env file and return variables as a dictionary.
    
    Args:
        env_file: Path to the .env file
        
    Returns:
        Dictionary of environment variables with values as strings
        
    Example .env file:
        KEY1=value1
        KEY2=value2
        KEY_WITH_SPACES=value with spaces
        KEY_WITH_EQUALS=value=with=equals
        KEY_WITH_QUOTES="quoted value"
        EMPTY=
        # comment line
    """
    env_vars = {}
    
    try:
        with open(env_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                # Strip newline and comments
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Skip lines that are only whitespace
                if line == '':
                    continue
                
                # Parse the line
                if '=' in line:
                    key, _, value = line.partition('=')
                    
                    # Strip whitespace and quotes from key
                    key = key.strip().strip('"\'')
                    
                    # If key is empty after stripping, skip
                    if not key:
                        continue
                    
                    # Strip quotes from value and handle edge cases
                    value = value.strip()
                    
                    # Handle quoted values (remove surrounding quotes)
                    if value and ((value.startswith('"') and value.endswith('"')) or
                                 (value.startswith("'") and value.endswith("'"))):
                        value = value[1:-1]
                    elif value.startswith('"'):
                        # Only start with quote, end with quote - keep the value
                        pass
                    
                    # Handle escaped quotes within quotes
                    value = value.replace('\\"', '"')
                    
                    # Handle backslash-escaped characters
                    value = value.replace('\\n', '\n').replace('\\t', '\t')
                    
                    # Handle equals signs in values (split only on first =)
                    if '=' not in value and '"' not in value:
                        # Value has no quotes, but might have equals
                        pass
                    
                    env_vars[key] = value
                elif not line.startswith('#') and not line.startswith('\\'):
                    # Line without = but not a comment - could be Windows line ending artifact
                    pass
                    
    except FileNotFoundError:
        print(f"Error: File '{env_file}' not found.")
        return env_vars
    except PermissionError:
        print(f"Error: Permission denied reading '{env_file}'.")
        return env_vars
    except Exception as e:
        print(f"Error parsing '{env_file}': {e}")
        return env_vars
    
    return env_vars


def parse_env_lines(lines: list[str] | None = None) -> dict[str, str]:
    """
    Parse a list of lines and return variables as a dictionary.
    
    Args:
        lines: List of strings (lines from a .env file)
        
    Returns:
        Dictionary of environment variables
    """
    if lines is None:
        lines = []
        
    env_vars = {}
    
    for line in lines:
        # Strip newline and comments
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Skip lines that are only whitespace
        if line == '':
            continue
        
        # Parse the line
        if '=' in line:
            key, _, value = line.partition('=')
            
            # Strip whitespace and quotes from key
            key = key.strip().strip('"\'')
            
            # If key is empty after stripping, skip
            if not key:
                continue
            
            # Strip quotes from value and handle edge cases
            value = value.strip()
            
            # Handle quoted values (remove surrounding quotes)
            if value and ((value.startswith('"') and value.endswith('"')) or
                          (value.startswith("'") and value.endswith("'"))):
                value = value[1:-1]
            elif value.startswith('"'):
                # Only start with quote, end with quote - keep the value
                pass
            
            # Handle escaped quotes within quotes
            value = value.replace('\\"', '"')
            
            # Handle backslash-escaped characters
            value = value.replace('\\n', '\n').replace('\\t', '\t')
            
            env_vars[key] = value
    
    return env_vars


# Example usage and test
if __name__ == '__main__':
    # Test with current working directory .env if it exists
    env_file = Path(__file__).parent / '.env'
    
    if env_file.exists():
        env_vars = parse_env_file(env_file)
        print("Parsed environment variables:")
        for key, value in env_vars.items():
            print(f"  {key}={value}")
    else:
        print("No .env file found in current directory.")
