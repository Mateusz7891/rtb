from playwright.sync_api import sync_playwright

from helper import extract_positions_data, save_positions_to_json, \
    count_job_offers
from pages.PoistionsPage import assertPositionsNumber, showAllRemoteJobs


def filterPageAndSaveJsonWithData(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.rtbhouse.com/careers-offers")

    showAllRemoteJobs(page)

    job_number = count_job_offers(page)

    assertPositionsNumber(page, job_number)

    positions = extract_positions_data(page, 15)

    save_positions_to_json(positions)

    browser.close()


with sync_playwright() as playwright:
    filterPageAndSaveJsonWithData(playwright)
