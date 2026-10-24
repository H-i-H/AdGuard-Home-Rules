import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional  

# 北京时间（UTC+8，无夏令时）
TZ_BEIJING = timezone(timedelta(hours=8))

# 必须与 fetch_upstream.py 的 SOURCES 键、README 订阅地址一致
CATEGORIES = ['ads', 'malware', 'adult']

RE_HOSTS = re.compile(r'^(?:0\.0\.0\.0|127\.0\.0\.1|::)\s+(\S+)', re.I)
RE_IPV4 = re.compile(r'^\d{1,3}(?:\.\d{1,3}){3}$')
RE_IPV6 = re.compile(r'^[0-9a-f:]+$')
RE_VALID = re.compile(r'^[^\s/^$*]+$')
SINKHOLE = {'0.0.0.0', '127.0.0.1', '::', '::1', 'localhost', 'broadcasthost',
            'localhost.localdomain', 'local', 'ip6-localhost'}

CATEGORY_TITLES = {
    'ads': 'H-i-H 广告黑名单',
    'malware': 'H-i-H 恶意网站黑名单',
    'adult': 'H-i-H 成人内容黑名单',
}


def _norm(candidate: str) -> Optional[str]:
    """规范化并校验；无效返回 None"""
    d = candidate.lower().strip().strip('.')
    if d.startswith('*.'):
        d = d[2:]
    if not d or d in SINKHOLE:
        return None
    if ':' in d:
        return d if RE_IPV6.match(d) and d.count(':') >= 2 else None
    if '.' not in d:
        return None
    return d if RE_VALID.match(d) else None


def extract_from_line(line: str) -> Optional[str]:
    """单行提取域名/IP。支持 hosts、||domain^、||domain^$mod、||IP^、|https://domain/path^、纯域名。
    跳过注释、@@ 放行、/正则/、元素隐藏(##)。
    """
    s = line.strip()
    if not s or s[0] in '!#/[<' or s.startswith('@@') or '##' in s:
        return None

    m = RE_HOSTS.match(s)
    if m:
        cand = m.group(1)
    else:
        cand = s.split()[0].lstrip('|')
        cand = re.sub(r'^https?://', '', cand)
        cand = cand.split('^')[0].split('$')[0].split('/')[0]
        if cand.count(':') == 1:
            cand = cand.split(':')[0]

    return _norm(cand)


def prune_redundant(domains: set) -> set:
    """父域已在集合中时，子域规则冗余（||父域^ 天然覆盖子域），予以删除"""
    out = set()
    for d in domains:
        if '.' not in d or d.replace('.', '').isdigit():
            out.add(d)
            continue
        parts = d.split('.')
        if not any('.'.join(parts[i:]) in domains for i in range(1, len(parts))):
            out.add(d)
    return out


def detect_file_type(lines) -> str:
    """仅用于日志展示，不参与解析决策"""
    sample = [s for s in (l.strip() for l in lines) if s and s[0] not in '!#['][:50]
    if not sample:
        return 'empty'
    if sum(1 for s in sample if RE_HOSTS.match(s)) > len(sample) // 2:
        return 'hosts'
    if sum(1 for s in sample if s.startswith('||')) > len(sample) // 2:
        return 'adguard'
    return 'plain/mixed'


def merge_category_rules(category: str) -> bool:
    """合并特定分类的规则"""
    print(f"  🔄 Merging {category} rules...")
    source_dir = Path('sources') / category

    if not source_dir.exists():
        print(f"  ⚠️  No sources directory: {source_dir}")
        return False

    files = [p for p in source_dir.glob('*') if p.is_file()]
    if not files:
        print(f"  ⚠️  No files in {source_dir}")
        return False

    all_rules = set()

    for filepath in files:
        print(f"    📄 Processing: {filepath.name}")
        try:
            lines = filepath.read_text(encoding='utf-8', errors='ignore').splitlines()
        except Exception as e:
            print(f"      ❌ Read error: {e}")
            continue

        print(f"      Detected format: {detect_file_type(lines)}")

        extracted = {d for d in (extract_from_line(l) for l in lines) if d}
        all_rules.update(extracted)
        print(f"      ➕ Extracted {len(extracted)} rules")

        if not extracted:
            size = filepath.stat().st_size
            sample = ' | '.join(l.strip() for l in lines[:5])[:300]
            print(f"      ⚠️ 0 rules extracted ({size} bytes). Sample: {sample}")

    if not all_rules:
        print(f"  ❌ No rules extracted for {category}")
        return False

    before = len(all_rules)
    all_rules = prune_redundant(all_rules)
    print(f"  ✂️  Pruned redundant subdomains: {before} -> {len(all_rules)}")

    output_dir = Path('filters')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f'{category}-blacklist.txt'

    try:
        tmp_file = output_file.with_name(output_file.name + '.tmp')
        with open(tmp_file, 'w', encoding='utf-8') as f:
            f.write(f"! Title: {CATEGORY_TITLES.get(category, category)}\n")
            f.write(f"! Source files: {len(files)}\n")
            f.write(f"! Total unique rules: {len(all_rules)}\n")
            f.write(f"! Last modified: {datetime.now(TZ_BEIJING).strftime('%Y-%m-%d %H:%M:%S')} UTC+8\n")
            f.write(f"! Homepage: https://github.com/H-i-H/AdGuard-Home-Rules\n")
            for rule in sorted(all_rules):
                f.write(f"||{rule}^\n")
        os.replace(tmp_file, output_file)
        print(f"  💾 {category}: {len(all_rules)} unique rules saved to {output_file}")
        return True
    except Exception as e:
        print(f"  ❌ Error saving {output_file}: {e}")
        return False


def merge_all_categories(categories: Optional[list] = None) -> bool:
    """合并所有分类规则"""
    print("🔄 Starting rule merging process...")

    if categories is None:
        categories = CATEGORIES

    if not Path('sources').exists():
        print("❌ 'sources' directory not found!")
        return False

    success_count = 0
    for category in categories:
        if merge_category_rules(category):
            success_count += 1

    ok = success_count == len(categories)
    print(f"\n{'✅' if ok else '❌'} Merging complete: {success_count}/{len(categories)} categories processed")
    return ok


if __name__ == '__main__':
    sys.exit(0 if merge_all_categories() else 1)
