from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List, Tuple, Optional
import re

def clean_and_deduplicate_rules(lines: List[str]) -> List[str]:
    """深度清洗与去重规则"""
    seen = set()
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        
        # 1. 跳过空行
        if not line:
            continue
            
        # 2. 保留注释和元数据
        if line.startswith('!') or line.startswith('#') or line.startswith('['):
            cleaned_lines.append(line)
            continue
            
        # 3. 规则去重（统一转小写，防止大小写导致的重复，AdGuard 域名部分不区分大小写）
        rule_key = line.lower()
        
        if rule_key not in seen:
            seen.add(rule_key)
            cleaned_lines.append(line)
            
    return cleaned_lines

def combine_all_rules() -> bool:
    """合并所有规则到最终文件"""
    # 配置参数
    output_dir = Path('Release')
    output_file = output_dir / 'combined-rules.txt'
    categories = ['ads', 'malware', 'adult']
    print("\n🔄 Combining all rules...")

    # 验证输入目录
    filters_dir = Path('filters')
    if not filters_dir.exists():
        print(f"  ❌ Filters directory not found: {filters_dir}")
        return False

    # 检查输入文件
    input_files = []
    for cat in categories:
        filepath = filters_dir / f'{cat}-blacklist.txt'
        if filepath.exists():
            input_files.append((cat, filepath))
        else:
            print(f"  ⚠️ {cat}: file not found")

    if not input_files:
        print("  ❌ No input files found to combine")
        return False

    # 收集所有规则
    final_rules: List[str] = []
    stats = {}

    for cat, filepath in input_files:
        try:
            rules = []
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('!'):
                        rules.append(line)

            count = len(rules)
            stats[cat] = count
            final_rules.extend(rules)
            print(f"  📥 {cat}: {count} rules")

        except Exception as e:
            print(f"  ❌ Error reading {filepath}: {e}")
            return False

    # 【关键修复】：统计原始有效规则数（严格排除注释行，防止统计错乱）
    total_original = len([r for r in final_rules if not r.startswith('!') and not r.startswith('#')])

    # 使用深度清洗与去重函数
    unique_rules = clean_and_deduplicate_rules(final_rules)
    
    # 统计去重后的有效规则数
    unique_rules_count = len([r for r in unique_rules if not r.startswith('!') and not r.startswith('#')])
    duplicates_removed = total_original - unique_rules_count

    if not unique_rules:
        print("  ⚠️ Warning: No rules after deduplication!")
        return False

    # 准备输出
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成头部信息
    generation_time = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
    header = [
        "! Adguard Home Private Rules Bundle",
        "! =================================",
        f"! Generated: {generation_time}",
        f"! Total categories: {len(categories)}",
        f"! Total rules (before dedup): {total_original}",
        f"! Total unique rules: {unique_rules_count}",
        f"! Duplicates removed: {duplicates_removed}",
        "!",
        "! Coverage: Ads + Malware + Adult",
        "! Personal whitelist applied",
        "! Auto-update: Daily at 06:00 UTC+8",
        "! =================================",
        ""  # 空行分隔
    ]

    # 写入文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(header))
            f.write('\n'.join(unique_rules))
            if unique_rules:
                f.write('\n')  # 确保末尾换行

        print(f"\n  💾 Final bundle saved to: {output_file}")
        return True

    except Exception as e:
        print(f"  ❌ Error writing to {output_file}: {e}")
        return False

def validate_combined_file() -> bool:
    """验证生成的文件"""
    output_file = Path('Release') / 'combined-rules.txt'
    if not output_file.exists():
        print("  ❌ Output file not found")
        return False

    size = output_file.stat().st_size
    if size == 0:
        print("  ❌ Output file is empty")
        return False

    try:
        content = output_file.read_text(encoding='utf-8')
        lines = [l for l in content.split('\n') if l.strip() and not l.startswith('!')]

        if not lines:
            print("  ❌ No rules in output file")
            return False

        print(f"  ✅ File validated: {size} bytes, {len(lines)} rules")
        return True

    except Exception as e:
        print(f"  ❌ Validation failed: {e}")
        return False

if __name__ == '__main__':
    success = combine_all_rules()
    if success:
        if validate_combined_file():
            print("\n✅ Bundle creation and validation complete!")
        else:
            print("\n⚠️ Bundle created but validation failed!")
            exit(1)
    else:
        print("\n❌ Bundle creation failed!")
        exit(1)
