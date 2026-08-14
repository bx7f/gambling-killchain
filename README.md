<div align="center">

# Gambling Killchain

**面向博彩平台的证据驱动安全审计 Skill**

[![Codex](https://img.shields.io/badge/Codex-compatible-111827)](https://github.com/openai/codex)
[![Claude Code](https://img.shields.io/badge/Claude_Code-compatible-D97757)](https://code.claude.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)](https://www.python.org/)

</div>

从落地分发、移动客户端和动态配置出发，连接会员/代理业务、游戏聚合、钱包支付、对象存储与软件家族证据。核心是判断组件、角色、对象和状态之间的真实关系，而非堆叠扫描脚本。

## 审计范围

| 领域 | 重点 |
|---|---|
| 落地与分发 | 跳转链、轮换域名、下载通道、签名与 Provisioning |
| 移动客户端 | APK、IPA、Flutter、RN、Hermes、WebView、Native 模块 |
| 动态配置 | Bootstrap、热更新、API/CDN 调度、请求信任与接口差集 |
| 角色与业务 | 访客、试玩、会员、代理、后台角色及对象/租户/状态边界 |
| 资金链路 | 钱包、充值、提现、代付、回调、账本与对账状态机 |
| 存储与家族 | Bucket/CDN、客户端仓库、白标代码、基础设施和家族关联 |
| 证据与报告 | 原始证据、负面结果、能力分层、影响校准与可执行结论 |

## 设计原则

- **业务语义优先**：成功响应只有放进角色、对象和状态关系中才有意义。
- **客户端是证据源**：沿调用链确认配置、密钥、路由和运行时用途。
- **最小判别测试**：每次只改变一个身份、对象、状态、参数或路由变量。
- **结论诚实分层**：区分线索、观察、已复现能力、有效 Finding 和家族/主体判断。
- **脚本保持克制**：仅保留一个确定性的证据归档与校验工具。

## 安装

### Codex

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/bx7f/gambling-killchain.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/gambling-killchain"
```

调用：

```text
$gambling-killchain
```

### Claude Code

```bash
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/bx7f/gambling-killchain.git \
  "$HOME/.claude/skills/gambling-killchain"
```

调用：

```text
/gambling-killchain
```

也可作为本地 Plugin 加载：

```bash
claude --plugin-dir ./gambling-killchain
```

## 使用示例

```text
分析这批 APK/IPA，确认当前构建使用的动态配置、API、支付与存储关系。

根据 HAR 和客户端调用点，判断试玩、会员、代理与后台接口的角色边界。

把现有客户端、订单、存储和签名证据整理为可复核、可执行的审计结论。
```

## 证据工具

```bash
python3 scripts/evidence.py init \
  --case-id CASE_ID --root evidence --question "QUESTION"

python3 scripts/evidence.py add \
  --case-dir evidence/CASE_ID --file PATH \
  --test-id TEST_ID --source SOURCE --notes "DIRECT OBSERVATION"

python3 scripts/evidence.py verify \
  --case-dir evidence/CASE_ID
```

工具只负责初始化案例、按内容哈希归档材料、维护 JSONL 清单和验证完整性。具体判断由 `SKILL.md` 与按需加载的 `references/` 提供。

## 目录

```text
SKILL.md                  核心方法与领域路由
references/               七个博彩审计知识域
assets/templates/         证据索引与报告模板
scripts/evidence.py       唯一证据工具
agents/openai.yaml        Codex 元数据
.claude-plugin/plugin.json  Claude Code Plugin 元数据
tests/                    工具与兼容性测试
```

## 免责声明

本项目用于安全研究、工程评估、证据管理与风险验证。使用者应自行确认适用的法律、合同、平台规则和评估范围，并对操作过程、数据处理及使用结果承担责任。

项目按现状提供。因使用本项目产生的服务中断、数据损失、合规争议或第三方索赔，由使用者结合实际场景承担相应责任。文中涉及的第三方产品、平台和商标归各自权利人所有，相关引用仅用于技术说明，不代表关联、认可或背书。
