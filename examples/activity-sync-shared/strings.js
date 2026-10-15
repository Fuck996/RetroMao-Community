(function (global) {
  "use strict";
  const messages = {
    "zh-Hans": {
      favoritesTitle: "收藏同步", recentTitle: "最近游戏记录同步", author: "4NPC · 演示插件", source: "同步网盘", select: "请选择已配置的网盘", sync: "立即同步", cancel: "取消同步",
      favoritesHelp: "首次合并两端收藏；后续同步新增和取消收藏。只匹配同一机种中游戏名及完整 ROM 文件名集合一致的游戏。",
      recentHelp: "保留较新的游玩时间，次数及时长取两端较大值，不累加重复记录。多 ROM 集合作为一个游戏。清空最近记录不会删除另一端历史。",
      privacy: "仅同步本插件的记录文件，不传输 ROM、媒体或存档。关闭页面后任务继续，游戏启动不等待同步。",
      noSources: "尚未配置网盘，请先在复古猫设置中添加连接。", chooseSource: "请在插件页面选择当前有效的网盘后再同步。", invalidCloud: "远端记录格式不正确，已停止同步。",
      readingLibrary: "读取游戏记录", syncing: "同步记录", complete: "同步完成", ready: "选择网盘后即可同步", saving: "正在保存网盘选择…", started: "同步已开始", last: "上次完成",
      local: "合并后记录", updated: "本机更新", uploaded: "更新的机种文件", unmatched: "未匹配游戏", retained: "以下远端记录暂未匹配本机游戏，仍保留在网盘。最多显示 30 项。", skipped: "缺少游戏名或 ROM 文件名，已跳过", empty: "还没有同步记录。",
      WAITING: "等待运行", RUNNING: "同步中", CANCELLING: "正在取消", SUCCEEDED: "同步完成", FAILED: "同步失败", CANCELLED: "已取消，已完成的修改保留", unavailable: "原网盘账号或目录已改变，请重新选择。"
    },
    "zh-Hant": {
      favoritesTitle: "收藏同步", recentTitle: "最近遊戲紀錄同步", author: "4NPC · 示範外掛", source: "同步網路硬碟", select: "請選擇已設定的網路硬碟", sync: "立即同步", cancel: "取消同步",
      favoritesHelp: "首次合併兩端收藏；後續同步新增和取消收藏。只比對同一機種中遊戲名稱及完整 ROM 檔名集合一致的遊戲。",
      recentHelp: "保留較新的遊玩時間，次數與時長取兩端較大值，不累加重複紀錄。多 ROM 集合作為一個遊戲。清空最近紀錄不會刪除另一端歷史。",
      privacy: "僅同步此外掛的紀錄檔，不傳輸 ROM、媒體或存檔。關閉頁面後工作繼續，遊戲啟動不必等待同步。",
      noSources: "尚未設定網路硬碟，請先在復古貓設定中新增連線。", chooseSource: "請先在外掛頁面選擇目前有效的網路硬碟，再進行同步。", invalidCloud: "遠端紀錄格式不正確，已停止同步。",
      readingLibrary: "讀取遊戲紀錄", syncing: "同步紀錄", complete: "同步完成", ready: "選擇網路硬碟後即可同步", saving: "正在儲存網路硬碟選擇…", started: "同步已開始", last: "上次完成",
      local: "合併後紀錄", updated: "本機更新", uploaded: "更新的機種檔案", unmatched: "未比對到的遊戲", retained: "以下遠端紀錄尚未比對到本機遊戲，仍保留於網路硬碟。最多顯示 30 項。", skipped: "缺少遊戲名稱或 ROM 檔名，已略過", empty: "尚無同步紀錄。",
      WAITING: "等待執行", RUNNING: "同步中", CANCELLING: "正在取消", SUCCEEDED: "同步完成", FAILED: "同步失敗", CANCELLED: "已取消，已完成的修改會保留", unavailable: "原網路硬碟帳號或目錄已變更，請重新選擇。"
    },
    en: {
      favoritesTitle: "Favorites sync", recentTitle: "Recent games sync", author: "4NPC · Demo plugin", source: "Cloud storage", select: "Select a configured connection", sync: "Sync now", cancel: "Cancel sync",
      favoritesHelp: "Merge favorites on first sync, then sync additions and removals. Games match only within the same platform, with identical titles and complete ROM filename sets.",
      recentHelp: "Keep the latest play date and the higher play count and duration. Repeated syncs do not add counts. Multiple ROMs remain one game. Clearing recents does not erase the other device’s history.",
      privacy: "Syncs only this plugin’s record files. ROMs, media and saves stay untouched. Tasks continue after this page closes and never delay launching a game.",
      noSources: "No cloud connection configured. Add one in RetroMao settings first.", chooseSource: "Select a valid cloud connection on the plugin page before syncing.", invalidCloud: "Invalid remote record format. Sync stopped.",
      readingLibrary: "Reading game records", syncing: "Syncing records", complete: "Sync complete", ready: "Choose a connection to sync", saving: "Saving connection…", started: "Sync started", last: "Last completed",
      local: "Merged records", updated: "Local updates", uploaded: "Platform files updated", unmatched: "Unmatched games", retained: "These remote records have no matching local game and remain in cloud storage. Showing up to 30.", skipped: "Missing title or ROM filenames; skipped", empty: "No sync history yet.",
      WAITING: "Queued", RUNNING: "Syncing", CANCELLING: "Cancelling", SUCCEEDED: "Sync complete", FAILED: "Sync failed", CANCELLED: "Cancelled; completed changes kept", unavailable: "The previous account or directory changed. Select a connection again."
    },
    ja: {
      favoritesTitle: "お気に入りの同期", recentTitle: "最近遊んだゲームの同期", author: "4NPC · サンプルプラグイン", source: "同期先のクラウド", select: "設定済みの接続を選択", sync: "今すぐ同期", cancel: "同期をキャンセル",
      favoritesHelp: "初回は両端末のお気に入りを統合し、以降は追加と解除を同期します。同じ機種で、ゲーム名と ROM ファイル名の集合がすべて一致するゲームだけを照合します。",
      recentHelp: "最終プレイ日時は新しい方、回数と時間は大きい方を保持し、同期のたびに加算しません。複数 ROM は1つのゲームとして扱います。履歴を消しても他の端末の履歴は削除しません。",
      privacy: "このプラグインの記録ファイルだけを同期します。ROM・メディア・セーブデータは転送しません。画面を閉じても処理を続け、ゲームの起動を妨げません。",
      noSources: "クラウド接続がありません。復古猫の設定で接続を追加してください。", chooseSource: "同期前にプラグイン画面で有効なクラウド接続を選んでください。", invalidCloud: "リモートの記録形式が正しくないため、同期を停止しました。",
      readingLibrary: "ゲーム記録を読み込み中", syncing: "記録を同期中", complete: "同期完了", ready: "接続を選ぶと同期できます", saving: "接続を保存中…", started: "同期を開始しました", last: "前回の完了日時",
      local: "統合後の記録", updated: "端末の更新数", uploaded: "更新した機種ファイル", unmatched: "一致しないゲーム", retained: "端末側に一致するゲームがない記録です。クラウドには保持します。最大30件を表示します。", skipped: "ゲーム名または ROM ファイル名がないためスキップ", empty: "同期履歴はまだありません。",
      WAITING: "待機中", RUNNING: "同期中", CANCELLING: "キャンセル中", SUCCEEDED: "同期完了", FAILED: "同期失敗", CANCELLED: "キャンセル済み・完了した変更は保持", unavailable: "以前のアカウントまたはフォルダーが変更されています。接続を選び直してください。"
    }
  };
  global.activitySyncText = (locale, kind, key) => {
    const tag = (locale || "zh-Hans").toLowerCase();
    const language = tag.startsWith("en") ? "en" : tag.startsWith("ja") ? "ja" : /hant|tw|hk|mo/.test(tag) ? "zh-Hant" : "zh-Hans";
    return messages[language][key === "title" ? kind + "Title" : key === "help" ? kind + "Help" : key];
  };
})(globalThis);
