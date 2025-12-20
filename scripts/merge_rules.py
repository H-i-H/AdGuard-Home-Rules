
import os
import re
from tldextract import extract as tld_extract

def is_valid_domain(domain):
    """检查是否为有效域名"""
    if not domain or '.' not in domain:
        return False
    # 简单的域名格式检查
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return re.match(pattern, domain) is not None

def process_hosts_file(filepath):
    """处理hosts文件格式"""
    rules = set()
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                # 跳过注释和空行
                if not line or line.startswith('#') or line.startswith('!'):
                    continue
                    
                # 提取域名部分
                parts = line.split()
                if len(parts) >= 2 and parts[0] in ('127.0.0.1', '0.0.0.0'):
                    domain = parts[1]
                    if is_valid_domain(domain):
                        rules.add(domain)
    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {e}")
    return rules

def process_adguard_file(filepath):
    """处理AdGuard规则文件"""
    rules = set()
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                # 跳过注释和空行
                if not line or line.startswith('!') or line.startswith('['):
                    continue
                    
                # 处理 ||example.com^ 格式
                if line.startswith('||') and line.endswith('^'):
                    domain = line[2:-1]
                    if is_valid_domain(domain):
                        rules.add(domain)
                        
                # 处理 ||example.com^$third-party 格式
                elif line.startswith('||') and '^$' in line:
                    domain = line[2:].split('^$')[0]
                    if is_valid_domain(domain):
                        rules.add(domain)
    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {e}")
    return rules

def merge_category_rules(category):
    """合并特定分类的规则"""
    print(f"  🔄 Merging {category} rules...")
    all_rules = set()
    source_dir = os.path.join('sources', category)
    
    if not os.path.exists(source_dir):
        print(f"  ⚠️  No sources for {category}")
        return False
        
    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)
        if not os.path.isfile(filepath):
            continue
            
        print(f"    📄 Processing: {filename}")
        
        # 根据文件内容判断类型
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000)  # 读取前1000个字符判断格式
                
            if '||' in content and ('^' in content or '$' in content):
                # AdGuard格式
                rules = process_adguard_file(filepath)
            else:
                # hosts格式
                rules = process_hosts_file(filepath)
                
            all_rules.update(rules)
            print(f"    ➕ Extracted {len(rules)} rules")
        except Exception as e:
            print(f"    ❌ Error reading {filename}: {e}")
            
    # 保存合并后的规则
    output_dir = 'filters'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{category}-blacklist.txt')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for rule in sorted(all_rules):
                f.write(f"||{rule}^\n")
        print(f"  💾 {category}: {len(all_rules)} unique rules saved")
        return True
    except Exception as e:
        print(f"  ❌ Error saving {output_file}: {e}")
        return False

def merge_all_categories():
    """合并所有分类规则"""
    print("🔄 Starting rule merging process...")
    categories = ['ads', 'malware', 'adult']
    success_count = 0
    
    for category in categories:
        if merge_category_rules(category):
            success_count += 1
            
    print(f"\n✅ Merging complete: {success_count}/{len(categories)} categories processed")
    return success_count > 0

if __name__ == '__main__':
    merge_all_categories()
