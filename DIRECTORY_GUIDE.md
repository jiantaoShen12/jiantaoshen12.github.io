# 项目目录说明

这是 Jiantao Shen 的静态学术主页，沿用 GitHub Pages，不需要前端依赖安装或构建。

- 实际根目录：`D:\Project_github\jiantaoshen12.github.io`
- 远程仓库：`https://github.com/jiantaoShen12/jiantaoshen12.github.io`
- 公开站点：`https://jiantaoshen12.github.io/`

| 路径 | 用途 |
| --- | --- |
| `index.html` | 主页入口，个人介绍、动态、论文、研究方向、教育及获奖记录 |
| `cv.html` | 英文 CV 的可编辑来源，同时提供浏览、打印样式和 PDF 下载 |
| `profile.jpg` | 原仓库已有的头像，保持不变 |
| `assets/pdf/` | 网站提供下载的英文 CV PDF |
| `scripts/build_cv.py` | 从 `cv.html` 的内容生成 PDF，避免两份 CV 内容分别维护 |
| `work/` | 被 Git 忽略的本地预览与 QA；`20261113_homepage_cv/` 保存本次检查记录和渲染图 |
| `_config.yml` | GitHub Pages / Jekyll 设置，排除维护文档、脚本和本地 QA 目录 |
| `README.md` | 项目介绍和本地维护说明 |
| `AGENTS.md` | 项目执行规则、生成和预览命令 |
| `.git/`, `.gitignore` | Git 元数据和忽略规则 |
| `.gitattributes` | 将 PDF 标记为二进制，防止 Windows 换行转换改变文件内容 |

本项目没有实验训练、原始数据或预处理数据；个人资料来源是原仓库公开的 `index.html` 和 `README.md`。本次改版参考张振毅主页的信息组织，不复制其个人经历或成果。
