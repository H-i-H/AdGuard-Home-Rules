import os
import re
import sys
from pathlib import Path

# ============ 配置 ============

# 白名单唯一来源（手工维护的构建输入）
WHITELIST_FILE = Path('Release/combined-whitelist.txt')
WHITELIST_MARK = '! ===== 白名单（内置）====='

# 分类黑名单：与 merge_rules.py 的输出一致
CATEGORIES = {
    'ads': Path('filters/ads-blacklist.txt'),
    'malware': Path('filters/malware-blacklist.txt'),
    'adult': Path('filters/adult-blacklist.txt'),
}

RE_HOSTS = re.compile(r'^(?:0\.0\.0\.0|127\.0\.0\.1|::)\s+(\S+)', re.I)


def load_whitelist(path: Path) -> set:
    """加载白名单：支持 @@||域名^$important 与裸域名，#/! 开头为注释"""
    whitelist = set()
    if not path.exists():
        print(f"  ❌ Whitelist file not found: {path}")
        return whitelist

    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith(('#', '!')):
            continue
        token = line.split()[0]
        m = re.match(r'^@@\|\|([^/^:\s]+)', token)
        domain = m.group(1) if m else token
        domain = domain.lower().strip('.').lstrip('*.')
        if domain and '.' in domain:
            whitelist.add(domain)

    print(f"  📋 Loaded {len(whitelist)} whitelist domains from {path}")
    return whitelist


def extract_domain(line: str):
    """从规则行提取域名；注释/正则/放行规则/无法识别的行返回 None（原样保留）"""
    s = line.strip()
    if not s or s[0] in '!#/' or s.startswith('@@'):
        return None

    m = RE_HOSTS.match(s)
    if m:
        candidate = m.group(1)
    else:
        s = s.lstrip('|')
        s = re.sub(r'^https?://', '', s)
        s = s.lstrip('*.')
        candidate = re.split(r'[/^:\s]', s, maxsplit=1)[0]

    domain = candidate.lower().strip('.')
    return domain if domain and '.' in domain else None


def is_whitelisted(domain: str, whitelist: set) -> bool:
    """域名或其任一父域命中白名单即放行（等价 @@||父域^ 语义）"""
    d = domain
    while True:
        if d in whitelist:
            return True
        dot = d.find('.')
        if dot == -1:
            return False
        d = d[dot + 1:]


def apply_whitelist(category: str, input_file: Path, whitelist: set, whitelist_text: str) -> bool:
    """剔除白名单命中的规则，并把白名单 @@ 行拼接到文件末尾（幂等）"""
    if not input_file.exists():
        print(f"  ❌ Input file not found: {input_file}")
        return False

    try:
        raw_text = input_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ❌ Read error {input_file}: {e}")
        return False

    # 幂等：去掉上次拼接的白名单段
    raw_text = raw_text.split(WHITELIST_MARK)[0]
    lines = raw_text.splitlines()

    if not lines:
        print(f"  ⚠️  Empty input: {input_file}")
        return False

    kept, removed = [], []
    for line in lines:
        domain = extract_domain(line)
        if domain and is_whitelisted(domain, whitelist):
            removed.append(domain)
            continue
        kept.append(line)

    kept.append('')
    kept.append(WHITELIST_MARK)
    kept.extend(whitelist_text.strip().splitlines())

    tmp_file = input_file.with_name(input_file.name + '.tmp')
    tmp_file.write_text('\n'.join(kept) + '\n', encoding='utf-8')
    os.replace(tmp_file, input_file)

    print(f"  ✅ {category}: {len(kept)} lines written, {len(removed)} rules removed")
    for domain in removed[:5]:
        print(f"     - {domain}")
    if len(removed) > 5:
        print(f"     ... and {len(removed) - 5} more")
    return True


def process_all() -> bool:
    """对所有分类应用白名单"""
    print("🔄 Applying whitelist (bake into blacklist)...")

    whitelist = load_whitelist(WHITELIST_FILE)
    if not whitelist:
        print("  ❌ Whitelist is empty or missing, abort.")
        return False

    whitelist_text = WHITELIST_FILE.read_text(encoding='utf-8')

    ok = 0
    for category, path in CATEGORIES.items():
        print(f"\n📂 Processing category: {category}")
        if apply_whitelist(category, path, whitelist, whitelist_text):
            ok += 1

    print(f"\n✅ Whitelist processing complete: {ok}/{len(CATEGORIES)} categories processed")
    return ok == len(CATEGORIES)


if __name__ == '__main__':
    sys.exit(0 if process_all() else 1)
