import sys
from datetime import datetime
from pathlib import Path

from merge_rules import prune_redundant  # 复用裁剪逻辑

# 与 whitelist_processor.py 保持一致
CATEGORIES = {
    'ads': Path('filters/ads-blacklist.txt'),
    'malware': Path('filters/malware-blacklist.txt'),
    'adult': Path('filters/adult-blacklist.txt'),
}
WHITELIST_FILE = Path('Release/combined-whitelist.txt')
WHITELIST_MARK = '! ===== 白名单（内置）====='
OUTPUT = Path('filters/combined-rules.txt')


def collect_rules() -> set:
    """从分类文件收集 ||domain^ 规则（忽略注释与 @@ 行）"""
    all_rules = set()
    for path in CATEGORIES.values():
        if not path.exists():
            print(f"  ⚠️  Missing {path}")
            continue
        for line in path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line.startswith('||') and line.endswith('^'):
                all_rules.add(line[2:-1])
    return all_rules


def main() -> bool:
    print("🔄 Combining final rules...")

    all_rules = collect_rules()
    if not all_rules:
        print("  ❌ No rules collected, abort.")
        return False

    print(f"  📊 Collected {len(all_rules)} unique rules (global dedup)")

    before = len(all_rules)
    all_rules = prune_redundant(all_rules)
    if before != len(all_rules):
        print(f"  ✂️  Global prune: {before} -> {len(all_rules)}")

    whitelist_text = WHITELIST_FILE.read_text(encoding='utf-8') if WHITELIST_FILE.exists() else ''

    tmp_file = OUTPUT.with_name(OUTPUT.name + '.tmp')
    with open(tmp_file, 'w', encoding='utf-8') as f:
        f.write('! Title: H-i-H 综合黑名单（广告+恶意+成人）\n')
        f.write('! Description: 由 GitHub Actions 每日自动合并去重生成，白名单已内置\n')
        f.write('! Homepage: https://github.com/H-i-H/AdGuard-Home-Rules\n')
        f.write(f'! Last modified: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC+8\n')
        f.write('! Expires: 1 day\n')
        f.write(f'! Total rules: {len(all_rules)}\n')
        for rule in sorted(all_rules):
            f.write(f'||{rule}^\n')
        if whitelist_text:
            f.write('\n' + WHITELIST_MARK + '\n')
            f.write(whitelist_text.strip() + '\n')

    import os
    os.replace(tmp_file, OUTPUT)
    print(f"  💾 Saved {len(all_rules)} rules -> {OUTPUT}")

    size_mb = OUTPUT.stat().st_size / 1024 / 1024
    print(f"  📦 File size: {size_mb:.1f} MB")
    return True


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
