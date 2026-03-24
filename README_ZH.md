# aup-learning-cloud-case-hub

<div align="center">

[![AMD](https://img.shields.io/badge/AMD-ED1C24?style=flat-square&logo=amd&logoColor=white)](https://www.amd.com)
[![ROCm](https://img.shields.io/badge/ROCm-FF6B35?style=flat-square&logo=amd&logoColor=white)](https://rocm.docs.amd.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-欢迎-brightgreen?style=flat-square)](./CONTRIBUTING_ZH.md)

</div>

> 基于 [aup-learning-cloud](https://github.com/AMDResearch/aup-learning-cloud) 的学生 AI 作品案例库 —— 按比赛归档，一键启动体验。

[English](./README.md)

## 这是什么？

本仓库收录了在 AMD aup-learning-cloud 平台上举办的各类 AI 比赛和工作坊中，学生提交的 notebook 作品。所有案例均运行于 AMD GPU 硬件，可通过 aup-learning-cloud 的 Git 克隆功能一键启动。

## 快速体验（评委 / 访客）

1. 打开你的 **aup-learning-cloud** 实例
2. 选择 **Basic GPU Environment**
3. 填入 Git URL：`https://github.com/amdjiahangpan/aup-learning-cloud-case-hub`
4. 点击 **Start** —— 仓库将自动克隆到你的 home 目录
5. 进入 `cases/`，打开任意 `main.ipynb` 运行

## 目录结构

```
cases/
└── YYYY-MM-活动名称/            ← 每个比赛/工作坊一个文件夹
    ├── README.md / README_ZH.md ← 活动说明 + 获奖名单（双语）
    ├── 01-gold-团队-项目/       ← 一等奖（金奖）
    ├── 02-silver-团队-项目/     ← 二等奖（银奖）
    ├── 03-bronze-团队-项目/     ← 三等奖（铜奖）
    └── 团队-项目/               ← 普通提交
```

## 案例列表

| 活动 | 时间 | 参赛作品数 | 获奖情况 |
|------|------|-----------|---------|
| [南邮寒假大作战](./cases/2026-03-njupt-winter-battle/) | 2026-03 | — | — |

## 参与贡献

学生请参阅 [CONTRIBUTING_ZH.md](./CONTRIBUTING_ZH.md)

提交模板：复制 [`template/`](./template/) 目录即可开始。

## 平台

基于 [aup-learning-cloud](https://github.com/AMDResearch/aup-learning-cloud) —— AMD 开源 AI 教育 JupyterHub 平台，由 AMD GPU 集群驱动。

## 贡献者

<div align="center">
  <a href="https://github.com/amdjiahangpan/aup-learning-cloud-case-hub/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=amdjiahangpan/aup-learning-cloud-case-hub" />
  </a>
</div>
