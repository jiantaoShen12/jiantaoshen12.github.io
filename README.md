# 申剑涛 - 个人学术主页

基于 GitHub Pages 的个人学术主页，参照 [qiangweipeng.github.io](https://qiangweipeng.github.io) 风格设计。

## 部署步骤

### 1. 创建 GitHub 仓库
- 在 GitHub 上创建一个名为 `你的用户名.github.io` 的仓库（例如 `shenjiantao.github.io`）
- 仓库必须设为 **Public**

### 2. 上传文件
```bash
cd shenjiantao.github.io
git init
git add .
git commit -m "Initial commit: academic homepage"
git branch -M main
git remote add origin https://github.com/你的用户名/你的用户名.github.io.git
git push -u origin main
```

### 3. 启用 GitHub Pages
- 进入仓库 → Settings → Pages
- Source 选择 `Deploy from a branch`
- Branch 选择 `main` / `/ (root)`
- 保存后等待几分钟即可访问

### 4. 访问你的主页
打开 `https://你的用户名.github.io`

## 自定义

- **头像**: 替换 `index.html` 中的 `avatar-placeholder` 为 `<img>` 标签，将头像图片放入 `images/` 文件夹
- **内容**: 直接编辑 `index.html` 中对应 section 的内容
- **颜色**: 修改 `:root` 中的 CSS 变量
- **技能条**: 调整 `skill-bar-fill` 的 `width` 百分比
