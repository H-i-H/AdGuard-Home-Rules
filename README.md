<div align="center">

# AdGuard-Home-Rules

<small>为 AdGuard Home 打造的自动化过滤规则集 · 广告 / 恶意网站 / 成人内容分类拦截，白名单兜底</small>

![更新时间](https://img.shields.io/badge/更新时间-每日%2006%3A00-2ea44f?style=flat-square)
![运行平台](https://img.shields.io/badge/运行平台-AdGuard%20Home-24292f?style=flat-square)
![更新方式](https://img.shields.io/badge/更新方式-GitHub%20Actions-1668a8?style=flat-square)
![设备要求](https://img.shields.io/badge/设备要求-中高配-b08800?style=flat-square)
![状态](https://img.shields.io/badge/状态-测试版-cb3837?style=flat-square)

<small><b>[特性](#-特性) · [使用方法](#-使用方法) · [目录结构](#-目录结构) · [规则精简](#-规则精简) · [误杀排查](#-误杀排查) · [鸣谢](#-鸣谢) · [免责声明](#-免责声明)</b></small>

</div>

> [!IMPORTANT]
> **已更新订阅方式** —— 规则体量巨大，低配设备不推荐使用。
>
> 建议 Fork 本仓库，按需精简上游规则后自行构建。
>
> 本仓库由 AI 编写，仅用于测试。如有侵权或违规，请联系作者删除（QQ：1753582514）。

---

## ✨ 特性

<table width="100%">
  <tr>
    <th align="left" width="22%"><small><b>特性</b></small></th>
    <th align="left"><small><b>说明</b></small></th>
  </tr>
  <tr>
    <td align="left"><small>🕘 自动更新</small></td>
    <td align="left"><small>每日 06:00（UTC+8）自动拉取上游并合并发布</small></td>
  </tr>
  <tr>
    <td align="left"><small>🗂️ 分类管理</small></td>
    <td align="left"><small>广告 / 恶意 / 成人独立订阅，按需自由组合</small></td>
  </tr>
  <tr>
    <td align="left"><small>✅ 白名单机制</small></td>
    <td align="left"><small>自维护白名单每日扣减，持续降低误杀</small></td>
  </tr>
  <tr>
    <td align="left"><small>✂️ 精简上游</small></td>
    <td align="left"><small>仅保留高质量、低误杀的核心规则源</small></td>
  </tr>
  <tr>
    <td align="left"><small>🌐 国内加速</small></td>
    <td align="left"><small>提供 CDN 加速订阅地址，拉取更稳定</small></td>
  </tr>
</table>

---

## 🚀 使用方法

<small>**面板路径**：过滤器 → DNS 黑名单（白名单同理）→ 添加订阅 → 检查更新　|　最终订阅与单项订阅<b>二选一</b></small>

<small>**完整版**（广告 + 恶意 + 成人 − 白名单）</small>

```
https://github.com/H-i-H/AdGuard-Home-Rules/releases/download/latest/combined-rules.txt
```

<small>**国内加速版**</small>

```
https://cdn.akaere.online/https://github.com/H-i-H/AdGuard-Home-Rules/releases/download/latest/combined-rules.txt
```

<details>
<summary><small><b>单项订阅地址（广告 / 恶意 / 成人 / 白名单）</b></small></summary>

<br>

<small>**广告内容拦截**</small>

```
https://github.com/H-i-H/AdGuard-Home-Rules/releases/download/latest/ads-blacklist.txt
```

<small>**恶意内容拦截**</small>

```
https://github.com/H-i-H/AdGuard-Home-Rules/releases/download/latest/malware-blacklist.txt
```

<small>**成人内容拦截**</small>

```
https://github.com/H-i-H/AdGuard-Home-Rules/releases/download/latest/adult-blacklist.txt
```

<small>**自维护白名单**（已自动合入最终订阅，也可单独添加）</small>

```
https://raw.githubusercontent.com/H-i-H/AdGuard-Home-Rules/main/Release/combined-whitelist.txt
```

</details>

---

## 📁 目录结构

<details>
<summary><small><b>展开查看</b></small></summary>

<br>

```
AdGuard-Home-Rules/
├── .github/workflows/
│   └── auto-update.yml            # 自动更新规则主流程
├── Release/
│   ├── combined-whitelist.txt     # 自维护白名单，发现误杀可补充至此
│   ├── Supplement-rules.txt       # 自维护黑名单，发现新增可补充至此
│   └── special-rules.txt          # 浏览器插件专用规则集
├── scripts/
│   ├── fetch_upstream.py          # 上游规则获取
│   ├── merge_rules.py             # 规则合并处理
│   ├── whitelist_processor.py     # 白名单处理器
│   └── combine_final.py           # 最终合并器
└── requirements.txt               # Python 依赖列表
```

</details>

---

## ✂️ 规则精简

<small>为降低误杀（部分应用无法打开）与规则体积，上游源已精简；被停用的源以注释保留在文末，取消注释即可恢复。</small>

<table width="100%">
  <tr>
    <th align="left" width="22%"><small><b>处理</b></small></th>
    <th align="left"><small><b>说明</b></small></th>
  </tr>
  <tr>
    <td align="left"><small>✅ 保留生效</small></td>
    <td align="left"><small>广告 5 · 恶意 2 · 成人 2，共 9 个核心源</small></td>
  </tr>
  <tr>
    <td align="left"><small>➡️ 移出 DNS</small></td>
    <td align="left"><small>浏览器规则 5 个 → 移入 special-rules.txt</small></td>
  </tr>
  <tr>
    <td align="left"><small>⏸️ 注释停用</small></td>
    <td align="left"><small>巨型 / 激进 / 重复源 15 个，详见文末注释</small></td>
  </tr>
  <tr>
    <td align="left"><small>🔧 专项可选</small></td>
    <td align="left"><small>SmartTV · jiekouAD · fanqie · fuck youtube</small></td>
  </tr>
</table>

---

## 🔧 误杀排查

<small>应用打不开时按此流程定位：</small>

1. <small>复现失败，查看 **查询日志**，按客户端 / 时间过滤出 blocked 域名</small>
2. <small>`nslookup 域名` 验证是否被解析为 `0.0.0.0`</small>
3. <small>白名单添加 `@@||域名^`，或提交至 `Release/combined-whitelist.txt`</small>
4. <small>若域名经 CNAME 跳转第三方，请把最终目标域名一并加白</small>
5. <small>高频误杀欢迎提交 Issue / PR，次日构建自动生效</small>

<small>**常见易误杀类别**：推送 SDK · 登录分享 · 支付验证码 · 地图 API · 崩溃上报 · 自更新与 CDN</small>

---

## 🙏 鸣谢

<small>上游规则版权归原作者，如有侵权请联系删除：<b>QQ：1753582514</b></small>

<small>**📌 广告（ADS）— 当前生效**</small>

```
https://anti-ad.net/easylist.txt
https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt
https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/dns.txt
https://small.oisd.nl
https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt
```

<small>**📌 恶意内容（Malware）— 当前生效**</small>

```
https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-agh-online.txt
https://malware-filter.gitlab.io/malware-filter/phishing-filter-agh.txt
```

<small>**📌 成人内容（Adult）— 当前生效**</small>

```
https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts
https://nsfw.oisd.nl
```

<!-- ============================================================
以下为已注释停用的上游源。恢复方法：删除对应区块首尾的注释标记即可。
============================================================ -->

<!-- 【移出 DNS：浏览器插件专用，请加入 special-rules.txt】
- EasyList               https://easylist-downloads.adblockplus.org/easylist.txt
- EasyList China         https://easylist-downloads.adblockplus.org/easylistchina.txt
- EasyPrivacy            https://easylist-downloads.adblockplus.org/easyprivacy.txt
- ADgk                   https://cdn.jsdelivr.net/gh/banbendalao/ADgk@master/ADgk.txt
- AWAvenue-Ads-Rule      https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt
==== -->

<!-- 【注释停用：巨型合集 / 档位过激，误杀主因】
- BlueSkyXN all.txt      https://raw.githubusercontent.com/BlueSkyXN/AdGuardHomeRules/master/all.txt
- oisd big               https://big.oisd.nl                 （已降档替换为 small）
- HaGeZi pro             https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt （已降档替换为 multi）
==== -->

<!-- 【注释停用：与核心源高度重复】
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
- 1Hosts Lite            https://badmojr.github.io/1Hosts/Lite/hosts.txt
==== -->

<!-- 【专项可选：特定设备 / 场景才启用】
- SmartTV                https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt
- jiekouAD               https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt
- AdGuard-fanqie         https://raw.githubusercontent.com/kl0711/adRlues/refs/heads/main/AdGuard-fanqie.txt
- fuck youtube           https://raw.githubusercontent.com/chinanjh/hosts/refs/heads/master/fuck%20youtube.txt
==== -->

---

## ⚖️ 免责声明

<small>仅用于测试与学习 · 规则版权归原作者，侵权即删 · 一切直接或间接损失与作者无关</small>
