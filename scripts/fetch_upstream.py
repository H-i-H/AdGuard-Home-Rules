import sys
import time
import requests
from pathlib import Path
from urllib.parse import urlparse
from typing import Tuple

# 上游规则源配置
SOURCES = {
    'ads': [
        'https://anti-ad.net/easylist.txt',
        'https://raw.githubusercontent.com/BlueSkyXN/AdGuardHomeRules/master/all.txt',
        'https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt',
        'https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/dns.txt',
        'https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt',
        'https://raw.githubusercontent.com/ppfeufer/adguard-filter-list/refs/heads/master/blocklist',
        'https://raw.githubusercontent.com/KiryChanOfficial/AdFilterForAdGuard/refs/heads/main/KR_DNS_Filter.txt',
        'https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt',
        'https://cdn.jsdelivr.net/gh/banbendalao/ADgk@master/ADgk.txt',
        'https://raw.githubusercontent.com/kl0711/adRlues/refs/heads/main/Ad-rules.txt',
        'https://raw.githubusercontent.com/kl0711/adRlues/refs/heads/main/AdGuard-fanqie.txt',
        'https://raw.githubusercontent.com/lingeringsound/adblock_auto/refs/heads/main/Rules/adblock_auto.txt',
        'https://raw.githubusercontent.com/chinanjh/hosts/refs/heads/master/fuck%20youtube.txt',
        'https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt',
        'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt',
        'https://big.oisd.nl',
        'https://badmojr.github.io/1Hosts/Lite/hosts.txt',
        'https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt',
        'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts',
        'https://adaway.org/hosts.txt',
        'https://someonewhocares.org/hosts/zero/hosts',
        'https://easylist-downloads.adblockplus.org/easylist.txt',
        'https://easylist-downloads.adblockplus.org/easylistchina.txt',
        'https://easylist-downloads.adblockplus.org/easyprivacy.txt',
        'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt',
        'https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt',
        'https://raw.githubusercontent.com/blocklistproject/Lists/main/ads.txt'
    ],
    'malware': [
        'https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-agh-online.txt',
        'https://malware-filter.gitlab.io/malware-filter/phishing-filter-agh.txt'
    ],
    'adult': [
        'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts',
        'https://nsfw.oisd.nl'
    ]
}

