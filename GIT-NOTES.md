# Git 学习笔记（journey-of-learning）

> 这份笔记是按我自己踩过的坑写的，不是通用教程。忘了直接翻。

---

## 一、日常五步（90% 的时间都在重复这个）

```bash
# 1. 起点干净，并在 main 上
git switch main
git pull

# 2. 开分支（永远不在 main 上直接改）
git switch -c feature/xxx

# 3. 改代码 → 先跑通 → 再提交
git add .
git commit -m "feat: 做了什么"

# 4. 推分支
git push -u origin feature/xxx        # 第一次要 -u，之后直接 git push

# 5. GitHub 建 PR → Squash and merge → 回本地收尾
git switch main
git pull
git branch -d feature/xxx
```

**记住四句话：**
1. 永远从 main 拉分支，永远不在 main 上直接改
2. 一个分支只干一件事
3. 推之前先跑一遍代码
4. 合并完回本地 pull，然后删分支

---

## 二、提交前检查清单（每次都要过）

- [ ] `git status` 看清楚：**要提交的文件是否都在"暂存的更改"里**
- [ ] 提交说明与实际改动**对得上**（写"加了游戏"，就别只提交 README）
- [ ] 代码能跑通
- [ ] 没有把密钥、路径、本地配置提交进去
- [ ] 文件名是英文的

> ⚠️ 我踩过的坑：第一次提交时说明写"增加猜字小游戏"，结果暂存区只有 README.md，`.py` 根本没进去。图形界面会把这个藏起来，**终端 `git status` 才看得清**。

---

## 三、命令速查

### 看状态
```bash
git status                  # 当前状态，最常用
git log --oneline -10       # 简洁历史
git log --stat              # 带文件改动统计
git diff                    # 未暂存的改动
git diff --staged           # 已暂存但未提交的改动
git show --stat HEAD        # 上一条提交装了什么
git branch -vv              # 本地分支 + 追踪的远程分支
```

### 提交
```bash
git add .                       # 全部加入暂存区
git add 文件名                   # 只加一个
git commit -m "说明"             # 提交
git commit --amend -m "新说明"   # 改写上一条（仅限未推送时！）
```

提交说明前缀约定：

| 前缀 | 用途 |
|---|---|
| `feat:` | 新功能 |
| `fix:` | 修 bug |
| `docs:` | 只改文档 |
| `refactor:` | 重构，不改行为 |
| `test:` | 测试相关 |
| `chore:` | 杂活（配置、依赖） |

### 分支
```bash
git branch                    # 本地分支，* 表示当前
git switch -c feature/xxx     # 新建并切过去
git switch main               # 切分支
git branch -d feature/xxx     # 删已合并的分支
git branch -D feature/xxx     # 强删（确认不要了再用）
git push origin --delete feature/xxx   # 删远程分支
```

> 老命令 `git checkout -b` 和 `git checkout` 也能用，但新版的 `switch`（切分支）和 `restore`（还原本地文件）语义更清楚，推荐用新的。

### 同步
```bash
git pull                       # = fetch + merge
git fetch                      # 只拉取，不改工作区
git push                       # 推已建立追踪的分支
git push -u origin 分支名       # 第一次推，建立追踪
```

### 撤销（按"危险程度"排序）
```bash
git restore 文件名                 # 丢掉工作区的改动（不可恢复！）
git restore --staged 文件名        # 从暂存区拿出来，改动保留
git commit --amend                 # 改写上一条提交
git revert <commit>               # 生成一条"反向提交"，安全，适合已推送的
git reset --soft HEAD~1           # 撤销提交，改动留在工作区（未推送时）
git reset --hard HEAD~1           # 连改动一起删（危险，几乎别用）
```

**原则：已推送的提交用 `revert`，没推送的才用 `reset`/`amend`。**

---

## 四、PR 三种合并方式

| 方式 | 结果 | 什么时候用 |
|---|---|---|
| **Merge commit** | 保留分支上所有提交 + 多一条合并节点 | 想保留完整过程、多人协作 |
| **Squash and merge** | 整条分支压成 1 条提交 | **个人项目默认选这个** |
| **Rebase and merge** | 提交逐个接到 main 末尾，线性历史 | 进阶，追求干净历史 |

