"""Read-only DigitalOcean checks, run locally with DIGITALOCEAN_ACCESS_TOKEN.

No service creation, payment, token disclosure, or state mutations.
"""
from __future__ import annotations
import json
import os
import sys
import urllib.error
import urllib.request

TOKEN = os.getenv('DIGITALOCEAN_ACCESS_TOKEN')
if not TOKEN:
    print('NOT CONNECTED: Set DIGITALOCEAN_ACCESS_TOKEN locally (never paste it into chat or commit it).')
    sys.exit(2)

URLS = {
    'account': 'https://api.digitalocean.com/v2/account',
    'balance': 'https://api.digitalocean.com/v2/customers/my/balance',
    'apps': 'https://api.digitalocean.com/v2/apps?per_page=20',
}
for label, url in URLS.items():
    try:
        request = urllib.request.Request(url, headers={'Authorization': f'Bearer {TOKEN}', 'Accept': 'application/json'})
        with urllib.request.urlopen(request, timeout=12) as response:
            data = json.load(response)
        if label == 'balance':
            print('Balance response (check promotional credits separately under Billing):')
            for key in ('account_balance', 'month_to_date_balance', 'month_to_date_usage', 'generated_at'):
                if key in data:
                    print(' ', key, ':', data[key])
        elif label == 'apps':
            print('Existing DigitalOcean app count:', len(data.get('apps', [])))
            for app in data.get('apps', [])[:5]:
                print(' ', app.get('spec', {}).get('name', '(unnamed)'), app.get('live_url', '(no URL)'))
        else:
            print('DigitalOcean account API accessible: YES')
    except urllib.error.HTTPError as exc:
        print(label, ': HTTP', exc.code, '(check token scopes/billing state)')
    except Exception as exc:
        print(label, ':', type(exc).__name__, '(network/token check failed)')
