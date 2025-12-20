
import os
from datetime import datetime

def combine_all_rules():
    """合并所有规则到最终文件"""
    final_rules = []
    categories = ['ads', 'malware', 'adult']

    # 配置参数
    output_dir = 'filters'
    output_file = os.path.join(output_dir, 'combined-rules.txt')

    print("\n🔄 Combining all rules...")

    # 检查输出目录
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"  📁 Created directory: {output_dir}")
        except OSError as e:
            print(f"  ❌ Cannot create directory {output_dir}: {e}")
            return False

    total_original = 0

    for cat in categories:
        filename = os.path.join('filters', f'{cat}-blacklist.txt')
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    rules = [line.strip() for line in content.split('\n')
                            if line.strip() and not line.startswith('!')]
                    final_rules.extend(rules)
                    total_original += len(rules)
                    print(f"  📥 {cat}: {len(rules)} rules")
            except Exception as e:
                print(f"  ❌ Error reading {filename}: {e}")
                return False
        else:
            print(f"  ⚠️  {cat}: file not found")

    # 最终去重（保持顺序）
    unique_rules = list(dict.fromkeys(final_rules))
    filtered_count = total_original - len(unique_rules)

    # 生成更友好的日期格式
    generation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 写入最终文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('! Adguard Home Private Rules Bundle\n')
            f.write('! =================================\n')
            f.write(f'! Generated: {generation_time}\n')
            f.write(f'! Total categories: {len(categories)}\n')
            f.write(f'! Total rules (before dedup): {total_original}\n')
            f.write(f'! Total unique rules: {len(unique_rules)}\n')
            f.write(f'! Duplicates removed: {filtered_count}\n')
            f.write('! \n')
            f.write('! Coverage: Ads + Malware + Adult\n')
            f.write('! Personal whitelist applied\n')
            f.write('! Auto-update: Daily at 06:00 UTC\n')
            f.write('! =================================\n\n')
            f.write('\n'.join(unique_rules))
            if unique_rules:  # 确保文件末尾有换行
                f.write('\n')

        print(f"  💾 Final bundle: {len(unique_rules)} rules")
        print(f"  📄 Saved to: {output_file}")
        return True

    except Exception as e:
        print(f"  ❌ Error writing to {output_file}: {e}")
        return False

if __name__ == '__main__':
    success = combine_all_rules()
    if success:
        print("\n✅ Bundle creation complete!")
    else:
        print("\n❌ Bundle creation failed!")