**关键常识：Squash 后的提交消息 = PR 标题。**
所以 PR 标题就是最终写进历史的那句话，花三十秒好好写，别用 GitHub 从分支名自动生成的那个。

> 我踩过的坑：PR 标题没改，最后 main 上的记录是 `Feature/max guess (#1)`，而不是"猜数字增加7次机会限制"。

---

## 五、常见报错对照

| 报错 | 原因 | 解决 |
|---|---|---|
| `no upstream branch` | 第一次推忘了 `-u` | `git push -u origin 分支名` |
| `Repository not found` | 仓库名错 / 私有库没权限 | 核对地址；授权要给 `repo` scope |
| `Updates were rejected` | 远程有你本地没有的提交 | `git pull --rebase origin main` 再推 |
| `fatal: not a git repository` | 不在仓库目录里 | `cd` 到项目目录，或 `git init` |
| `CONFLICT (content): Merge conflict in xxx` | 两边改了同一行 | 见第六节 |
| `deleting branch ... not yet merged to HEAD` | 先删分支、后 pull，顺序错了 | 无害，但下次先 `git pull` 再 `git branch -d` |

### 中文文件名显示成八进制
```
modified: "\347\214\234\346\225\260..."
```
不是文件坏了，是 Git 默认转义非 ASCII。修：
```bash
git config --global core.quotepath false
```
更彻底的做法：**文件名用英文**，跨平台、上 CI 都不会出问题。

---

## 六、冲突处理预案（还没实操过，先记着）

现象：`git pull` 或合并时报 `CONFLICT`，文件里出现：

```
<<<<<<< HEAD
你这一边的代码
=======
对方那一边的代码
>>>>>>> feature/xxx
```

处理：

1. 打开那个文件，**手动改成你要的最终版本**，把 `<<<<<<<`、`=======`、`>>>>>>>` 三行全删掉
2. `git add 文件名`（表示"我解决完了"）
3. `git commit`（如果用 `git pull` 触发的，直接 `git commit` 就行，不要带 -m 以外的参数）
4. 继续 `git push`

**别慌，冲突不是错误，是 Git 在问你"这两个版本要哪个"。**

---

## 七、我踩过的具体坑（复盘）

1. **`random.randint(1, 101)` vs `randint(1, 100)`**
   `randint` 是**闭区间**（两边都包含），`range` 是**左闭右开**。这两个最容易混。想生成 1~100 就写 `randint(1, 100)`。

2. **暂存区遗漏**  
   提交说明写的东西，必须在 `git status` 的"暂存的更改"里真的存在。

3. **提交作者名不一致**  
   中途改过 `user.name`，导致同一仓库里出现两个作者名。统一：
   ```bash
   git config --global user.name "JiaRong213"
   git config --global user.email "你的GitHub邮箱"
   ```
   邮箱必须和 GitHub 账号一致，否则贡献格子不亮。

4. **`.gitignore` 一定要早建**  
   Python 跑一次就生成 `__pycache__`。早建忽略规则，比事后从历史里删干净（要用 `git filter-repo`）省事一百倍。

5. **提交作者显示 geomet 图案（identicon）**  
   说明本地 email 没绑到 GitHub 账号。

---

## 八、.gitignore（Python 项目模板）

```
__pycache__/
*.py[cod]
.venv/
venv/
env/
.env
.vscode/
.idea/
.DS_Store
Thumbs.db
```

---

## 九、还没学的（按优先级）

- [ ] **冲突处理** —— 故意制造一次练手：开分支改第 6 行，main 上也改同一行，合并看冲突
- [ ] **`.gitignore` 与 `git rm --cached`** —— 已经误提交的文件怎么移出仓库
- [ ] **SSH key** —— 比 GCM/令牌更稳，不怕网络抽风
- [ ] **tag 与 release** —— 给版本打标记
- [ ] **rebase** —— 整理提交历史
- [ ] **`git revert` 实战** —— 已推送的代码怎么安全撤回

---

## 十、当前项目状态

- 仓库：`github.com/JiaRong213/journey-of-learning`
- 主分支：`main`
- 内容：猜数字小游戏（`MAX_TRIES = 7` 次数限制版）
- 已完成流程：建分支 → 改代码 → 提交 → 推送 → PR #1 → Squash 合并 → 回本地同步 → 删分支
