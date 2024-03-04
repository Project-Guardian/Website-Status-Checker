import json
import requests
import time
from datetime import datetime
from urllib.parse import urlparse
import argparse
import os

# Function to check the URL and return the status code and message
def check_url(url, verbose):
    failedString = '' # Initialize failedString variable
    for _ in range(4):  # Retry 3 times
        try:
            # Add a header
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
            }

            # Attempt to make an HTTP GET request to the provided URL (add timeout=X)
            response = requests.get(url, headers=headers)
            status_code = response.status_code
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
            if verbose:
                # If verbose mode is enabled, print a success message
                print(f"Status Message for {url}: Success \n")
            
            return status_code, "Success"
        except requests.exceptions.RequestException as e:
            if verbose:
                # If verbose mode is enabled, print an error message
                print(f"Status Message for {url}: Failure")
                print(f"{str(e)} \n")
            failedString = e      
    
            # Wait for a short duration before retrying
            time.sleep(3)
    
    # Return the status code even on failure (4XX or 5XX)
    return response.status_code if 'response' in locals() else None, failedString


# Function to update the JSON data with the results of the URL check
def update_json(json_data, original_url, status_code, status_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a new entry in the JSON data if the URL is not already present
    if original_url not in json_data:
        json_data[original_url] = {
            "Reached": None,               # Initialize 'Reached' to None
            "Last Check Time": None,       # Initialize 'Last Check Time' to None
            "Last Fail Time": None,        # Initialize 'Last Fail Time' to None
            "Status Code": None,           # Initialize 'Status Code' to None
            "Status Message": None         # Initialize 'Status Message' to None
        }

    entry = json_data[original_url]  # Retrieve the entry for the original URL

    if status_code is not None:
        # If the URL check was successful:
        entry["Last Check Time"] = timestamp  # Update the "Last Check Time" to the current timestamp
        entry["Status Code"] = status_code   # Update the "Status Code" with the received status code
        entry["Status Message"] = status_message  # Update the "Status Message" with the success message

        # Check if the status code indicates an error (4XX or 5XX)
        if 400 <= status_code < 600:
            if entry["Reached"]:
                # If the previous status was "Reached" (i.e., it was successful before):
                entry["Last Fail Time"] = timestamp  # Update the "Last Fail Time" to the current timestamp
                print(f"Status Message for {original_url}: Failure")
                print(f"{status_message}")
                print("Current failed time " + timestamp + "\n")
            entry["Reached"] = False
        else:
            # Adds an output if it failed previously but is not able to reconnect
            if entry["Reached"] == False:
                print(f"Connection successful again for {original_url}")
                print("Current success time " + timestamp + "\n")
            entry["Reached"] = True
    else:
        # If the URL check failed:
        if entry["Reached"]:
            # If the previous status was "Reached" (i.e., it was successful before):
            entry["Last Fail Time"] = timestamp  # Update the "Last Fail Time" to the current timestamp
            print(f"Status Message for {original_url}: Failure")
            print(f"{status_message}")
            print("Current failed time " + timestamp + "\n")

        entry["Reached"] = False            # URL check failed
        entry["Last Check Time"] = timestamp  # Update the "Last Check Time" to the current timestamp
        entry["Status Message"] = status_message  # Update the "Status Message" with the failure message

# Main function to perform the URL checks and update the JSON data
def main(json_file, verbose):
    # If json_file is not provided, use "list.json" as the default
    if json_file is None:
        json_file = "list.json"

    # Check if the JSON file exists in the current directory
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found in the current directory.")
        return
    
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Create a copy of the keys to iterate over
    urls = list(data.keys())

    for original_url in urls:
        # Check if the URL has a scheme (http:// or https://)
        parsed_url = urlparse(original_url)
        if not parsed_url.scheme:
            temp_url = "https://" + original_url  # Add "https://" if scheme is missing
        else:
            temp_url = original_url  # Use the original URL for the request

        if verbose:
            # If verbose mode is enabled, print the URL being checked
            print(f"Checking URL: {temp_url}")
        
        status_code, status_message = check_url(temp_url, verbose)
        update_json(data, original_url, status_code, status_message)

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "-V", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("json_file", nargs='?', help="Path to the JSON file (optional)")
    args = parser.parse_args()
    
    # Call the main function with parsed arguments
    main(args.json_file, args.verbose)
