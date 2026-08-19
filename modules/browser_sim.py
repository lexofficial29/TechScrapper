from playwright.sync_api import sync_playwright
import time
import json
import concurrent.futures

def load_rules(filepath='data/markers.json'):
    with open(filepath, 'r') as f:
        return json.load(f)

def analyze_technology(url):
    if not url.lower().startswith(("http://", "https://")):
        url = "http://" + url

    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 ...")
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)

            time.sleep(2)

            content = page.content().lower() 

            rules = load_rules()
            for rule in rules:
                for marker in rule["markers"]:
                    if marker in content:
                        results.append({
                            "tech": rule["name"],
                            "proof": rule["proof"]
                        })
                        
        
            unique_results = {res['tech']: res for res in results}.values()
            return [url, list(unique_results)]

        except Exception as e:
            print(f"Error loading {url}: {e}")
            return [url, []]
        finally:
            browser.close()

def start_sim(url_list, max_threads=5):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        threaded_results = executor.map(analyze_technology, url_list)
        
        for data in threaded_results:
            results.append(data)
            print(f"Finished scanning: {data}")
            
    return results