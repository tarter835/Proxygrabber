import sys
import requests
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
import socket

proxy_sources = {
    "http": [
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
        'https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt'
    ],
    "https": [
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
        'https://raw.githubusercontent.com/RX4096/proxy-list/main/online/https.txt'
    ],
    "socks4": [
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt'
    ],
    "socks5": [
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt',
        'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt'
    ]
}


def fetch_and_deduplicate(proxy_type):
    print(f"[+] Fetching {proxy_type} proxies...")
    urls = proxy_sources.get(proxy_type, [])
    combined = ""

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            combined += response.text + "\n"
        except Exception as e:
            print(f"[!] Failed to fetch from {url}: {e}")

    proxies = list(OrderedDict.fromkeys(combined.strip().splitlines()))
    with open(f"{proxy_type}.txt", "w") as f:
        f.write("\n".join(proxies))

    print(f"[+] Fetched {len(proxies)} {proxy_type.upper()} proxies.")
    return proxies


def check_proxy(proxy, proxy_type, timeout=5):
    test_url = "http://httpbin.org/ip"
    proxies = {}

    if proxy_type == "http" or proxy_type == "https":
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    elif proxy_type == "socks4":
        proxies = {
            "http": f"socks4://{proxy}",
            "https": f"socks4://{proxy}"
        }
    elif proxy_type == "socks5":
        proxies = {
            "http": f"socks5://{proxy}",
            "https": f"socks5://{proxy}"
        }

    try:
        r = requests.get(test_url, proxies=proxies, timeout=timeout)
        if r.status_code == 200:
            return proxy
    except:
        return None


def validate_proxies(proxy_type, proxies):
    print(f"[~] Validating {len(proxies)} {proxy_type} proxies...")

    valid = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_proxy, proxy, proxy_type) for proxy in proxies]
        for future in futures:
            result = future.result()
            if result:
                valid.append(result)

    with open(f"valid_{proxy_type}.txt", "w") as f:
        f.write("\n".join(valid))

    print(f"[✓] {len(valid)} valid {proxy_type.upper()} proxies saved to valid_{proxy_type}.txt\n")


if __name__ == "__main__":
    try:
        proxy_type = sys.argv[1].lower()
    except IndexError:
        print(f"Usage: python {sys.argv[0]} <proxy_type>")
        print("Available types: http, https, socks4, socks5, all")
        sys.exit(1)

    if proxy_type == "all":
        for p_type in proxy_sources.keys():
            proxies = fetch_and_deduplicate(p_type)
            validate_proxies(p_type, proxies)
    elif proxy_type in proxy_sources:
        proxies = fetch_and_deduplicate(proxy_type)
        validate_proxies(proxy_type, proxies)
    else:
        print(f"[ERROR] Invalid proxy type: {proxy_type}")
        print("Available types: http, https, socks4, socks5, all")
