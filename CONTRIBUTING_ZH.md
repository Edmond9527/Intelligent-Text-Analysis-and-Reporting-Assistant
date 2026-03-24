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

将 `template/` 目录复制到对应的比赛文件夹下。本仓库最终（获奖公布后）的完整目录结构如下：

```
cases/
└── 2026-03-njupt-winter-battle/         ← 活动文件夹
    ├── README.md                         ← 活动简介 + 获奖名单
    ├── 01-gold-teamalpha-llmchat/        ← 一等奖（主办方重命名）
    ├── 02-silver-teambeta-cvdetect/      ← 二等奖（主办方重命名）
    ├── 03-bronze-teamgamma-robot/        ← 三等奖（主办方重命名）
    └── teamdelta-nlpchat/                ← 普通提交（无前缀）
        ├── README.md                     ← 英文文档（必须提交）
        ├── README_ZH.md                  ← 中文文档（必须提交）
        ├── requirements.txt
        ├── main.ipynb                    ← 英文 notebook（必须提交）
        ├── main_zh.ipynb                 ← 中文 notebook（必须提交）
        └── assets/                       ← 截图、动图（可选）
```

**根据你的比赛结果命名文件夹：**

| 结果 | 文件夹命名格式 | 示例 |
|------|--------------|------|
| 一等奖（金奖） | `01-gold-团队名-项目简称` | `01-gold-teamalpha-llmchat` |
| 二等奖（银奖） | `02-silver-团队名-项目简称` | `02-silver-teambeta-cvdetect` |
| 三等奖（铜奖） | `03-bronze-团队名-项目简称` | `03-bronze-teamgamma-robot` |
| 未获奖 / 工作坊 | `团队名-项目简称` | `teamdelta-nlpchat` |

> **不是比赛提交？** 直接用无前缀的 `团队名-项目简称` 格式即可，和未获奖格式相同。

**命名规则：**
- 只用小写字母、数字、连字符，不用空格或特殊字符
- 简洁有描述性（如 `teamalpha-llmchat`、`smith-image-caption`）

### 3. 填写 README.md 和 README_ZH.md

两份文档均为必须提交：

- **`README.md`** — 英文版本。使用 `template/README.md` 中的模板，**所有标注 `<!-- required -->` 的字段必须填写**，请用**英文**填写。
- **`README_ZH.md`** — 中文版本。使用 `template/README_ZH.md` 中的模板，**所有标注 `<!-- 必填 -->` 的字段必须填写**，请用**中文**填写。

### 4. 添加截图、动图和演示视频（推荐）

视觉内容能让你的作品脱颖而出。建议在 `README.md` 和 `README_ZH.md` 中都加入。

**建议包含的内容：**

| 类型 | 推荐内容 |
|------|---------|
| 截图 | 界面截图、推理结果、图表 |
| GIF 动图 | 10–30 秒的功能演示 |
| 视频 | 外链（B站、YouTube），在 README 中附链接 |

**在 README 中引用媒体文件：**

```markdown
![demo](./assets/demo.gif)
![result](./assets/result.png)
```

所有媒体文件请放在项目目录下的 `assets/` 文件夹中。

**视频转 GIF 方法：**

若演示视频体积较大，建议截取关键片段转为 GIF：

```bash
# ffmpeg：从第 5 秒开始截取 20 秒，宽度缩放至 720px，15 帧/秒
ffmpeg -ss 00:00:05 -t 20 -i demo.mp4 \
  -vf "fps=15,scale=720:-1:flags=lanczos" \
  -loop 0 assets/demo.gif
```

> 单个 GIF 请控制在 **10 MB 以内**，`assets/` 文件夹总大小不超过 **50 MB**。

### 5. 填写依赖列表

编辑 `requirements.txt`，列出你的 notebook 需要的额外 pip 包。

**不需要填写**：`torch`、`torchvision`、`rocm` 相关包（已在 Basic GPU Environment 中预装）。

若无额外依赖，保留空文件即可（文件必须存在）。

### 6. 在 aup-learning-cloud 中测试

提交前请完成以下验证（**两个 notebook 都要测试**）：

1. 打开 aup-learning-cloud → 选择 **Basic GPU Environment**
2. 从头到尾运行 `main.ipynb`（英文版）的所有 Cell，确认无报错
3. 从头到尾运行 `main_zh.ipynb`（中文版）的所有 Cell，确认无报错

### 7. 提交 Pull Request

1. 将修改 commit 并 push 到你的 fork
2. 向本仓库发起 Pull Request
3. GitHub 会显示提交 checklist —— **逐项勾选后再提交**
4. 等待主办方 Review 并合并

## 文件大小限制

提交内容总大小请控制在 **100MB 以内**。

大型数据集或模型权重请使用外链（如 Hugging Face、Google Drive），并在 README 中注明。

## 有问题？

在 GitHub 上提 Issue，或直接联系比赛主办方。
