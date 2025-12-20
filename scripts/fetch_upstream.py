
import requests
import os
import time
from urllib.parse import urlparse

# 上游规则源配置
SOURCES = {
    'ads': [
        'https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt',
        'https://easylist-downloads.adblockplus.org/easylist.txt',
        'https://easylist-downloads.adblockplus.org/easylistchina.txt'
    ],
    'malware': [
        'https://malware-filter.pages.dev/urlhaus-filter-online.txt',
        'https://malware-filter.pages.dev/phishing-filter.txt'
    ],
    'adult': [
        'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts'
    ]
}

def download_file(url, filename):
    """下载单个文件"""
    try:
        print(f"  📥 Downloading: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 创建目录
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"  ✅ Saved to: {filename}")
        return True
    except Exception as e:
        print(f"  ❌ Failed to download {url}: {e}")
        return False

def fetch_all_sources():
    """获取所有上游规则"""
    print("🔄 Fetching upstream rules...")
    
    for category, urls in SOURCES.items():
        print(f"\n📂 Processing category: {category}")
        category_dir = os.path.join('sources', category)
        os.makedirs(category_dir, exist_ok=True)
        
        for i, url in enumerate(urls):
            filename = os.path.join(category_dir, f"{i+1}.txt")
            if not download_file(url, filename):
                print(f"  ⚠️  Continuing with other sources...")
            time.sleep(1)  # 避免请求过于频繁
            
    print("\n✅ All upstream sources fetched!")
    return True

if __name__ == '__main__':
    fetch_all_sources()
