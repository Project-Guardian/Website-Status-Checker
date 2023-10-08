# Website Status Checker

This Python script checks the status of websites listed in a JSON file, records the results, and updates the JSON file with the status of each website.

## Prerequisites

- Python 3.x
- Required Python packages: `requests`

## Usage

1. Clone this repository or download the Python script to your local machine.
2. Ensure you have Python 3.x installed on your system.
3. Install the required Python packages using pip:



```pip install requests```


4. Prepare a JSON file containing a list of websites you want to check. The JSON file should have the following structure:

```json
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
    Replace "https://example.com" and "https://example2.com" with the URLs of the websites you want to check.
    Leave the other fields ("Reached", "Last Check Time", "Last Fail Time", "Status Code", "Status Message") as null or provide an empty dict; they will be created automatically.

Run the script using the following command:

```python website_status_checker.py your_json_file.json```

Replace your __json_file.json__ with the path to your JSON file containing the list of websites.

Optionally, use the __-v__ or __--verbose__ flag to enable verbose output. This will display additional information about the status of each URL.

```python website_status_checker.py -v your_json_file.json```

## Output

The script will perform the following actions:

    Send HTTP GET requests to each website listed in the JSON file.
    Record the status code and status message for each website.
    Update the "Reached", "Last Check Time", "Last Fail Time", "Status Code", and "Status Message" fields in the JSON file with the results of the checks.
    "Status Code" is not updated if the site is completely unreachable.

If a website's status code falls within the range of 4xx or 5xx, it is considered unsuccessful, and the __"Reached"__ field is set to __False__. If the website's status code is not in that range, it is considered successful, and the __"Reached"__ field is set to __True__. The script also records the time of the last check and, if applicable, the time of the last failure.
## Example

Here's an example of a JSON file before and after running the script:

### Before:


```json
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

```json
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