# AdGuard-Home-Rules
这是一个由Ai编写的为AdGuard Home设计的过滤规则仓库，仅用于测试，如有违规，请联系作者删除，该仓库具有以下特点：

- **自动化更新**：每日06:00⏰ UTC+8自动更新规则
- **分类管理**：广告、恶意网站、成人内容分门别类
- **白名单机制**：每个类别都有白名单，减少误拦截
- **轻量精简**：基于高质量规则源，避免臃肿

**使用方法**
#### 直接使用：AdGuard Home 管理面板 → 过滤器 → DNS 黑名单/白名单中添加规则订阅（最终订阅地址和单项订阅地址二选一，）

##### 最终订阅地址（广告内容拦截+恶意内容拦截+成人内容拦截-白名单）→
```
https://raw.githubusercontent.com/H-i-H/AdGuard-Home-Rules/main/Release/combined-rules.txt
```

##### 单项订阅地址 →
```
广告内容拦截：
https://raw.githubusercontent.com/H-i-H/AdGuard-Home-Rules/main/filters/ads-blacklist.txt

恶意内容拦截：
https://raw.githubusercontent.com/H-i-H/AdGuard-Home-Rules/main/filters/malware-blacklist.txt

成人内容拦截：
https://raw.githubusercontent.com/H-i-H/AdGuard-Home-Rules/main/filters/adult-blacklist.txt

自维护白名单：
https://raw.githubusercontent.com/H-i-H/AdGuard-Home-Rules/main/Release/combined-whitelist.txt
```

#### 文件目录说明
```
AdGuard-Home-Rules/
├── .github/workflows/          # GitHub Actions 工作流配置
│   └── auto-update.yml          # 自动更新规则主流程
├── Release/
│   ├── combined-whitelist      #白名单规则集，如发现新增的，可直接添加在此文件
│   └── combined-rules.txt       # 最终合并黑名单规则集（添加此黑名单即可）
│   └── special-rules.txt       # 补充黑名单规则集（浏览器插件专用）
├── filters/                      # 生成的过滤规则文件
│   ├── ads-blacklist.txt         # 广告黑名单
│   ├── malware-blacklist.txt    # 恶意软件黑名单
│   ├── adult-blacklist.txt       # 成人内容黑名单
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
上游规则（感谢以下上游规则，如有侵权，请联系我删除：QQ：1753582514）

# 黑名单
📌 ADS
- https://anti-ad.net/easylist.txt
- https://raw.githubusercontent.com/BlueSkyXN/AdGuardHomeRules/master/all.txt
- https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt
- https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/dns.txt
- https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt
- https://raw.githubusercontent.com/ppfeufer/adguard-filter-list/refs/heads/master/blocklist
- https://raw.githubusercontent.com/KiryChanOfficial/AdFilterForAdGuard/refs/heads/main/KR_DNS_Filter.txt
- https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt
- https://cdn.jsdelivr.net/gh/banbendalao/ADgk@master/ADgk.txt
- https://raw.githubusercontent.com/kl0711/adRlues/refs/heads/main/Ad-rules.txt
- https://raw.githubusercontent.com/kl0711/adRlues/refs/heads/main/AdGuard-fanqie.txt
- https://raw.githubusercontent.com/lingeringsound/adblock_auto/refs/heads/main/Rules/adblock_auto.txt
- https://raw.githubusercontent.com/chinanjh/hosts/refs/heads/master/fuck%20youtube.txt
- https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt
- https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt
- https://big.oisd.nl
- https://badmojr.github.io/1Hosts/Lite/hosts.txt
- https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt
- https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
- https://adaway.org/hosts.txt
- https://someonewhocares.org/hosts/zero/hosts
- https://easylist-downloads.adblockplus.org/easylist.txt
- https://easylist-downloads.adblockplus.org/easylistchina.txt
- https://easylist-downloads.adblockplus.org/easyprivacy.txt
- https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt
- https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt
- https://raw.githubusercontent.com/blocklistproject/Lists/main/ads.txt


📌 malware
- https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-agh-online.txt
- https://malware-filter.gitlab.io/malware-filter/phishing-filter-agh.txt

📌 adult
- https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts
- https://nsfw.oisd.nl
```
