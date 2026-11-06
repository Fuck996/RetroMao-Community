# MSX platform pack / MSX 平台包 / MSX 機種パック

## 中文

1.1.0 将旧版的流程示例升级为完整平台包，需要主程序 1.0.32。包含日本市场 MSX 标准卡带、日版 Konami 系闭合塑料盒、与内置平台同源的像素机种图及 MSX 字标；tintLogo=true 让字标跟随主题文字色，像素图保持原色。用户主题的显式图标/模型覆盖优先。保留 msx 机种 ID，重新导入更新后原游戏关联不变。没有 ROM 或模拟器，RetroArch 启动配置使用 blueMSX 核心，核心仍需由玩家安装。

卡带壳主体 109 × 69.4 × 16.8 mm，依据 Sony/ASCII《MSX Technical Data Book》印刷页 31（PDF 页 34），25 对触点依据页 32；[原始技术手册](https://hansotten.file-hunter.com/uploads/files/msxtech.pdf)。闭合塑料盒的轮廓、书脊、锁扣和分型线参考 [RC754 日版实物](https://www.generation-msx.nl/software/konami/knightmare-iii---shalom/release/946/)，使用近似比例，不声称是所有厂商统一外壳或毫米级复刻。参考照片和游戏封面不打包。模型是原创网格，通过 tools/build_msx_models.py 重建，进入原 Filament 渲染与动态封面/卡贴管线，缺图沿用主程序占位图。

Logo 来自 [HVR88/Monochrome-Gaming-Logos](https://github.com/HVR88/Monochrome-Gaming-Logos)，固定提交 7eb7ddb7246fa5c39b71d5136e7a527bac03fb7f，png/msx.png，Git blob SHA-1 49da8dbc396199ede0e604395d55bd0add7b7c92。像素图来自 [libretro/retroarch-assets](https://github.com/libretro/retroarch-assets)，固定提交 73106363e14e34c08a5854b4cfbc29f184e3b783，xmb/dot-art/png/Microsoft - MSX.png，blob f855b158aa6cc6c418ca00980880394a00213da1。作者为 Yoshi-kun、Tatsuya79 及项目贡献者；随包保留许可和作者说明。Logo 的使用说明见 licenses/platform-logos-authors.txt，商标仍属于原权利人。原创模型使用 [MIT 许可](LICENSE)。

## English

1.1.0 replaces the old installation-only demo with a complete platform pack for host 1.0.32. Includes Japanese-market MSX cartridge geometry, a Japanese Konami-style closed plastic case, the same pixel-art source as built-in platforms, and the MSX wordmark. tintLogo=true follows theme text color; pixel art retains color and explicit theme overrides take priority. Keep the msx ID to preserve game associations. No ROM/emulator is included; players install the blueMSX RetroArch core themselves.

The cartridge body follows the 109 × 69.4 × 16.8 mm standard from Sony/ASCII's [MSX Technical Data Book](https://hansotten.file-hunter.com/uploads/files/msxtech.pdf), printed p.31/PDF p.34, with 25 contact pairs from p.32. Case proportions, spine, latches and seams reference the [Japanese RC754 package](https://www.generation-msx.nl/software/konami/knightmare-iii---shalom/release/946/); this is an approximation, not a universal vendor shell or millimeter-perfect replica. Reference photos/game covers are excluded. Original meshes are rebuilt by tools/build_msx_models.py and use the existing Filament/artwork/placeholder pipeline.

Logo: [HVR88](https://github.com/HVR88/Monochrome-Gaming-Logos), commit 7eb7ddb7246fa5c39b71d5136e7a527bac03fb7f, png/msx.png, blob 49da8dbc396199ede0e604395d55bd0add7b7c92. Pixel art: [libretro](https://github.com/libretro/retroarch-assets), commit 73106363e14e34c08a5854b4cfbc29f184e3b783, xmb/dot-art/png/Microsoft - MSX.png, blob f855b158aa6cc6c418ca00980880394a00213da1. Credits: Yoshi-kun, Tatsuya79 and contributors. Source notices/licenses are included; logo terms are in licenses/platform-logos-authors.txt. Trademarks remain with their owners; original models use [MIT](LICENSE).

## 日本語

1.1.0 は導入確認だけの旧サンプルを、ホスト 1.0.32 用の完全な機種パックに更新します。日本市場の MSX 標準カートリッジ、Konami 系の閉じたプラスチック箱、内蔵と同じ出典のドット絵と MSX ロゴを含みます。tintLogo=true は文字色に追従し、ドット絵は原色を維持。テーマの明示上書きが優先されます。msx ID を維持し、ゲーム関連を保ちます。ROM/エミュレーターは含まず、blueMSX コアは利用者が導入します。

カートリッジ本体 109 × 69.4 × 16.8 mm は Sony/ASCII の [MSX Technical Data Book](https://hansotten.file-hunter.com/uploads/files/msxtech.pdf) の印刷 31 頁/PDF 34 頁、25 対の端子は 32 頁を参照します。箱の形状、背、留め具、分割線は [日本版 RC754 の実物](https://www.generation-msx.nl/software/konami/knightmare-iii---shalom/release/946/) に基づく近似で、全メーカー共通や精密な複製とはしません。参考写真とゲーム表紙は含めません。独自形状は tools/build_msx_models.py で再生成し、既存の Filament、画像差替え、代替画像を使います。

ロゴ：[HVR88](https://github.com/HVR88/Monochrome-Gaming-Logos)、版 7eb7ddb7246fa5c39b71d5136e7a527bac03fb7f、png/msx.png、blob 49da8dbc396199ede0e604395d55bd0add7b7c92。ドット絵：[libretro](https://github.com/libretro/retroarch-assets)、版 73106363e14e34c08a5854b4cfbc29f184e3b783、xmb/dot-art/png/Microsoft - MSX.png、blob f855b158aa6cc6c418ca00980880394a00213da1。作者は Yoshi-kun、Tatsuya79 と貢献者です。出典とライセンスを同梱し、ロゴの条件は licenses/platform-logos-authors.txt を参照します。商標は権利者に帰属し、独自形状は [MIT](LICENSE) です。
