# AdGuard-Home-Rules
这是一个由Ai编写的为AdGuard Home设计的过滤规则仓库，仅用于测试，如有违规，请联系作者删除，该仓库具有以下特点：

- **自动化更新**：每日06:00⏰ UTC+8自动更新规则
- **分类管理**：广告、恶意网站、成人内容分门别类
- **白名单机制**：每个类别都有白名单，减少误拦截
- **轻量精简**：基于高质量规则源，避免臃肿

**使用方法**
#### 直接使用：在AdGuard Home中添加规则订阅
```
https://raw.githubusercontent.com/H-i-H/AdGuard-Home-Rules/refs/heads/main/filters/combined-rules.txt
```

#### 文件目录说明
```
AdGuard-Home-Rules/
├── .github/workflows/          # GitHub Actions 工作流配置
│   ├── auto-update.yml          # 自动更新规则主流程
├── filters/                      # 生成的过滤规则文件
│   ├── combined-rules.txt       # 最终合并规则集
│   ├── ad-blacklist.txt         # 广告黑名单
│   ├── malware-blacklist.txt    # 恶意软件黑名单
│   ├── adult-blacklist.txt       # 成人内容黑名单
│   ├── ad-whitelist.txt         # 广告白名单
│   ├── malware-whitelist.txt    # 恶意软件白名单
│   └── adult-whitelist.txt      # 成人内容白名单
├── scripts/                      # 核心处理脚本
│   ├── fetch_upstream.py        # 上游规则获取
│   ├── merge_rules.py            # 规则合并处理
│   ├── whitelist_processor.py    # 白名单处理器
│   └── combine_final.py         # 最终合并器
├── sources/                      # 上游规则源缓存
│   ├── malware/                  # 恶意软件规则源
│   ├── adult/                     # 成人内容规则源
│   └── ad/                         # 广告规则源
└── requirements.txt              # Python 依赖列表
```

#### 鸣谢 
```
上游规则
📌 ADS
- https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt
- https://easylist-downloads.adblockplus.org/easylist.txt
- https://easylist-downloads.adblockplus.org/easylistchina.txt
📌 malware
- https://malware-filter.pages.dev/urlhaus-filter-online.txt
- https://malware-filter.pages.dev/phishing-filter.txt
- https://ransomwaretracker.abuse.ch/downloads/RW_DOMBL.txt
📌 adult
- https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts
- https://easylist-downloads.adblockplus.org/easylist-cookie.txt
```
