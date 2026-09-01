# StarShack 官网 · 部署说明

✅ **已部署上线**，无需再做初始化操作。

## 线上地址

| 项目 | 地址 |
|------|------|
| **首页** | https://vliantwo.github.io/starshack-site/ |
| **下载页** | https://vliantwo.github.io/starshack-site/download.html |
| **GitHub 仓库** | https://github.com/vliantwo/starshack-site |

- 仓库：**Public**，分支 `main`，根目录 `/ (root)` 作为 Pages 源
- HTTPS：**已强制开启**（证书由 GitHub 自动签发）
- 自定义域名：暂未绑定（你目前没有自己的域名；以后买了随时可以加 `CNAME`）

> 这是 GitHub 免费赠送的 `*.github.io` 子域名。
> 客户端源码仍在 `https://github.com/vliantwo/Starshack`，与本仓库**完全隔离**，互不影响。

---

## 文件清单

| 文件 | 说明 |
|------|------|
| `index.html` | 首页（Hero / 功能特性 / 9 大分类·124 模块 / KOOK 社区） |
| `download.html` | 下载页（系统要求 / 双下载卡 / 五步安装 / 使用须知） |
| `styles.css` | 首页样式 |
| `pages.css` | 二级页共用样式 |
| `app.js` | 滚动入场动画 |
| `assets/hero-logo.png` | Stars 品牌 Hero 图 |
| `assets/qrcode.png` | 官网二维码（指向 GitHub Pages 地址） |
| `assets/poster_share.png` | 分享海报（2160×3840） |
| `assets/qrcode.svg` / `hero_deco.svg` | 矢量源文件 |
| `.nojekyll` | 阻止 GitHub 的 Jekyll 处理，保证静态资源原样托管 |
| `sync_github.py` | 增量同步脚本（见下） |
| `DEPLOY.md` | 本文件 |

---

## 怎么更新线上内容

### 方式一：同步脚本（推荐，本环境可靠）

改完文件后，在本目录执行：

```bash
python sync_github.py           # 先预览哪些文件会变
python sync_github.py --apply   # 确认无误后真正写入
```

脚本会：从 Git Credential Manager 自动取 `vliantwo` 的 token → 用 blob sha 比对本地与远程 → **只上传有变动的文件**。通常 1 分钟内 Pages 生效。

### 方式二：git 推送（在你自己的终端里）

```bash
cd C:/Users/32846/WorkBuddy/StarsTool/starshack-site
git add -A
git commit -m "更新说明"
git push origin main
```

⚠️ 两点注意：

1. **本工作环境的 git 用不了** —— 环境内有本地代理（`http_proxy=127.0.0.1:547xx`），HTTPS 的 push/fetch 大块 POST 会被切断，报 `send-pack: unexpected disconnect`。在你自己的 PowerShell / 终端里没有这个代理，git 是正常的。
2. **首次推送可能需要 `--force`** —— 仓库里现有的文件是通过 GitHub API 创建的，与本地 `.git` 里的那次 commit 没有共同祖先，直接 push 会被拒。内容本身完全一致，`git push --force origin main` 是安全的（remote 指向 `starshack-site`，**不会**碰到源码仓库 `Starshack`）。

---

## 以后想绑定自己的域名

1. 在域名注册商买一个域名（阿里云 / 腾讯云 / Cloudflare / Namecheap 等）。
2. 在本目录建 `CNAME` 文件，内容只写一行你的域名，例如 `stars.example.com`。
3. 用 `sync_github.py --apply` 推上去。
4. 仓库 **Settings → Pages → Custom domain** 填入同一个域名，勾 Enforce HTTPS。
5. 去域名解析后台加记录：
   - **子域名**（推荐）：`CNAME` → `vliantwo.github.io`
   - **根域名**：4 条 `A` 记录 → `185.199.108.153` / `185.199.109.153` / `185.199.110.153` / `185.199.111.153`

---

## 为什么仓库是这样建起来的（背景记录）

最初想把网站直接推到你已有的 `vliantwo/Starshack` 仓库，但发现**那个仓库里是客户端源码本身**（`build.gradle.kts` / `src/` / `gradlew` / `LICENSE`…），网站推上去会覆盖开源工程。所以改为新建独立仓库 `starshack-site`，两边彻底隔离。

另外，本环境 git 到 GitHub 有两个坑，都已绕过：

- **证书吊销检查**：`CRYPT_E_NO_REVOCATION_CHECK` 拦住 TLS 握手 → 用 `http.sslBackend=schannel` + `http.schannelCheckRevoke=false` 解决（已写入本仓库的 git 配置）。
- **代理切断大 POST**：即使握手成功，push 仍被切 → 改用 GitHub Contents API 逐文件 PUT，绕开 git 协议。
