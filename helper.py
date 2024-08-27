import json
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from model.Position import Position


def click_see_more(page):
    while True:
        try:
            if page.is_visible('role=button[name="See more"]'):
                page.click('role=button[name="See more"]')
            else:
                print("'See more' button is not visible.")
                break
        except TimeoutError:
            print("Timeout exceeded.")
            break


def count_job_offers(page):
    try:
        job_number = page.locator('a[href*="/careers-offers"]').count()
        return job_number
    except Exception as e:
        print(f"Error while counting job offers: {e}")
        return 0


def extract_positions_data(page, positions_number):
    try:
        soup = BeautifulSoup(page.content(), 'html.parser')
        position_elements = soup.select('div.sc-acbd9527-2.gRSddi')[:positions_number]

        positions = [
            Position(
                element.select_one('span.sc-acbd9527-5.ctqJqd').text,
                element.select_one('p.sc-5cd84594-0.diUEBQ').text,
                element.select_one('div.sc-acbd9527-7.esWJUe span').text,
                element.select_one('a[data-testid="button"]')['href']
            )
            for element in position_elements
        ]

        for position in positions:
            print(
                f"Role Name: {position.role_name}, Work Mode: {position.work_mode}, Location: {position.location}, Offer URL: {position.offer_url}")

        return positions

    except Exception as e:
        print(f"Error while extracting positions data: {e}")
        return []


def save_positions_to_json(positions):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'positions_{timestamp}.json'

    folder_path = 'jsons'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, filename)

    positions_data = [
        {
            "role_name": position.role_name,
            "work_mode": position.work_mode,
            "location": position.location,
            "offer_url": f"https://www.rtbhouse.com{position.offer_url}"
        }
        for position in positions
    ]

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(positions_data, json_file, ensure_ascii=False, indent=4)

    print(f"Data saved to {file_path}")
