import http.client
import urllib.parse

def test_phpmyadmin(host="192.168.1.16", port=80, path="/phpMyAdmin/themes/original/img/logo_right.png"):
    # Body identico a quello visto su Burp
    body_data = {
        "pma_username": "root",
        "pma_password": "",
        "server": "1",
        "lang": "en",
        "token": "e1ac3d57e592bebe00bdf33252fb9386"
    }
    encoded_body = urllib.parse.urlencode(body_data)

    # Header basati su Burp
    headers = {
        "Host": host,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/139.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"http://{host}/phpMyAdmin/",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": f"http://{host}",
        "Connection": "close",
        "Cookie": "phpMyAdmin=ab5b7a5234dc8f6c8272134778ae6e667e54c58; pma_lang=en-utf-8; pma_charset=utf-8"
    }

    verbs = ["GET", "POST", "HEAD", "PUT", "DELETE"]
    results = []

    for verb in verbs:
        conn = http.client.HTTPConnection(host, port, timeout=5)
        print(f"\n--- Testing {verb} {path} ---")
        try:
            if verb == "POST":
                conn.request(verb, path, body=encoded_body, headers=headers)
            else:
                conn.request(verb, path, headers=headers)

            res = conn.getresponse()
            data = res.read().decode("utf-8", errors="ignore")
            print(f"Status: {res.status} {res.reason}")
            print(f"Server: {res.getheader('Server')}")
            print(f"Set-Cookie: {res.getheader('Set-Cookie')}")
            print(f"Location: {res.getheader('Location')}")
            print(f"Body length: {len(data)} chars")
            print("-" * 60)
            results.append((verb, res.status, res.reason))
        except Exception as e:
            print(f"Errore: {e}")
        finally:
            conn.close()

    print("\n=== Riepilogo ===")
    for v, s, r in results:
        print(f"{v:6} → {s} {r}")

if __name__ == "__main__":
    test_phpmyadmin()
