
import os

# 个人白名单配置
PERSONAL_WHITELIST = {
    # 常用合法网站
    'github.com',
    'google.com',
    'microsoft.com',
    'apple.com',
    'amazon.com',
    'youtube.com',
    'wikipedia.org',
    # 开发相关
    'stackoverflow.com',
    'npmjs.com',
    'pypi.org',
    # 社交媒体
    'twitter.com',
    'linkedin.com',
    'reddit.com',
    # 新闻媒体
    'reuters.com',
    'bbc.com',
    'nytimes.com',
    # 银行金融
    'paypal.com',
    'visa.com',
    'mastercard.com'
}

def load_custom_whitelist():
    """加载自定义白名单文件"""
    whitelist_file = 'whitelist.txt,ad-whitelist.txt,adult-whitelist.txt,malware-whitelist.txt'
    custom_whitelist = set()
    
    if os.path.exists(whitelist_file):
        try:
            with open(whitelist_file, 'r', encoding='utf-8') as f:
                for line in f:
                    domain = line.strip()
                    if domain and not domain.startswith('#'):
                        custom_whitelist.add(domain)
            print(f"  📋 Loaded {len(custom_whitelist)} domains from custom whitelist")
        except Exception as e:
            print(f"  ❌ Error loading {whitelist_file}: {e}")
    else:
        print("  ⚠️  No custom whitelist file found")
        
    return custom_whitelist

def apply_whitelist_to_category(category):
    """对特定分类应用白名单"""
    input_file = os.path.join('filters', f'{category}-blacklist.txt')
    output_file = os.path.join('filters', f'{category}-blacklist-whitelisted.txt')
    
    if not os.path.exists(input_file):
        print(f"  ⚠️  Input file not found: {input_file}")
        return False
        
    try:
        # 读取黑名单规则
        with open(input_file, 'r', encoding='utf-8') as f:
            rules = [line.strip() for line in f if line.strip()]
            
        print(f"  📥 {category}: {len(rules)} rules loaded")
        
        # 应用白名单过滤
        filtered_rules = []
        removed_count = 0
        
        for rule in rules:
            # 提取域名
            if rule.startswith('||') and rule.endswith('^'):
                domain = rule[2:-1]
                # 检查是否在白名单中
                if domain in PERSONAL_WHITELIST:
                    removed_count += 1
                    continue
                # 检查子域名是否在白名单中
                is_whitelisted = False
                for whitelist_domain in PERSONAL_WHITELIST:
                    if domain.endswith('.' + whitelist_domain) or domain == whitelist_domain:
                        is_whitelisted = True
                        break
                if not is_whitelisted:
                    filtered_rules.append(rule)
                else:
                    removed_count += 1
            else:
                filtered_rules.append(rule)
                
        # 保存处理后的规则
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(filtered_rules))
            if filtered_rules:  # 确保文件末尾有换行
                f.write('\n')
                
        print(f"  ✅ {category}: {len(filtered_rules)} rules after whitelist ({removed_count} removed)")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {category}: {e}")
        return False

def process_all_categories():
    """处理所有分类的白名单"""
    print("🔄 Applying whitelist processing...")
    
    # 加载自定义白名单
    custom_whitelist = load_custom_whitelist()
    PERSONAL_WHITELIST.update(custom_whitelist)
    print(f"  🛡️  Total whitelist domains: {len(PERSONAL_WHITELIST)}")
    
    categories = ['ads', 'malware', 'adult']
    success_count = 0
    
    for category in categories:
        print(f"\n📂 Processing category: {category}")
        if apply_whitelist_to_category(category):
            # 替换原文件
            input_file = os.path.join('filters', f'{category}-blacklist.txt')
            output_file = os.path.join('filters', f'{category}-blacklist-whitelisted.txt')
            if os.path.exists(output_file):
                os.replace(output_file, input_file)
                print(f"  🔄 Updated {input_file}")
            success_count += 1
            
    print(f"\n✅ Whitelist processing complete: {success_count}/{len(categories)} categories processed")
    return success_count > 0

if __name__ == '__main__':
    process_all_categories()
