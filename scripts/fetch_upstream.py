import requests
import os
from datetime import datetime
import time

# 规则源配置
SOURCES = {
    'ad': [
        'https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule.txt',
        'https://raw.githubusercontent.com/damengzhu/abpmerge/main/abpmerge.txt',  # 直接使用原始URL
    ],
    'privacy': [
        'https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_11_Mobile/filter.txt',
        'https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_3_Social_media/filter.txt',
    ],
    'malware': [
        'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts',
        'https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Browsing_security/filter.txt',
    ],
    'adult': [
        'https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_16_Adult/filter.txt',
    ]
}

def fetch_with_retry(url, max_retries=3, timeout=30):
    """带重试的请求函数"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return response.text
            else:
                print(f"      ⚠️  Status {response.status_code}, retry {attempt + 1}/{max_retries}")
        except Exception as e:
            print(f"      ❌ Error: {str(e)[:50]}, retry {attempt + 1}/{max_retries}")

        if attempt < max_retries - 1:
            time.sleep(2)  # 等待2秒后重试

    return None

def fetch_and_save():
    os.makedirs('sources', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    success_count = 0

    for category, urls in SOURCES.items():
        print(f"\n📥 Fetching {category} rules...")
        all_rules = []

        for i, url in enumerate(urls):
            print(f"  → Source {i+1}: {url[:60]}...")
            content = fetch_with_retry(url)

            if content:
                lines = content.split('\n')
                all_rules.extend(lines)
                print(f"    ✅ Fetched {len(lines)} lines")
                success_count += 1
            else:
                print(f"    ❌ Failed to fetch: {url[:60]}...")

        # 只有在获取到数据时才保存
        if all_rules:
            filename = f'sources/{category}_{timestamp}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f'! Category: {category}\n')
                f.write(f'! Fetched: {datetime.now()}\n')
                f.write(f'! Total sources: {len(urls)}\n')
                f.write('\n'.join(all_rules))

            print(f"  💾 Saved to {filename} ({len(all_rules)} total lines)")
        else:
            print(f"  ⚠️  No rules fetched for {category}, skipping save")

    # 检查整体成功率
    total_sources = sum(len(urls) for urls in SOURCES.values())
    if success_count == 0:
        print("\n❌ Failed to fetch any rules!")
        return False
    elif success_count < total_sources:
        print(f"\n⚠️  Partial success: {success_count}/{total_sources} sources fetched")
        return True
    else:
        print(f"\n✅ All upstream rules fetched successfully!")
        return True

if __name__ == '__main__':
    success = fetch_and_save()
    exit(0 if success else 1)
