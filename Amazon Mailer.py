# This script takes a screenshot of a webpage using Playwright and sends it as an email attachment
import asyncio
from playwright.async_api import async_playwright
import smtplib
from email.message import EmailMessage


# Click 'Continue shopping' button, take screenshot
async def click_and_screenshot(url, screenshot_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        try:
            # Wait for and click the 'Continue shopping' button
            await page.wait_for_selector('text=Continue shopping', timeout=10000)
            await page.click('text=Continue shopping')
        except Exception as e:
            print(f"Button not found or error: {e}")
        await page.screenshot(path=screenshot_path, full_page=True)
        await browser.close()

def send_email_with_attachment(sender, password, receiver, subject, body, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(body)
    with open(attachment_path, 'rb') as f:
        img_data = f.read()
        msg.add_attachment(img_data, maintype='image', subtype='png', filename='screenshot.png')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)


if __name__ == "__main__":
    # --- CONFIGURE THESE ---
    url = "https://amzn.in/d/dCKX9cU"  # The page to load
    screenshot_path = "screenshot.png"
    sender = "shakthinandanp0712@gmail.com"      # Your email address
    password = "tbrw gwdp falc zzcr"       # Your email app password
    receiver = "shakthinandanp0712@gmail.com"  # Recipient's email address
    subject = "Watch Today Price"
    body = "Fasttrack Watch Today Price" 

    # Click button and take screenshot
    asyncio.run(click_and_screenshot(url, screenshot_path))
    # Send email
    send_email_with_attachment(sender, password, receiver, subject, body, screenshot_path)
'''

from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://amzn.in/d/dCKX9cU")
    page.wait_for_timeout(5000)
    page.screenshot(path="")
    print(page.title())
    browser.close()'''