from playwright.sync_api import sync_playwright
import pandas as pd
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    url = "https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1BCAIotQFCAnBrSDNYA2i1AYgBAZgBCbgBF8gBDNgBAegBAYgCAagCA7gC95ikwwbAAgHSAiQ5ODkwZjBlZC00NDJjLTQxMmMtYWY5ZS01YmQxMzFlODViN2bYAgXgAgE&sid=0e218bc4f06eb1b2190123429c65e1a5&aid=356980&ss=+Islambad&ssne=Royal+Exective+Suite+F+8+Islambad&ssne_untouched=Royal+Exective+Suite+F+8+Islambad&lang=en-gb&src=searchresults&dest_id=12401388&dest_type=hotel&place_id=hotel%2F12401388&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=1&search_selected=true&search_pageview_id=3e435b9364270265&checkin=2025-07-08&checkout=2025-07-09&group_adults=1&no_rooms=1&group_children=0&nflt=price%3DPKR-min-5000-1"
    page.goto(url, timeout=60000)
    page.wait_for_load_state("networkidle")

    
    for _ in range(5):
        page.mouse.wheel(0, 1000)
        time.sleep(1)

    page.wait_for_selector("div[data-testid='property-card']", timeout=30000)
    hotels = page.query_selector_all("div[data-testid='property-card']")
    print(f"✅ Found {len(hotels)} hotels")

    data = []

    for i, hotel in enumerate(hotels):
        hotel.scroll_into_view_if_needed()
        time.sleep(0.5)

        name_el = hotel.query_selector("div[data-testid='title']")
        price_el = hotel.query_selector("span[data-testid='price-and-discounted-price'], span[data-testid='price']")
        location_el = hotel.query_selector("span[data-testid='address']")
        link_el = hotel.query_selector("a[data-testid='title-link']")
        sentiment_el = hotel.query_selector("div[class*='f63b14ab7a f546354b44 becbee2f63']")
        rating_el = hotel.query_selector("div[data-testid='review-score'] div:nth-child(2)")

        name = name_el.inner_text().strip() if name_el else "N/A"
        price = price_el.inner_text().strip() if price_el else "N/A"
        location = location_el.inner_text().strip() if location_el else "N/A"
        sentiment = sentiment_el.inner_text().strip() if sentiment_el else "N/A"
        rating = rating_el.inner_text().strip() if rating_el else "N/A"

        href = link_el.get_attribute("href") if link_el else None
        full_url = "https://www.booking.com" + href if href else "N/A"

        

        data.append({
            "Hotel Name": name,
            "Price": price,
            "Location": location,
            "Rating": rating,
            "Sentiment": sentiment,
            "Hotel Link": full_url
        })

    df = pd.DataFrame(data)
    df.to_excel("Booking.com.xlsx", index=False)
    print("✅ Done. Saved to Booking.com.xlsx")
    browser.close()





