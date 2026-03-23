# 提交你的作品

感谢参赛！请按以下步骤将你的 notebook 作品提交到案例库。

[English Version](./CONTRIBUTING.md)

## 前提条件

- 拥有 GitHub 账号
- 作品已在 **aup-learning-cloud Basic GPU Environment** 环境中测试可正常运行

## 提交步骤

### 1. Fork 本仓库

点击页面右上角的 **Fork** 按钮，创建你的个人副本。

### 2. 创建你的作品文件夹

将 `template/` 目录复制到对应的比赛文件夹下：

```
cases/
└── 2026-03-njupt-winter-battle/    ← 你的比赛文件夹
    └── 你的团队名-项目简称/         ← 新建文件夹（从 template/ 复制）
        ├── README.md               ← 英文文档（必须提交）
        ├── README_ZH.md            ← 中文文档（必须提交）
        ├── requirements.txt
        ├── main.ipynb              ← 英文 notebook（必须提交）
        └── main_zh.ipynb           ← 中文 notebook（必须提交）
```

**文件夹命名规则：**
- 格式：`团队名-项目简称`（如 `teamalpha-llmchat`）
- 只用小写字母、数字、连字符，不用空格或特殊字符
- 简洁有描述性

> **关于获奖前缀**：请勿自行添加 `01-gold-`、`02-silver-`、`03-bronze-` 等前缀。
> 比赛结果公布后，由主办方统一重命名。

### 3. 填写 README.md 和 README_ZH.md

两份文档均为必须提交：

- **`README.md`** — 英文版本。使用 `template/README.md` 中的模板，**所有标注 `<!-- required -->` 的字段必须填写**，请用**英文**填写。
- **`README_ZH.md`** — 中文版本。使用 `template/README_ZH.md` 中的模板，**所有标注 `<!-- 必填 -->` 的字段必须填写**，请用**中文**填写。

### 4. 填写依赖列表

编辑 `requirements.txt`，列出你的 notebook 需要的额外 pip 包。

**不需要填写**：`torch`、`torchvision`、`rocm` 相关包（已在 Basic GPU Environment 中预装）。

若无额外依赖，保留空文件即可（文件必须存在）。

### 5. 在 aup-learning-cloud 中测试

提交前请完成以下验证（**两个 notebook 都要测试**）：

1. 打开 aup-learning-cloud → 选择 **Basic GPU Environment**
2. 从头到尾运行 `main.ipynb`（英文版）的所有 Cell，确认无报错
3. 从头到尾运行 `main_zh.ipynb`（中文版）的所有 Cell，确认无报错

### 6. 提交 Pull Request

1. 将修改 commit 并 push 到你的 fork
2. 向本仓库发起 Pull Request
3. GitHub 会显示提交 checklist —— **逐项勾选后再提交**
4. 等待主办方 Review 并合并

## 文件大小限制

提交内容总大小请控制在 **100MB 以内**。

大型数据集或模型权重请使用外链（如 Hugging Face、Google Drive），并在 README 中注明。

## 获奖标记说明

比赛结果公布后，主办方将对获奖作品文件夹重命名：

| 奖项 | 前缀 | 示例 |
|------|------|------|
| 一等奖（金奖） | `01-gold-` | `01-gold-teamalpha-llmchat` |
| 二等奖（银奖） | `02-silver-` | `02-silver-teambeta-cvdetect` |
| 三等奖（铜奖） | `03-bronze-` | `03-bronze-teamgamma-robot` |
| 无奖项 | _(无前缀)_ | `teamdelta-nlpchat` |

提交时无需在文件夹名中包含获奖前缀，主办方在比赛结束后统一处理。

## 有问题？

在 GitHub 上提 Issue，或直接联系比赛主办方。
