import os
import re

# 误拦截修复白名单
AD_WHITELIST_PATTERNS = [
    r'\|\|alicdn\.com[\$\^]',  # 阿里CDN - 修正：支持$和^两种结束符
    r'\|\|bdstatic\.com[\$\^]', # 百度静态资源
    r'\|\|qq\.com[\$\^]',      # 腾讯系
    r'\|\|microsoft\.com[\$\^]', # 微软
    r'\|\|apple\.com[\$\^]',   # 苹果
    r'\|\|googleapis\.com[\$\^]', # Google APIs
    r'\|\|gstatic\.com[\$\^]', # Google静态资源
    r'\|\|github\.com[\$\^]',  # GitHub
    r'\|\|githubassets\.com[\$\^]', # GitHub资源
]

MALWARE_WHITELIST = [
    'localhost', '127.0.0.1', '::1',
    'test-server.local', 'dev-env.example',
    '192.168.', '10.0.', '172.16.'  # 添加内网IP段
]

ADULT_WHITELIST = [
    'health.gov', 'medical-site.com', 'sex-education.org',
    'who.int', 'cdc.gov'  # 添加权威健康机构
]

def apply_whitelist(category, input_file):
    """应用白名单过滤"""
    if not os.path.exists(input_file):
        print(f"⚠️  File not found: {input_file}")
        return False

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error reading {input_file}: {e}")
        return False

    # 提取规则行，保留注释但不在过滤时处理
    original_lines = [line for line in lines if line.strip()]
    rules = [line.strip() for line in lines if line.strip() and not line.startswith('!')]
    original_count = len(rules)

    # 应用白名单
    filtered_rules = []
    filtered_count = 0

    for rule in rules:
        should_filter = False

        if category == 'ad':
            # 使用正则表达式搜索，而不是search（避免部分匹配问题）
            should_filter = any(re.search(pattern, rule) for pattern in AD_WHITELIST_PATTERNS)
        elif category == 'malware':
            should_filter = any(wl in rule for wl in MALWARE_WHITELIST)
        elif category == 'adult':
            should_filter = any(wl in rule for wl in ADULT_WHITELIST)

        if not should_filter:
            filtered_rules.append(rule)
        else:
            filtered_count += 1

    # 回写文件
    try:
        with open(input_file, 'w', encoding='utf-8') as f:
            # 写入头部注释
            f.write(f'! Category: {category} (with whitelist processing)\n')
            f.write(f'! Original: {original_count} rules\n')
            f.write(f'! After whitelist: {len(filtered_rules)} rules\n')
            f.write(f'! Filtered: {filtered_count} rules\n')
            f.write(f'! Processing date: {os.popen("date").read().strip()}\n\n')

            # 写入过滤后的规则
            f.write('\n'.join(filtered_rules))
            if filtered_rules:  # 确保文件末尾有换行
                f.write('\n')

        print(f"✅ {category}: {original_count} → {len(filtered_rules)} rules (filtered: {filtered_count})")
        return True

    except Exception as e:
        print(f"❌ Error writing {input_file}: {e}")
        return False

def main():
    categories = ['ad', 'malware', 'adult']
    success_count = 0

    for cat in categories:
        input_file = f'filters/{cat}-blacklist.txt'
        if apply_whitelist(cat, input_file):
            success_count += 1

    print(f"\n✅ Whitelist processing complete! ({success_count}/{len(categories)} categories processed)")

if __name__ == '__main__':
    main()
