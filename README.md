# RPA → AI Kit 🤖🔧

开放、零依赖的工具集，把**影刀 / UiBot / 通用 RPA 流程**桥接到现代 AI 工作流。
作者是一线 RPA 开发（影刀 + UiBot，带项目 PM），工具都来自真实交付里踩过的坑。

> 配套文章（掘金，待发布）：
> 1. `rpa2mcp` — 把 RPA 动作封装成 MCP server，让 Claude/任意 Agent 直接调用你的自动化。
> 2. 零依赖 UiBot Excel — 不装 Office、不装第三方库，纯标准库读写 xlsx。
> 3. `rpa2test` — 用录制/回放把外部系统调用变成可测试 mock。

## What's inside

| Tool | Path | What it does |
|------|------|--------------|
| **dryrun_recorder** | `tools/dryrun_recorder.py` | 录制真实 RPA/外系统调用，回放成 mock。CI 里跑不了真自动化也能测试下游逻辑。零依赖。 |

## Install

```bash
git clone https://github.com/Zhiyilang/rpa-to-ai-kit.git
python rpa-to-ai-kit/tools/dryrun_recorder.py   # runs the self-test
```

## Why this exists

Claude-builders 之类的赏金板走 Stripe，大陆个人收不到钱。所以这个仓库做成**自己拥有、可打赏**的开放资产——
免费使用，觉得有用就请作者喝杯咖啡（PayPal）。省下的排错时间，比一杯咖啡贵多了。☕

## Support

如果这套工具帮你少踩坑、多交付，欢迎 PayPal 打赏，支持更多免费工具。

👉 **仓库主人注册好 PayPal 中国个人卖家账户后，把 [`.github/FUNDING.yml`](.github/FUNDING.yml) 里的链接换成自己的 PayPal.me ID 即可收款。**

## License

MIT — 随便用，保留声明即可。

---

## 💝 赞助 / 打赏

如果这个项目对你有帮助，欢迎通过 **爱发电** 请我喝杯咖啡 ☕  
👉 https://afdian.com/a/Zhiyilang

> GitHub Sponsors 在中国大陆暂不支持个人账号，赞助统一走爱发电。

---
## 📚 我的实战课程
**《影刀RPA到AI Agent工程师：大专生的实战转型笔记》** —— 5 课可直接抄的作业（含可复制代码模板 + 真实接单复盘）。
在 **小报童 / 小红书** 搜索「支一郎」即可购买；完整大纲见 [GitHub Pages](https://Zhiyilang.github.io/#course)。
