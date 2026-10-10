from playwright.sync_api import sync_playwright
import re
import json
import os

print("Ανάφλεξη! Ψάχνω για ευκαιρίες Mazda MX-5...")

TARGET_URL = "https://www.car.gr/used-cars/mazda/mx-5.html?category=15001&crashed=f&make=13303&media_types=photo&model=14461&offer_type=sale&pg=1&price-from=1500&price-to=5000&withprice=1"

found_deals = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    print("Μπαίνω στο car.gr...")
    page.goto(TARGET_URL)
    
    try:
        page.locator("text=€").first.wait_for(timeout=20000)
    except Exception:
        print("Δεν βρέθηκε καμία αγγελία ή Cloudflare timeout.")
    
    try:
        page.locator("button:has-text('ΔΙΑΦΩΝΩ')").first.click(timeout=3000)
        page.wait_for_timeout(3000)
    except Exception:
        pass

    print("Σαρώνω τη σελίδα για εικόνες, χιλιόμετρα και χρονολογίες...")
    
    # Σκρολάρουμε λίγο προς τα κάτω για να "ξεγελάσουμε" το site και να φορτώσει τις εικόνες (Lazy Loading)
    page.mouse.wheel(0, 2000)
    page.wait_for_timeout(1500)

    all_links = page.locator("a").all()
    
    for element in all_links:
        text = element.inner_text()
        href = element.get_attribute("href")
        
        if text and href and '€' in text and ('Km' in text or 'cc' in text):
            price_match = re.search(r'([\d\.]+)\s*€', text)
            if price_match:
                clean_price = price_match.group(1).replace('.', '')
                if clean_price.isdigit():
                    price = int(clean_price)
                    
                    if 1000 <= price <= 5000:
                        # 1. Εξαγωγή Χιλιομέτρων
                        km_match = re.search(r'([\d\.]+)\s*Km', text, re.IGNORECASE)
                        mileage = km_match.group(1) + " Km" if km_match else "Άγνωστα"
                        
                        # 2. Εξαγωγή Χρονολογίας (ψάχνουμε 4ψήφιο μεταξύ 1980 και 2029)
                        year_match = re.search(r'\b(19[8-9]\d|20[0-2]\d)\b', text)
                        year = year_match.group(1) if year_match else "Άγνωστη"
                        
                        # 3. Εξαγωγή Εικόνας (Αν δεν βρει, βάζει μια έτοιμη γκρίζα εικόνα placeholder)
                        image_url = "https://via.placeholder.com/400x300?text=No+Photo"
                        try:
                            img_locator = element.locator("img").first
                            src = img_locator.get_attribute("src")
                            if src and src.startswith("http"):
                                image_url = src
                        except Exception:
                            pass

                        full_url = f"https://www.car.gr{href}" if href.startswith('/') else href
                            
                        # Αποθήκευση της αγγελίας με ΟΛΑ τα νέα δεδομένα
                        if not any(d['link'] == full_url for d in found_deals): 
                            found_deals.append({
                                "title": f"Mazda MX-5",
                                "price": price,
                                "year": year,
                                "mileage": mileage,
                                "image": image_url,
                                "link": full_url
                            })

    browser.close()

# --- ΕΜΦΑΝΙΣΗ ΚΑΙ ΑΠΟΘΗΚΕΥΣΗ ---
if len(found_deals) > 0:
    sorted_deals = sorted(found_deals, key=lambda x: x['price'])
    print(f"\nΒρέθηκαν {len(sorted_deals)} ευκαιρίες! Τα αποθηκεύω στο mx5.json...")
    
    
    output_path = os.path.join('mx5-ui', 'src', 'mx5.json')

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_deals, f, ensure_ascii=False, indent=4)
        
    print("ΕΠΙΤΥΧΙΑ! Το αρχείο mx5.json αναβαθμίστηκε!")
else:
    print("Δυστυχώς δεν βρέθηκε κανένα MX-5 κάτω από 5.000€.")