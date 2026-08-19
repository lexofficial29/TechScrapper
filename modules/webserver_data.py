import requests
import concurrent.futures

def get_webserver(url):
    if not url.lower().startswith(("http://", "https://")):
        url = "http://" + url
    try:
        response = requests.get(url, timeout=30, allow_redirects=True)
        headers = response.headers
        content = response.text.lower()
        webserver = headers.get("Server", "Unknown")
        cookie_str = str(headers.get("Set-Cookie", "")).lower()
        found_platforms = []

        if "x-powered-by" in headers:
            found_platforms.append({"tech": headers["X-Powered-By"], "proof": "Detected 'X-Powered-By' header."})

        if "shopify" in webserver.lower():
            found_platforms.append({"tech": "Shopify", "proof": "Detected 'Shopify' in the Server header."})
        
        if "shop_id" in cookie_str or "shopify" in cookie_str:
            if "Shopify" not in found_platforms:
                found_platforms.append({"tech": "Shopify", "proof": "Detected 'Shopify' in the Set-Cookie header."})

        if "shopify" in content or "cdn.shopify.com" in content:
            if "Shopify" not in found_platforms:
                found_platforms.append({"tech": "Shopify", "proof": "Detected 'Shopify' in the content."})

        if "wp-content" in content or "wordpress" in content:
            if "WordPress" not in found_platforms:
                found_platforms.append({"tech": "WordPress", "proof": "Detected 'WordPress' in the content."})

        if found_platforms:
            return {
                "url": url,
                "webserver": webserver,
                "platforms": found_platforms
            }
        
        return {
            "url": url,
            "webserver": webserver,
            "platforms": {"tech": "Not detected", "proof": "No specific platform markers found."}
        }

    except Exception:
        return {
            "url": url,
            "webserver": "Not detected",
            "platforms": {"tech": "Not detected", "proof": "Error occurred while scanning."}
        }

def scan_webservers(url_list, max_threads=10):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        threaded_results = executor.map(get_webserver, url_list)
        
        for data in threaded_results:
            results.append(data)
            print(f"Finished scanning: {data['url']} -> {data["webserver"]} | {data['platforms']}")
            
    return results