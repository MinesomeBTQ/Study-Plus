# Study Plus v 1.0.4

一款使用Python开发的可用于课堂多媒体教学的工具集

目前有 `随机抽号、课程表、文件定时启动` 等功能

## 安装教程

选择 **Study Plus Installer.exe** ，下载并运行

根据提示进行安装即可

若要进行更新，在同一文件夹下安装新版本即可（为避免其他问题，建议先使用安装工具删除旧版再安装新版）

### 软件架构

[...]代表由程序生成的配置文件，安装后这些文件不存在，删除后这些文件依然保留

```
-- data    存放软件数据
   -- images    存放图片文件
      -- ...
   -- static    存放样式表以及静态颜色、背景信息
      -- [bg.json]    背景信息
      -- [color.json]    颜色信息
      -- menu.qss    菜单样式表
      -- style.qss    全局样式表
   -- [file_starter.json]    文件定时启动数据
   -- [mainWindow.json]    主窗口数据
   -- [randoms.json]    随机抽号数据
   -- [schedule.json]    课程表内容数据
   -- [schedule_func.json]    课程表功能数据
-- Study Plus.exe    软件主体
```

### 使用说明

#### 随机抽号

双击悬浮球即可进行抽号

在随机抽号设置界面可以设置 数字抽号 与 自定义抽号

· 数字抽号：可以在0~99内设置抽号范围

· 自定义抽号：可以自行编辑或从外部文件导入抽号项目

注：从外部文件导入，即将一个文本(.txt)文件按用户输入的分隔符分开，分别作为抽号项目

如 `Andy,Alex,BT.Q` 可以以`,`为分隔符分为`Andy` `Alex` `BT.Q`三项

#### 课程表

当检测到当前星期、时间符合用户设置的课程表中某一项时，发送通知

通知内容由用户自行设置，其中的“@N”将被替换为当前课程名称

#### 文件定时启动

当检测到系统时间符合用户设置的启动时间时，自动打开用户指定的文件

可用于播放课间操等

#### 其他

悬浮球的设置

在 设置 -> 悬浮球设置 中可以设置悬浮球大小、透明度

设置程序启动时只显示悬浮球，不打开主窗口

在 设置 -> 悬浮球设置 中设置“启动时隐藏主窗口”，若要打开主窗口，可以右键悬浮球或点击任务选项卡中的上箭头打开

### 更新日志

#### v 1.0.0
最初版本

#### v 1.0.1
该版本存在 **大型问题**：开机自启动失败

· 修改了在任务选项卡的图标

· 修改了部分文本

#### v 1.0.2
该版本存在 **小型问题**：悬浮球与字体大小可能不匹配
· 修复了开机自启动失败的Bug

· 新增了检测新版本并提示安装的功能

· 新增了隐藏悬浮球设置

· 若设置主窗口开启时隐藏，会添加任务选项卡图标

· 程序会识别并重置旧版本中已经不适用的配置文件

· 优化了其他体验

#### v 1.0.3
该版本存在 **中等问题**：版本号错误

· 调整了悬浮球大小的设置，使其适应不同分辨率

· 优化了单/多选按钮的UI样式

· 修复了错误显示的文本

#### v 1.0.4
最新版本

· 覆盖了 v1.03 中版本号的错误

注：

· 小型问题：对使用体验影响很小，或可以通过设置解决的问题

· 中等问题：功能正常，但对使用有明显影响

· 大型问题：功能异常，或对使用有巨大影响

### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request