考公信息追踪系统
================

## 项目结构

```
exam_tracker/
├── crawler.py      # 爬虫主程序
├── dashboard.html  # 自动生成的仪表盘（运行后出现）
├── data/
│   ├── notices.json   # 公告数据库（自动生成）
│   └── crawler.log    # 运行日志（自动生成）
└── README.txt      # 本文件
```

---

## 快速开始

### 第一步：安装依赖

打开命令提示符（cmd）或 PowerShell，执行：

  pip install requests beautifulsoup4 schedule lxml

### 第二步：立即抓取一次

  cd exam_tracker
  python crawler.py

程序会自动：
1. 抓取浙江省考、浙江事业编、温州人社局等网站
2. 保存公告到 data/notices.json
3. 生成 dashboard.html

### 第三步：打开仪表盘

直接双击打开 dashboard.html，即可查看所有公告。

---

## 自动定时运行（推荐）

让程序每天8:00和20:00自动抓取，有新公告时更新仪表盘：

  python crawler.py --daemon

注意：需要保持这个命令窗口开着（或设置为开机自启）。

---

## 开机自启设置（Windows）

方法一：任务计划程序
1. 按 Win+R，输入 taskschd.msc
2. 创建基本任务
3. 触发器选"登录时"
4. 操作选"启动程序"
5. 程序填：python
   参数填：C:\完整路径\exam_tracker\crawler.py --daemon

方法二：批处理文件（简单）
创建 start_tracker.bat，内容：
  @echo off
  cd /d C:\Users\chenx\WorkBuddy\Claw\exam_tracker
  python crawler.py --daemon
然后把这个bat文件放到：
  C:\Users\chenx\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\

---

## 配置微信推送（可选）

有新公告时自动推送到微信：

1. 访问 https://sct.ftqq.com 注册Server酱
2. 用微信扫码绑定
3. 复制你的 SendKey
4. 打开 crawler.py，找到第27行：
   SERVERCHAN_KEY = ""
   改为：
   SERVERCHAN_KEY = "你的SendKey"

之后有新公告时，微信服务号会自动通知你。

---

## 监控的网站

- 浙江省公务员考试录用网 gwy.zjks.com
- 浙江省事业单位招聘 qssy.zjks.com
- 温州市人力资源和社会保障局
- 国家公务员局

如需添加其他网站，在 crawler.py 的 TARGETS 列表里增加配置项即可。

---

## 常见问题

Q: 抓取失败/没有数据怎么办？
A: 部分政府网站有反爬措施，可能需要手动更新 HEADERS 里的 User-Agent，
   或者适当增加延迟（time.sleep(5)）。

Q: 数据在哪里？
A: 所有公告保存在 data/notices.json，可以用记事本打开查看。

Q: 如何只看温州相关公告？
A: crawler.py 里每个 target 的 keywords 列表已经包含"温州"，
   会自动过滤只保留包含关键词的公告。
