import requests
import os
import time
import concurrent.futures
from pathlib import Path
from urllib.parse import urlparse
from typing import Tuple, Optional

# 上游规则源配置
SOURCES = {
    'ads': [
        'https://raw.githubusercontent.com/ppfeufer/adguard-filter-list/refs/heads/master/blocklist',
        'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt',
        'https://easylist-downloads.adblockplus.org/easylist.txt',
        'https://easylist-downloads.adblockplus.org/easylistchina.txt',
        'https://raw.githubusercontent.com/chinanjh/hosts/refs/heads/master/fuck%20youtube.txt',
        'https://raw.githubusercontent.com/BlueSkyXN/AdGuardHomeRules/master/all.txt',
        'https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt',
        'https://cdn.jsdelivr.net/gh/banbendalao/ADgk@master/ADgk.txt',
        'https://raw.githubusercontent.com/lingeringsound/adblock_auto/refs/heads/main/Rules/adblock_auto.txt',
        'https://raw.githubusercontent.com/kl0711/adRlues/refs/heads/main/Ad-rules.txt',
        'https://raw.githubusercontent.com/kl0711/adRlues/refs/heads/main/AdGuard-fanqie.txt',
        'https://raw.githubusercontent.com/KiryChanOfficial/AdFilterForAdGuard/refs/heads/main/KR_DNS_Filter.txt',
        'https://raw.githubusercontent.com/H-i-H/AdGuard-Home-Rules/refs/heads/main/Release/Supplement-rules.txt',
        'https://anti-ad.net/easylist.txt'
    ],
    'malware': [
        'https://malware-filter.pages.dev/urlhaus-filter-online.txt',
        'https://malware-filter.pages.dev/phishing-filter.txt'
    ],
    'adult': [
        'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts'
    ]
}

# 请求配置
REQUEST_TIMEOUT = 30
RETRY_DELAY = 2
MAX_RETRIES = 3
MIN_FILE_SIZE = 50  # 最小文件大小（字节）
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

def get_filename_from_url(url: str) -> str:
    """从 URL 生成有意义的文件名"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    path_parts = [p for p in parsed.path.split('/') if p]

    if path_parts:
        name = path_parts[-1].split('.')[0]  # 去掉扩展名
        return f"{domain}_{name}.txt"
    return f"{domain}.txt"

def download_with_retry(url: str, filepath: Path, max_retries: int = MAX_RETRIES) -> Tuple[bool, str]:
    """带重试机制的下载"""
    for attempt in range(max_retries):
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(
                url,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True,
                verify=True
            )
            response.raise_for_status()

            content = response.content
            if len(content) < MIN_FILE_SIZE:
                return False, f"File too small ({len(content)} bytes)"

            # 检查是否返回 HTML 错误页面 (修复了原代码截断的问题)
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' in content_type and 'filter' not in url:
                if b'<html' in content.lower() or b'<body' in content.lower():
                    return False, "Received HTML error page"

            # 【关键】：强制覆盖写入，确保文件内容更新，配合 YAML 的哈希对比
            filepath.write_bytes(content)
            filename = get_filename_from_url(url)
            return True, f"Downloaded {filename}"

        except Exception as e:
            if attempt == max_retries - 1:
                return False, f"Failed: {str(e)}"
            time.sleep(RETRY_DELAY)
    
    return False, "Max retries exceeded"

def process_single_url(url: str, category: str) -> Tuple[str, bool, str]:
    """处理单个 URL 的下载逻辑（供并发调用）"""
    category_dir = Path('sources') / category
    category_dir.mkdir(parents=True, exist_ok=True)
    filename = get_filename_from_url(url)
    filepath = category_dir / filename

    # 【关键修复】：移除“文件存在则跳过”的逻辑，必须每次都强制下载覆盖！
    # 否则 YAML 中的 MD5 哈希对比会永远返回“无变化”，导致规则永远不更新。
    success, message = download_with_retry(url, filepath)
    return url, success, message

def fetch_all_sources():
    """并发获取所有源"""
    print("🚀 Starting upstream sources fetch (Concurrent Mode)...")
    
    tasks = []
    for category, urls in SOURCES.items():
        for url in urls:
            tasks.append((url, category))

    stats = {'success': 0, 'failed': 0}
    
    # 使用线程池并发下载，最多 10 个并发
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_single_url, url, cat): url for url, cat in tasks}
        
        for future in concurrent.futures.as_completed(futures):
            url, success, message = future.result()
            if success:
                stats['success'] += 1
                print(f"  ✅ {message}")
            else:
                stats['failed'] += 1
                print(f"  ❌ {url} -> {message}")

    print(f"\n📊 Summary: {stats['success']} succeeded, {stats['failed']} failed")
    return stats['failed'] == 0

def validate_downloaded_files():
    """验证下载的文件"""
    print("\n🔍 Validating downloaded files...")
    issues = []
    for category in SOURCES.keys():
        category_dir = Path('sources') / category
        if not category_dir.exists():
            continue

        for filepath in category_dir.glob('*.txt'):
            size = filepath.stat().st_size
            if size == 0:
                issues.append(f"Empty file: {filepath}")
            elif size < MIN_FILE_SIZE:
                issues.append(f"Small file ({size} bytes): {filepath}")

    if issues:
        print("  ⚠️ Validation issues found:")
        for issue in issues:
            print(f"    - {issue}")
        return False

    print("  ✅ All files validated")
    return True

if __name__ == '__main__':
    success = fetch_all_sources()
    if success:
        validate_downloaded_files()
    else:
        print("\n❌ Some downloads failed. Please check the logs.")
        exit(1)