# 请求配置
REQUEST_TIMEOUT = 30
RETRY_DELAY = 2
MAX_RETRIES = 3
MIN_FILE_SIZE = 50  # 最小文件大小（字节）
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def get_filename_from_url(url: str) -> str:
    """从URL生成有意义且不冲突的文件名（保留最后两级路径）"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    path_parts = [p for p in parsed.path.split('/') if p]

    if path_parts:
        # 每级去掉扩展名再拼，避免出现 xxx.txt.txt
        name = '_'.join(p.rsplit('.', 1)[0] for p in path_parts[-2:])
    else:
        name = 'index'
    name = name.replace('%20', '-')
    return f"{domain}_{name}.txt"


def download_with_retry(url: str, filepath: Path, max_retries: int = MAX_RETRIES) -> Tuple[bool, str]:
    """带重试机制的下载"""
    for attempt in range(max_retries):
        try:
            print(f"    📥 Attempt {attempt + 1}/{max_retries}: {url}")

            response = requests.get(
                url,
                headers={'User-Agent': USER_AGENT},
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True,
                verify=True
            )
            response.raise_for_status()

            # 验证内容
            content = response.content
            if len(content) < MIN_FILE_SIZE:
                return False, f"File too small ({len(content)} bytes)"

            # 检查是否返回HTML错误页面（仅靠内容嗅探）
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' in content_type:
                head = content[:200].lower()
                if b'<html' in head or b'<!doctype' in head:
                    return False, "Response appears to be HTML error page"

            # 保存文件
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(content)

            return True, f"Saved {len(content)} bytes"

        except requests.exceptions.Timeout:
            if attempt == max_retries - 1:
                return False, "Timeout after all retries"
            print(f"    ⚠️  Timeout, retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

        except requests.exceptions.HTTPError as e:
            code = e.response.status_code if e.response is not None else 'unknown'
            if code in RETRYABLE_STATUS and attempt < max_retries - 1:
                wait = RETRY_DELAY * (attempt + 1)
                print(f"    ⚠️  HTTP {code}, retrying in {wait}s...")
                time.sleep(wait)
                continue
            return False, f"HTTP {code}"

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return False, f"Network error: {e}"
            print(f"    ⚠️  Error: {e}, retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

    return False, "Unknown error"


def fetch_all_sources():
    """获取所有上游规则，返回总体统计与各分类成功数"""
    print("🔄 Fetching upstream rules...")

    stats = {'success': 0, 'failed': 0, 'skipped': 0}
    category_success = {category: 0 for category in SOURCES}

    for category, urls in SOURCES.items():
        print(f"\n📂 Processing category: {category}")
        category_dir = Path('sources') / category
        category_dir.mkdir(parents=True, exist_ok=True)

        for url in urls:
            filename = get_filename_from_url(url)
            filepath = category_dir / filename

            # 检查是否已存在且有效
            if filepath.exists():
                size = filepath.stat().st_size
                if size > MIN_FILE_SIZE:
                    print(f"    ⏭️  Already exists: {filename} ({size} bytes)")
                    stats['skipped'] += 1
                    category_success[category] += 1
                    continue
                filepath.unlink()  # 删除无效的旧文件

            success, message = download_with_retry(url, filepath)

            if success:
                print(f"    ✅ {message} -> {filename}")
                stats['success'] += 1
                category_success[category] += 1
            else:
                print(f"    ❌ {message}")
                stats['failed'] += 1

            # 避免请求过于频繁
            time.sleep(RETRY_DELAY)

    print(f"\n📊 Summary: {stats['success']} succeeded, {stats['failed']} failed, {stats['skipped']} skipped")
    return stats, category_success


def validate_downloaded_files():
    """验证下载的文件"""
    print("\n🔍 Validating downloaded files...")

    issues = []

    # 文件名冲突自检（冲突会让某个源永远被静默跳过）
    for category, urls in SOURCES.items():
        names = [get_filename_from_url(u) for u in urls]
        dupes = sorted({n for n in names if names.count(n) > 1})
        if dupes:
            issues.append(f"Filename collision in '{category}': {dupes}")

    for category in SOURCES:
        category_dir = Path('sources') / category
        if not category_dir.exists():
            issues.append(f"Missing directory: {category_dir}")
            continue

        # 预期文件齐全性
        expected = {get_filename_from_url(u) for u in SOURCES[category]}
        existing = {p.name for p in category_dir.glob('*.txt')}
        for missing in sorted(expected - existing):
            issues.append(f"Missing file: {category_dir / missing}")

        for filepath in category_dir.glob('*.txt'):
            size = filepath.stat().st_size
            if size < MIN_FILE_SIZE:
                issues.append(f"Small file ({size} bytes): {filepath}")
                continue
            try:
                content = filepath.read_text(encoding='utf-8', errors='ignore')
                if not content.strip():
                    issues.append(f"File contains only whitespace: {filepath}")
            except Exception as e:
                issues.append(f"Cannot read file: {filepath} ({e})")

    if issues:
        print("  ⚠️  Validation issues found:")
        for issue in issues:
            print(f"    - {issue}")
        return False

    print("  ✅ All files validated")
    return True


if __name__ == '__main__':
    stats, category_success = fetch_all_sources()
    validate_ok = validate_downloaded_files()

    if stats['success'] + stats['skipped'] == 0:
        print("\n❌ All downloads failed.")
        sys.exit(1)

    empty_categories = [c for c, n in category_success.items() if n == 0]
    if empty_categories:
        print(f"\n❌ No sources available for category: {empty_categories}")
        sys.exit(1)

    if not validate_ok:
        print("\n⚠️  Validation reported issues (see above), continuing.")
    if stats['failed'] > 0:
        print(f"\n⚠️  {stats['failed']} source(s) failed, continuing with partial data.")
