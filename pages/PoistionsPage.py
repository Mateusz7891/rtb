from playwright.sync_api import expect

from helper import click_see_more


def assertPositionsNumber(page, job_number):
    print(f"There are {job_number} positions that are remote currently")
    expect(page.locator("h1")).to_contain_text(f"{job_number} positions in all locations")


def showAllRemoteJobs(page):
    page.get_by_label("Allow all").click()
    page.get_by_placeholder("On-site/remote/hybrid").click()
    page.get_by_role("option", name="Remote").click()
    click_see_more(page)


class PositionsPage:

    def __init__(self, page):
        self.page = page
