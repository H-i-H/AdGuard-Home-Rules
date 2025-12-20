import os

# 确保目录存在
os.makedirs('scripts', exist_ok=True)

#要写入的Python代码
code = '''import os
import re
import requests
from datetime import datetime

# 误拦截高风险域名白名单（个人测试环境）
PERSONAL_WHITELIST = {
    'ad': {
        '||alicdn.com$',  # 阿里CDN
        '||bdstatic.com$', # 百度静态资源
        '||qq.com$',      # 腾讯系
        '||microsoft.com$', # 微软更新
    },
    'malware': {
        'localhost', '127.0.0.1', '::1',
        '||test-server.local$', '||dev-env.example$',
    },
    'adult': {
        'health.gov', 'medical-site.com', 'sex-education.org'
    }
}

def is_valid_rule(line):
    """验证规则有效性"""
    if not line or line.startswith(('!', '[', '#')):
        return False

    line = line.strip()
    if not line:
        return False

    # 过滤过于宽泛的规则
    if re.match(r'^\\|\\|[^\\.]+\\.[a-z]+$', line):
        return False

    # 过滤无效的主机文件格式
    if line.startswith('0.0.0.0 ') or line.startswith('127.0.0.1 '):
        parts = line.split()
        if len(parts) >= 2:
            domain = parts[1]
            if domain == 'localhost' or domain.startswith('127.'):
                return False

    return True

def normalize_rule(line):
    """标准化规则格式"""
    line = line.strip()

    # 转换hosts格式到adblock格式
    if line.startswith('0.0.0.0 ') or line.startswith('127.0.0.1 '):
        parts = line.split()
        if len(parts) >= 2:
            domain = parts[1]
            return f'||{domain}^'
        else:
            return line  # 无效格式保持原样

    # 确保以||开头（域名规则）
    if line.startswith('||') or line.startswith('|http'):
        return line

    return line

def process_category(category):
    """处理单个类别的规则"""
    print(f"\\n🔄 Processing {category} category...")

    # 查找最新的源文件
    source_files = [f for f in os.listdir('sources') if f.startswith(f'{category}_')]
    if not source_files:
        print(f"  ⚠️  No source files found for {category}")
        return []

    # 读取最新文件（按文件名排序）
    latest_file = sorted(source_files)[-1]
    print(f"  📖 Reading from {latest_file}")

    try:
        with open(f'sources/{latest_file}', 'r', encoding='utf-8') as f:
            raw_rules = f.readlines()
    except FileNotFoundError:
        print(f"  ❌ File not found: sources/{latest_file}")
        return []
    except Exception as e:
        print(f"  ❌ Error reading file: {e}")
        return []

    # 处理规则
    processed = set()
    for line in raw_rules:
        if is_valid_rule(line):
            normalized = normalize_rule(line)
            # 应用个人白名单
            if normalized not in PERSONAL_WHITELIST.get(category, set()):
                processed.add(normalized)

    print(f"  ✅ Processed: {len(raw_rules)} → {len(processed)} unique rules")
    return sorted(list(processed))

def main():
    # 确保必要的目录存在
    os.makedirs('sources', exist_ok=True)
    os.makedirs('filters', exist_ok=True)

    all_categories = ['ad', 'privacy', 'malware', 'adult']

    for category in all_categories:
        rules = process_category(category)

        if rules:
            output_file = f'filters/{category}-blacklist.txt'
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f'! Category: {category}\\n')
                    f.write(f'! Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\\n')
                    f.write(f'! Original source: AWAvenue + Multi-source\\n')
                    f.write(f'! Total rules: {len(rules)}\\n')
                    f.write(f'! Personal whitelist applied: {len(PERSONAL_WHITELIST.get(category, set()))} entries\\n\\n')
                    f.write('\\n'.join(rules))
                    f.write('\\n')  # 确保文件以换行符结尾

                print(f"  💾 Saved to {output_file}")
            except Exception as e:
                print(f"  ❌ Error writing to {output_file}: {e}")
        else:
            print(f"  ⚠️  No valid rules for {category}")

if __name__ == '__main__':
    main()
    print("\\n✅ All categories processed!")
'''

# 写入文件
file_path = 'scripts/merge_rules.py'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"File created: {file_path}")
