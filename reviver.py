# Function to read credentials from a CSV or TXT file
import csv
def read_credentials_from_file(filepath: str) -> list:
    """
    Reads a file containing username and password pairs.
    Supports CSV (comma or tab separated) and TXT (comma, tab, or whitespace separated).
    Returns a list of (username, password) tuples.
    """
    credentials = []
    with open(filepath, 'r', encoding='utf-8') as f:
        # Try CSV reader first (comma or tab separated)
        try:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    credentials.append((row[0].strip(), row[1].strip()))
        except Exception:
            # Fallback: whitespace separated
            f.seek(0)
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    credentials.append((parts[0], parts[1]))
    return credentials
import re
from playwright.sync_api import Page, expect


def test_example(page: Page,username,password) -> None:
    page.goto("https://www.pythonanywhere.com/")
    page.wait_for_selector('[role="link"][name="Log in"]', timeout=10000)
    page.get_by_role("link", name="Log in").click()
    page.wait_for_selector('[role="textbox"][name="Username or email address"]', timeout=10000)
    page.get_by_role("textbox", name="Username or email address").click()
    page.get_by_role("textbox", name="Username or email address").fill(username)
    page.wait_for_selector('[role="textbox"][name="Password"]', timeout=10000)
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill(password)
    page.wait_for_selector('[role="button"][name="Log in"]', timeout=10000)
    page.get_by_role("button", name="Log in").click()
    page.wait_for_selector('[role="link"][name="Web"]', timeout=10000)
    page.get_by_role("link", name="Web", exact=True).click()
    page.wait_for_selector('[role="button"][name="Run until 3 months from today"]', timeout=10000)
    page.get_by_role("button", name="Run until 3 months from today").click()
    page.wait_for_selector('[role="button"][name="Log out"]', timeout=10000)
    page.get_by_role("button", name="Log out").click()


# Function to loop through a list of username/password pairs and submit them
def submit_multiple_logins(page: Page, credentials: list, index: int = None):
    """
    credentials: list of (username, password) tuples
    index: optional integer, if specified only that credential is used
    """
    if index is not None:
        # Use only the credential at the specified index
        username, password = credentials[index]
        test_example(page, username, password)
        print(f"Login successful for: {username}")
    else:
        # Use all credentials
        for username, password in credentials:
            test_example(page, username, password)
            print(f"Login successful for: {username}")


if __name__ == "__main__":
    import os
    import sys
    from playwright.sync_api import sync_playwright

    credentials = read_credentials_from_file("credentials.csv")

    # Optional: allow index to be specified via command line or environment variable
    index = None
    if len(sys.argv) > 1:
        try:
            index = int(sys.argv[1])
        except Exception:
            index = None
    elif os.environ.get("CREDENTIAL_INDEX"):
        try:
            index = int(os.environ["CREDENTIAL_INDEX"])
        except Exception:
            index = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        submit_multiple_logins(page, credentials, index=index)
        browser.close()
