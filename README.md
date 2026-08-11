<p align="center">
  <img 
    src="icons/icon.png"
    alt="ok-Onmyoji logo"
    width="128"
    height="128"
  />
</p>

<h1 align="center">ok-Onmyoji</h1>

<p align="center">
基于图像识别的阴阳师(Onmyoji)自动化程序，支持后台运行，基于 <a href="https://github.com/ok-oldking/ok-script">ok-script</a> 开发。
<br />
An image-recognition-based automation tool for Onmyoji, with background mode support, developed with <a href="https://github.com/ok-oldking/ok-script">ok-script</a>.
</p>

<p align="center"><i>通过模拟 Windows 用户接口进行操作，无内存读取、无文件修改</i></p>

<!-- Badges -->
<div align="center">

![平台](https://img.shields.io/badge/platform-Windows-blue)
[![GitHub release](https://img.shields.io/github/v/release/YunLiuZ/ok-Onmyoji)](https://github.com/YunLiuZ/ok-Onmyoji/releases)
[![总下载量](https://img.shields.io/github/downloads/YunLiuZ/ok-Onmyoji/total)](https://github.com/YunLiuZ/ok-Onmyoji/releases)

</div>

## ⚠️ 免责声明

本软件为外部辅助工具，旨在自动化《阴阳师》的部分游戏流程。它完全通过模拟常规用户界面与游戏交互，遵循相关法律法规。本项目旨在简化用户的重复性操作，不会破坏游戏平衡或提供不公平优势，也绝不会修改任何游戏文件或数据。

本软件开源、免费，仅供个人学习与交流使用，请勿用于任何商业或营利性目的。开发者团队拥有本项目的最终解释权。因使用本软件而产生的任何问题，均与本项目及开发者无关。

**使用本软件即表示您已阅读、理解并同意以上声明，并自愿承担一切潜在风险。**

## 🚀 快速开始

1. **下载安装包**：从下方的"下载渠道"中选择一个，下载最新的压缩包。
2. **解压运行**：解压后双击 `ok-Onmyoji.exe` 即可运行，下载后可应用内更新。
3. **配置任务**：根据需求在软件界面配置任务参数并执行。

## 📥 下载渠道

* **[GitHub](https://github.com/YunLiuZ/ok-Onmyoji/releases)**: 官方发布页。（**请下载 `7z` 压缩包，而不是 `Source Code` 源码压缩包**）
* **[Mirror酱](https://mirrorchyan.com/zh/projects?rid=ok-Onmyoji)**: 国内镜像，下载可能需要购买其平台的 CD-KEY。

## 运行要求与推荐设置

- 系统：Windows
- 分辨率：支持所有 16:9 分辨率，建议 2560×1440、1920×1080、1600×900、1280×720
- 语言：支持简体中文
- 路径：安装/运行路径使用纯英文

---

## 🎮 功能一览

- **多种功能**：支持多开、支持一键多个任务、支持定时任务
- **战斗任务**：魂土、困二八、觉醒、活动爬塔
- **日常任务**：签到、式神委派、寄养、挂卡、同心之兰
- **日常-战斗任务**：地域鬼王、个人突破、寮突破、金币妖怪、经验妖怪

## 使用前必读

1. **游戏选择**
- 请使用MuMu模拟器，并在初始页面的游戏中心，搜索阴阳师，第一个应用下载安装即可

   <img src="docs/images/MuMuOnm.png" width="600" />

2. **模拟器设置**
- 建议将固定窗口大小打开，其他设置默认即可

   <img src="docs/images/MuMu.png" width="600" />

3. **游戏设置！！！！！**
- 阴阳师最近更新了新客户端，使用前请保证客户端是最新的
- 画质可自行定义，但请保证在模拟器中流畅运行，当有明显卡顿的时候，请降低画质
- 点击，头像→音画→画质，请关闭登录动画，打开高清字体，町中模式选择原生
- 点击，头像→交互→战斗，打开结算加成图标合成，关闭战斗结算个性化
- 点击，图鉴→外观设置 将战斗主题设置为怀旧主题，签到主题设置为默认主题，庭院皮肤设置为初语谧景（不是换新），町中皮肤设置为故梦雅景，结界皮肤设置为妖伞结界，鲤鱼旗皮肤设置为吉鲤游风
- 一切设置尽量都为默认的皮肤是最好的，其实并非如此严格，有些特效简单的皮肤是可以使用的，但为了避免不必要的ui问题，还请使用前更换好默认皮肤，如果出现了卡住报错的情况，请先检查某场景下的皮肤是不是为默认皮肤

4. **ok-Onmyoji的使用**
- 第一次使用请先启动游戏，然后再启动ok-Onmyoji
- 请先选择好游戏窗口，请务必选择好游戏窗口，请一定记得选择好游戏窗口

   <img src="docs/images/ok1.png" width="600" />

- 关于窗口的选择比较简单，在选择窗口页面选择好要控制的对应的模拟器即可，请注意MuMu模拟器的后缀即可分辨对应的模拟器窗口，务必选择ADB截图，这样才能在后台运行
- 当选择好窗口后点击截图按钮，稍等片刻，弹出截图并显示游戏页面，恭喜您成功运行本项目
- 请务必注意输入冒号：逗号，等符号时务必使用英文的格式
- 实时触发页面：有一个后台调度器，主要对应调度面板中的各种任务，使用前请先去调度面板中，勾选想要定时执行的任务，并设置好各个参数，下次运行时间根据上次运行时间和间隔自动计算保存，设置好后，在实时触发页面将后台调度启用任务启动，即可定时运行任务
- 任务页面：请先设置好参数，在设置参数前请先注意参数的描述，点击开始即可运行任务，启动前可以手动将游戏页面回到主页，避免出现错误
- 多开助手页面：账号的编号不要重复使用，建议一个编号尽量对应一个角色，这样可以避免反复的修改参数

   <img src="docs/images/ok2.png" width="600" />

5. **ok-Onmyoji的启用演示**
- 以刷御魂演示
- 首先启动多开（真的有单人刷副本的吗，应该没有吧，应该没有吧，八嘎呀路，如果真是一个人刷，请快去创建一个小号）
- 第一个参数角色，这个参数的初衷是为了让用户填写一些容易混淆的信息，比如这个任务是为了控制谁，用的是什么分组帮助确认下面的信息的正确性，不填也无伤大雅
- 很多参数都有注释，理解应该问题不大，在这里强调一点，绝大多数的第X个预设队伍就是该任务的预设队伍，但当下面的参数出现其他的预设队伍时请填写下面的参数。比如魂土，就在下方提供了独立的御魂设置参数：御魂悲鸣，御魂神罚，御魂虚无，主要是为了打不同的副本时来回切换不同的队伍，所以请设置好一劳永逸
- 还有一件事，锁定阵容参数比较特殊，当不选的时候默认会锁定阵容进入战斗，当选上后，第一次战斗会切换阵容，第二次战斗锁定阵容，所以当想切换阵容的时候可以考虑将这个参数勾选上，还有一件事，强烈建议自己刷一次后锁定阵容，尽量少用这个参数，这个辅助如果只是当作减少反复刷副本的次数时它应该会很好用，对于一些特殊情况作者也尽量的处理了，也会经常出现意想不到的情况，所以尽量让辅助只做重复的事，当然这些功能作者反复测过很多次，基本上没有什么问题
- 下图设置了队长，双开之后设置另一个为队员即可，建议要刷就两个号一起用辅助一起刷，这样可以尽可能的避免两边游戏的速度不一样
- 关于名字的输入，作者用的不是精准匹配，因为当名字中有一些特殊符号的时候会识别不出来，所以尽量输入账号的文字部分，比如爷傲丶奈我何，可以输入爷傲|奈我何，|表示或者，系统会去匹配爷傲和奈我何，如果实在识别不出来可以考虑改名

   <img src="docs/images/ok3.png" width="600" />
6. **注意事项**
- 一键多任务和实时触发中的任务调度，是有自动启动游戏的功能的，但前提是应该选择好对应的窗口和游戏角色，而且请务必先在各个任务的参数设置中将参数设置好！！
- 结界突破的使用：结界突破的使用很特别，在这个项目中结界突破的突破顺序是设置好的，先正着打八次，然后退四次，然后打第九次刷新，倒着打九次刷新，开始循环，所以在第一次使用时，请先将没打完的突破手动打完一次然后从零开始即可。这样可以帮助项目识别什么时候需要退四次保证一直都是57级，所以将你的结界突破完全交给ok-onmyoji即可。
- 在第一次启动后窗口选择就会出现对应的窗口只是显示未连接，所以如果不想手动启动游戏的话可以尝试启动该项目后直接使用上述的两个功能，而其他的任务选项暂时没有完整启动游戏的功能，他们只能在游戏已启动的情况下进行使用（这里的启动是指进入到庭院）。
- 使用任务调度时请不要将各个任务的执行时间设置得太过紧凑，比如想在晚上一点刷100次魂土，预计一小时，那下个任务就可以设置在晚上两点半，请给足每个任务充足的运行时间，这很重要
- 这里提一下寮突破在晚上九点后可以无限制次数的攻破，该任务的初衷是给玩僵尸寮的阴阳师一次性刷几十次的，当有次数限制的时候作者暂时还没有写相关代码，但后续会优化
7. 该项目还有很多不足，作者还在努力开发其他功能，希望各位用的开心，会尽可能的去维护这个项目

## 💬 加入我们

* **QQ 交流群**：`871543404`（入群答案：`YL`）

本项目基于 [ok-script](https://github.com/ok-oldking/ok-script) 框架开发，简单易维护。欢迎有兴趣的开发者使用 [ok-script](https://github.com/ok-oldking/ok-script) 开发您自己的自动化项目。

## 🔗 使用 ok-script 的项目

* 阴阳师 [https://github.com/YunLiuZ/ok-Onmyoji](https://github.com/YunLiuZ/ok-Onmyoji)
* 终末地 [https://github.com/AliceJump/ok-end-field](https://github.com/AliceJump/ok-end-field)
* 鸣潮 [https://github.com/ok-oldking/ok-wuthering-waves](https://github.com/ok-oldking/ok-wuthering-waves)
* 鸣潮（日常一条龙-优化版）[https://github.com/zzc-tongji/ok-ww-enhanced](https://github.com/zzc-tongji/ok-ww-enhanced)
* 原神（停止维护，后台过剧情可用）[https://github.com/ok-oldking/ok-genshin-impact](https://github.com/ok-oldking/ok-genshin-impact)
* 少前2 [https://github.com/ok-oldking/ok-gf2](https://github.com/ok-oldking/ok-gf2)
* 星铁 [https://github.com/Shasnow/ok-starrailassistant](https://github.com/Shasnow/ok-starrailassistant)
* 星痕共鸣 [https://github.com/Sanheiii/ok-star-resonance](https://github.com/Sanheiii/ok-star-resonance)
* 二重螺旋 [https://github.com/BnanZ0/ok-duet-night-abyss](https://github.com/BnanZ0/ok-duet-night-abyss)
* 白荆回廊（停止更新）[https://github.com/ok-oldking/ok-baijing](https://github.com/ok-oldking/ok-baijing)

## 致谢

* [ok-oldking/OnnxOCR](https://github.com/ok-oldking/OnnxOCR)
* [zhiyiYo/PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)
* [ok-oldking/ok-script](https://github.com/ok-oldking/ok-script)
