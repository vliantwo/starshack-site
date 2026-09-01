# StarShack 官网 · GitHub Pages 部署指引

纯静态站点（HTML / CSS / JS + 图片），**无需构建**，推上 GitHub 开启 Pages 即可。

> 本方案使用 GitHub 免费赠送的 `*.github.io` 子域名，**不需要你自己买域名**。
> 若以后想绑定自己的域名，再单独做自定义域名（CNAME + DNS），本目录已含 `.nojekyll` 可直接复用。

---

## 一、在 GitHub 上建仓库

1. 登录 GitHub（你提供的 `3284689009@qq.com` 是**登录邮箱**，不是用户名；真实用户名在 `github.com/<这里>` 的地址栏可见）。
2. 右上角 `+` → **New repository**。
3. Repository name 填：`starshack`（这会变成 URL 的一部分，建议用小写英文）。
4. 选 **Public**（私有仓库 GitHub Pages 需付费）。
5. **不要**勾选 "Add a README file" / .gitignore / license（保持空仓库，避免和本地文件冲突）。
6. 点 **Create repository**，进入后复制它的 HTTPS 地址，形如：
   `https://github.com/<USERNAME>/starshack.git`

---

## 二、本地推送（在 starshack-site 目录下执行）

> 注意：你的 `C:\Users\32846` 主目录本身已是一个 git 仓库，所以在 `starshack-site` 里单独 `git init` 会建一个**嵌套仓库**，属正常操作，照跑即可。

```bash
cd C:/Users/32846/WorkBuddy/StarsTool/starshack-site

git init
git add -A
git commit -m "StarShack official site"

git branch -M main
git remote add origin https://github.com/<USERNAME>/starshack.git
git push -u origin main
```

push 时会要求登录 GitHub（弹窗 / 或填 Personal Access Token，密码方式已停用）。

---

## 三、开启 GitHub Pages

1. 进入仓库 → **Settings** → 左侧 **Pages**（或 **Code and automation → Pages**）。
2. **Build and deployment** → Source 选 **Deploy from a branch**。
3. Branch 选 **main**，目录选 **/ (root)**。
4. 点 **Save**。
5. 等 1–2 分钟，页面会显示：

   > Your site is live at https://<USERNAME>.github.io/starshack/

6. 勾选 **Enforce HTTPS**（证书由 GitHub 自动签发，约几分钟生效）。

---

## 四、访问地址

- 首页：`https://<USERNAME>.github.io/starshack/`
- 下载页：`https://<USERNAME>.github.io/starshack/download.html`

把上面 `<USERNAME>` 换成你的真实 GitHub 用户名即可。

---

## 五、以后改内容怎么更新

直接在 `starshack-site/` 改文件，然后：

```bash
git add -A
git commit -m "更新说明"
git push
```

GitHub Pages 会自动重新发布（通常 1 分钟内生效）。

---

## 文件清单（本目录）

| 文件 | 说明 |
|------|------|
| `index.html` | 首页（Hero / 功能 / 9 大分类模块 / KOOK 社区） |
| `download.html` | 下载页（系统要求 / 安装步骤 / 使用须知） |
| `styles.css` | 首页样式 |
| `pages.css` | 二级页共用样式 |
| `app.js` | 滚动入场动画 |
| `assets/` | 品牌图、二维码、分享海报 |
| `.nojekyll` | 阻止 GitHub 的 Jekyll 处理，确保静态资源原样托管 |
| `DEPLOY.md` | 本文件 |
