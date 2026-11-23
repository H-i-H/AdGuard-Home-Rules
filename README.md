<div align="center">

# AdGuard-Home-Rules

**为 AdGuard Home 打造的自动化过滤规则集**

广告拦截 · 恶意网站拦截 · 成人内容拦截 —— 分类订阅，白名单兜底

![更新](https://img.shields.io/badge/更新-每日%2006%3A00%20UTC%2B8-2ea44f)
![平台](https://img.shields.io/badge/平台-AdGuard%20Home-blue)
![更新方式](https://img.shields.io/badge/更新方式-GitHub%20Actions-black)
![设备](https://img.shields.io/badge/设备要求-中高配-orange)
![状态](https://img.shields.io/badge/状态-测试版-red)

</div>

> [!IMPORTANT]
> 已更新订阅方式。规则体量巨大，**低配设备不推荐直接使用**。
> 建议 Fork 本仓库，按需精简上游规则后自行构建。

> [!NOTE]
> 本仓库由 AI 编写，仅用于测试。如有侵权或违规内容，请联系作者删除。

---

## 📑 目录

<details><summary>展开查看</summary>

- [特性](#-特性)
- [使用方法](#-使用方法)
- [目录结构](#-目录结构)
- [规则精简说明](#-规则精简说明)
- [误杀排查与白名单](#-误杀排查与白名单)
- [鸣谢](#-鸣谢)
- [免责声明](#-免责声明)

</details>

---

## ✨ 特性

| 特性 | 说明 |
| --- | --- |
| 🕘 自动化更新 | 每日 06:00（UTC+8）由 GitHub Actions 自动拉取上游并合并发布 |
| 🗂️ 分类管理 | 广告 / 恶意网站 / 成人内容独立订阅，可按需自由组合 |
| ✅ 白名单机制 | 自维护白名单持续更新，每日自动从最终订阅中扣除，降低误杀 |
| ✂️ 精简上游 | 只保留高质量、低误杀的核心规则源，误杀源已注释停用 |
| 🌐 国内加速 | 提供 CDN 加速订阅地址，国内拉取更稳定 |

---

## 🚀 使用方法

1. 打开 **AdGuard Home 管理面板**
2. 进入 **过滤器 → DNS 黑名单**（白名单同理）
3. 添加下方订阅地址（**最终订阅地址与单项订阅地址二选一**）
4. 等待规则拉取完成，可点击「检查更新」立即生效

### 方式一：最终订阅（推荐）

**完整版**（广告拦截 + 恶意内容拦截 + 成人内容拦截 − 白名单）：

```
https://github.com/H-i-H/AdGuard-Home-Rules/releases/download/latest/combined-rules.txt
```

**国内加速版**：

```
https://cdn.akaere.online/https://github.com/H-i-H/AdGuard-Home-Rules/releases/download/latest/combined-rules.txt
```

### 方式二：单项订阅

**广告内容拦截**

```
https://github.com/H-i-H/AdGuard-Home-Rules/releases/download/latest/ads-blacklist.txt
```

**恶意内容拦截**

```
https://github.com/H-i-H/AdGuard-Home-Rules/releases/download/latest/malware-blacklist.txt
```

**成人内容拦截**

```
https://github.com/H-i-H/AdGuard-Home-Rules/releases/download/latest/adult-blacklist.txt
```

**自维护白名单**（持续更新中，已自动合入最终订阅，也可单独添加）：

```
https://raw.githubusercontent.com/H-i-H/AdGuard-Home-Rules/main/Release/combined-whitelist.txt
```

---

## 📁 目录结构

<details><summary>展开查看</summary>

```
AdGuard-Home-Rules/
├── .github/workflows/
│   └── auto-update.yml            # 自动更新规则主流程
├── Release/
│   ├── combined-whitelist.txt     # 自维护白名单，如发现误杀可直接补充至此
│   ├── Supplement-rules.txt       # 自维护黑名单，如发现新增可直接补充至此
│   └── special-rules.txt          # 浏览器插件专用规则集
├── scripts/                       # 核心处理脚本
│   ├── fetch_upstream.py          # 上游规则获取
│   ├── merge_rules.py             # 规则合并处理
│   ├── whitelist_processor.py     # 白名单处理器
│   └── combine_final.py           # 最终合并器
└── requirements.txt               # Python 依赖列表
```

</details>

---

## ✂️ 规则精简说明

为降低误杀（部分应用无法打开）与规则体积，上游规则源已做精简。被停用的源均以注释形式保留在本文档末尾，取消注释即可恢复。

| 处理方式 | 涉及规则源 | 原因 |
| --- | --- | --- |
| ✅ 保留 | anti-AD、AdGuard SDNS、GOODBYEADS、oisd small、HaGeZi multi、malware ×2、成人 ×2 | 质量高、误杀少、中英文覆盖均衡 |
| ➡️ 移出 DNS | EasyList、EasyList China、EasyPrivacy、ADgk、AWAvenue | 浏览器专用规则，已挪至 `special-rules.txt` |
| ⏸️ 注释停用 | BlueSkyXN all.txt、oisd big、HaGeZi pro 及 11 条重复/激进源 | 巨型合集、档位过激、高度重叠，误杀主因 |
| 🔧 专项可选 | SmartTV、jiekouAD、AdGuard-fanqie | 仅特定设备/场景需要，默认停用 |

> [!TIP]
> 规则越多，误杀概率越高。建议按需订阅单项规则；恢复任何源之前，先确认确实有覆盖缺口。

---

## 🔧 误杀排查与白名单

部分应用打不开？按以下流程定位并修复：

1. **复现并抓取**：打开出问题的应用，立刻到 AdGuard Home **查询日志**，按客户端 / 时间过滤，找出被拦截（Blocked）的域名；
2. **验证**：用 `nslookup 域名` 确认是否被解析为 `0.0.0.0`；
3. **放行**：在 DNS 白名单中添加放行规则（或提交到 `Release/combined-whitelist.txt`）：

   ```
   @@||example.com^
   ```

4. **注意 CNAME 链路**：若被拦域名是 CNAME 跳转到第三方域名，请把最终目标域名一并加入白名单；
5. 反复出现的误杀欢迎提交 Issue / PR，次日构建自动生效。

常见易被误杀的域名类别（可预先加白）：消息推送 SDK（个推 / 极光 / 友盟等）、登录分享 SDK、支付与验证码、地图 API、崩溃上报、App 自更新与 CDN。

---

## 🙏 鸣谢

> 上游规则版权归原作者所有，如有侵权，请联系我删除：**QQ：1753582514**

**📌 广告（ADS）— 当前生效**

| 规则源 | 地址 |
| --- | --- |
| anti-AD | https://anti-ad.net/easylist.txt |
| AdGuard SDNS Filter | https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt |
| GOODBYEADS | https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/dns.txt |
| oisd small | https://small.oisd.nl |
| HaGeZi multi | https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt |

**📌 恶意内容（Malware）— 当前生效**

| 规则源 | 地址 |
| --- | --- |
| urlhaus-filter | https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-agh-online.txt |
| phishing-filter | https://malware-filter.gitlab.io/malware-filter/phishing-filter-agh.txt |

**📌 成人内容（Adult）— 当前生效**

| 规则源 | 地址 |
| --- | --- |
| StevenBlack/hosts (porn) | https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts |
| oisd nsfw | https://nsfw.oisd.nl |

<!-- ============================================================
以下为已注释停用的上游源，恢复 = 删除对应的 <!-- --> 包裹即可。
============================================================ -->

<!-- ---------- 移出 DNS：浏览器插件专用，请加入 special-rules.txt ----------
📌 ADS (browser-only)
- EasyList               https://easylist-downloads.adblockplus.org/easylist.txt
- EasyList China         https://easylist-downloads.adblockplus.org/easylistchina.txt
- EasyPrivacy            https://easylist-downloads.adblockplus.org/easyprivacy.txt
- ADgk                   https://cdn.jsdelivr.net/gh/banbendalao/ADgk@master/ADgk.txt
- AWAvenue-Ads-Rule      https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt
-->

<!-- ---------- 注释停用：巨型合集 / 档位过激（误杀主因） ----------
- BlueSkyXN all.txt      https://raw.githubusercontent.com/BlueSkyXN/AdGuardHomeRules/master/all.txt
- oisd big               https://big.oisd.nl                （已降档替换为 small）
- HaGeZi pro             https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt （已降档替换为 multi）
-->

<!-- ---------- 注释停用：与核心源高度重复 ----------
- Cats-Team/AdRules      https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt
- StevenBlack/hosts      https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
- AdAway                 https://adaway.org/hosts.txt
- someonewhocares        https://someonewhocares.org/hosts/zero/hosts
- DeveloperDan           https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt
- ppfeufer               https://raw.githubusercontent.com/ppfeufer/adguard-filter-list/refs/heads/master/blocklist
- AdguardFilters Mobile  https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt
- blocklistproject ads   https://raw.githubusercontent.com/blocklistproject/Lists/main/ads.txt
- kl0711 Ad-rules        https://raw.githubusercontent.com/kl0711/adRlues/refs/heads/main/Ad-rules.txt
- lingeringsound         https://raw.githubusercontent.com/lingeringsound/adblock_auto/refs/heads/main/Rules/adblock_auto.txt
- KiryChan KR_DNS_Filter https://raw.githubusercontent.com/KiryChanOfficial/AdFilterForAdGuard/refs/heads/main/KR_DNS_Filter.txt
-->

<!-- ---------- 专项可选：特定设备/场景才启用 ----------
- SmartTV                https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt
- jiekouAD               https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt
- AdGuard-fanqie         https://raw.githubusercontent.com/kl0711/adRlues/refs/heads/main/AdGuard-fanqie.txt
- fuck youtube           https://raw.githubusercontent.com/chinanjh/hosts/refs/heads/master/fuck%20youtube.txt
-->

---

## ⚖️ 免责声明

- 本仓库仅用于**测试与学习**，不作任何商业用途承诺；
- 所有规则来自公开上游项目，版权归原作者，侵权即删（QQ：**1753582514**）；
- 因使用本规则造成的任何直接或间接损失，作者不承担责任。
