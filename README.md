# Website Status Checker

This Python script checks the status of websites listed in a JSON file, records the results, and updates the JSON file with the status of each website.
## Prerequisites

    Python 3.x
    Required Python packages: requests

## Usage

    Clone this repository or download the Python script to your local machine.

    Ensure you have Python 3.x installed on your system.

    Install the required Python packages using pip:

pip install requests

Prepare a JSON file containing a list of websites you want to check. The JSON file should have the following structure. An example is provided file is provided:

json
```
{
    "https://example.com": {
        "Reached": null,
        "Last Check Time": null,
        "Last Fail Time": null,
        "Status Code": null,
        "Status Message": null
    },
    "https://example2.com": {
        "Reached": null,
        "Last Check Time": null,
        "Last Fail Time": null,
        "Status Code": null,
        "Status Message": null
    },
    // Add more websites as needed
}
```
    Replace __"https://example.com"__ and __"https://example2.com"__ with the URLs of the websites you want to check.
    Leave the other fields (__"Reached"__, __"Last Check Time"__, __"Last Fail Time"__, __"Status Code"__, __"Status Message"__) as null or provide an empty dict, they will be created automatically.

Run the script using the following command:

python website_status_checker.py your_json_file.json

Replace your __json_file.json__ with the path to your JSON file containing the list of websites.

Optionally, use the __-v__ or __--verbose__ flag to enable verbose output. This will display additional information about the status of each URL.

    python website_status_checker.py -v your_json_file.json

## Output

The script will perform the following actions:

    Send HTTP GET requests to each website listed in the JSON file.
    Record the status code and status message for each website.
    Update the __"Reached"__, __"Last Check Time"__, __"Last Fail Time"__, __"Status Code"__, and __"Status Message"__ fields in the JSON file with the results of the checks.
    "Status Code" is not update if the site is completely unreachable.

If a website's status code falls within the range of 4xx or 5xx, it is considered unsuccessful, and the __"Reached"__ field is set to __False__. If the website's status code is not in that range, it is considered successful, and the "Reached" field is set to True. The script also records the time of the last check and, if applicable, the time of the last failure.
## Example

Here's an example of a JSON file before and after running the script:

### Before:

json
```
{
    "https://example.com": {
        "Reached": null,
        "Last Check Time": null,
        "Last Fail Time": null,
        "Status Code": null,
        "Status Message": null
    },
    "https://example2.com": {
        "Reached": null,
        "Last Check Time": null,
        "Last Fail Time": null,
        "Status Code": null,
        "Status Message": null
    }
}
```
### After:

json
```
{
    "https://example.com": {
        "Reached": true,
        "Last Check Time": "2023-10-10 14:30:00",
        "Last Fail Time": null,
        "Status Code": 200,
        "Status Message": "Success"
    },
    "https://example2.com": {
        "Reached": false,
        "Last Check Time": "2023-10-10 14:35:00",
        "Last Fail Time": "2023-10-10 14:35:00",
        "Status Code": 404,
        "Status Message": "Not Found"
    }
}
```