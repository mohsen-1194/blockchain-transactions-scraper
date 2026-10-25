import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

URL = "https://eth.blockscout.com/txs"
REAL_ROWS_LINK = 'table tbody a[href^="/tx/"]:not([data-loading="true"])'
NUM_PAGES = 10


def wait_for_rows(page, previous_first: str | None = None) -> None:
    # need some work here for checking new rows with old ones
    try:
        if previous_first is None:
            page.wait_for_selector(REAL_ROWS_LINK, timeout=30000)  # first page
        else:
            page.wait_for_function(
                """(old) => {
                        const a = document.querySelector('table tbody a[href^="/tx/"]:not([data-loading="true"])');
                        return a && a.getAttribute('href') !== old;
                    }""",
                arg=previous_first,
                timeout=30000,
            )
    except PlaywrightTimeout:
        page.screenshot(path="debug.png", full_page=True)
        raise


def scroll_down(page) -> None:
    previous = 0
    for _ in range(10):  # safety limit
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1500)  # give the page time to add rows
        count = page.locator(REAL_ROWS_LINK).count()
        if count == previous:
            return
        previous = count


def next_page(page) -> str | None:
    next_btn = page.get_by_role("button", name="Next page")
    if next_btn.is_disabled():
        return None

    before = page.locator(REAL_ROWS_LINK).first.get_attribute("href")
    next_btn.click()

    # wait for rows to load
    try:
        wait_for_rows(page, before)
    except PlaywrightTimeout:
        print("page did not change after click, stopping")
        return None

    # scroll down to bottom of the page
    scroll_down(page)

    html = page.content()
    return html


def fetch_page(url: str, page) -> str:
    page.goto(url)

    # wait for rows to load
    wait_for_rows(page)
    # toggle the time. only need once
    page.get_by_role("button", name="Toggle time format").click()
    page.wait_for_function(
        "() => ![...document.querySelectorAll('table tbody tr')].some(r => /\\bago\\b/.test(r.innerText))",
        timeout=15000,
    )
    # scroll down to bottom of the page
    scroll_down(page)

    html = page.content()
    return html


def scrape_page(soup: BeautifulSoup) -> list:
    txs = []
    for row in soup.select("table tbody tr"):
        tag = row.select_one("a[href^='/tx/']:not([data-loading='true'])")
        if tag is None:
            continue
        transaction_id = tag.get("href").split("/tx/")[1]

        new_tag = tag.parent.find_next_sibling("div")
        timestamp = new_tag.get_text(strip=True)

        tags = row.select("a[href^='/address/']")
        sender_address = tags[0].get("href").split("/address/")[1] if tags else None
        recipient_address = (
            tags[1].get("href").split("/address/")[1] if len(tags) > 1 else None
        )

        new_tag2 = row.select_one("td:nth-of-type(7)")
        amount_transferred = new_tag2.get_text(strip=True).split("$")[0]

        txs.append(
            {
                "transaction_id": transaction_id,
                "timestamp": timestamp,
                "sender_address": sender_address,
                "recipient_address": recipient_address,
                "amount_transferred": amount_transferred,
            }
        )

    return txs


def save_to_csv(data: list) -> None:
    df = pd.DataFrame(data)

    try:
        df.to_csv("transactions.csv", index=False)
        print("File written successfully.")

    except PermissionError:
        print(
            "Error: Permission denied. The file might be open in another program like Excel."
        )

    except OSError as e:
        print(f"System or Disk I/O error occurred: {e}")


def main() -> None:
    data = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        html = fetch_page(URL, page)

        for i in range(NUM_PAGES):
            soup = BeautifulSoup(html, "html.parser")
            page_data = scrape_page(soup)

            for row in page_data:  # removing duplicates
                data[row["transaction_id"]] = row

            html = next_page(page)
            if html is None:
                break

        browser.close()

    save_to_csv(list(data.values()))


if __name__ == "__main__":
    main()
