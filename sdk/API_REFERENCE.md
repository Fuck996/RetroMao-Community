# API 调用手册 / API reference / API リファレンス

[中文](#中文) · [English](#english) · [日本語](#日本語)

[SDK](README.md) · [Types](retromao.d.ts) · [Inventory](api.json) · [Versioning](API_VERSIONING.md) · [Changes](API_CHANGELOG.md) · [All contracts](../docs/INTERFACES.md)

## 中文

本文件由 tools/check_api.py 从 api.json 生成，请编辑清单后运行 --write。当前契约 1.0.0，运行时 API 1，对照宿主 0.9.108。完整字段见 Types；本页覆盖每个公开成员的签名、权限、上下文、参数、返回值、限制与示例。

PAGE = 已启用插件的业务页面；CONFIGURATION = 独立配置页，可在插件禁用时使用；ACTION = tasks.run 发起的后台动作；RESOURCE = 宿主资源解析回调。标记未列出的上下文不属于受支持调用方式。权限须在 plugin.json 声明并授权；storage.sources 的配置页例外见该接口。

调用前等待 retromao.ready。所有 Promise 失败以 Error 拒绝，部分本地同步方法直接抛 Error；没有稳定数字错误码，不按提示文本判断业务状态。插件被禁用／替换、缺权限、输入无效、并发冲突、网络或会话关闭均可能失败。向界面或任务返回真实错误；冲突先重读，禁止静默重试写入。HTTP 非 2xx 是正常响应对象，作者须检查 status。

示例中的 game-demo、media-demo、task-demo 和 example.com 是样本标识，须替换为当前库、任务和已声明主机；含写入的示例会修改数据，应先在独立预览样本运行。每段可独立调用，define 只用于后台入口。SDK 最多同时发送 4 个请求；单条请求／响应最大 512 KiB。后台无 DOM 或 Node.js。__run、__dispose、原生桥和传输协议不是公开调用入口。

| API | Since / 起始 / 初出 | Capability / 能力 / 権限 | Context / 上下文 / 実行場所 |
| --- | --- | --- | --- |
| [`version`](#api-zh-version) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`ready`](#api-zh-ready) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`icons.list`](#api-zh-icons-list) | 0.9.92 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`icons.url`](#api-zh-icons-url) | 0.9.92 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`library.game`](#api-zh-library-game) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`library.games`](#api-zh-library-games) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`library.records`](#api-zh-library-records) | 0.9.91 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`library.edit`](#api-zh-library-edit) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`library.apply`](#api-zh-library-apply) | 0.9.91 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`favorites.list`](#api-zh-favorites-list) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`recent.list`](#api-zh-recent-list) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`favorites.set`](#api-zh-favorites-set) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`recent.edit`](#api-zh-recent-edit) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`media.folders`](#api-zh-media-folders) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`media.assets`](#api-zh-media-assets) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`media.edit`](#api-zh-media-edit) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`index.patch`](#api-zh-index-patch) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`settings.get`](#api-zh-settings-get) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`data.get`](#api-zh-data-get) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`data.patch`](#api-zh-data-patch) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`storage.sources`](#api-zh-storage-sources) | 0.9.91 | STORAGE | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`storage.read`](#api-zh-storage-read) | 0.9.91 | STORAGE | ACTION |
| [`storage.write`](#api-zh-storage-write) | 0.9.91 | STORAGE | ACTION |
| [`http.request`](#api-zh-http-request) | 0.9.90 | NETWORK | PAGE, ACTION, RESOURCE |
| [`tasks.run`](#api-zh-tasks-run) | 0.9.90 | — | PAGE |
| [`tasks.current`](#api-zh-tasks-current) | 0.9.90 | — | PAGE, ACTION, RESOURCE |
| [`tasks.get`](#api-zh-tasks-get) | 0.9.90 | — | PAGE, ACTION, RESOURCE |
| [`tasks.result`](#api-zh-tasks-result) | 0.9.90 | — | PAGE, ACTION, RESOURCE |
| [`tasks.cancel`](#api-zh-tasks-cancel) | 0.9.90 | — | PAGE |
| [`tasks.progress`](#api-zh-tasks-progress) | 0.9.90 | — | ACTION |
| [`tasks.watch`](#api-zh-tasks-watch) | 0.9.90 | — | PAGE |
| [`define`](#api-zh-define) | 0.9.90 | — | ACTION, RESOURCE |

<a id="api-zh-version"></a>

### retromao.version

```typescript
readonly version: 1
```

`LOCAL` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

只读值 1，表示协议主版本；不表示宿主已支持该主版本下的所有后续新增接口。通过 minAppVersion 声明所用功能的最低宿主版本。

```javascript
const apiMajor = retromao.version;
```

<a id="api-zh-ready"></a>

### retromao.ready

```typescript
readonly ready: Promise<{ locale?: string; appLocale?: string; defaultLocale?: string; locales?: readonly string[]; messages?: Readonly<Record<string, string>>; colors?: Record<string, string>; configuring?: boolean }>
```

`session.ready` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

只读 Promise，等待会话就绪并返回环境对象。locale 是插件实际语言，appLocale 是宿主语言，defaultLocale/locales/messages 来自插件清单（这些字段从 0.9.94 提供）；colors 为页面主题变量，configuring 从 0.9.96 标记配置页。类型中可选字段在旧宿主可缺失。连接失败会拒绝。不要从此环境读取账号或系统凭据。

```javascript
const environment = await retromao.ready;
```

<a id="api-zh-icons-list"></a>

### retromao.icons.list

```typescript
list(): Promise<readonly IconName[]>
```

`LOCAL` · `0.9.92` · PAGE / CONFIGURATION / ACTION / RESOURCE

无参数；自动等待 ready，返回只读 IconName 数组。旧宿主不提供图标列表时明确失败，不发额外 RPC。

```javascript
const names = await retromao.icons.list();
```

<a id="api-zh-icons-url"></a>

### retromao.icons.url

```typescript
url(name: IconName): string
```

`LOCAL` · `0.9.92` · PAGE / CONFIGURATION / ACTION / RESOURCE

name 必须来自公共图标列表；等待 ready 后同步返回 `/__retromao/icons/<name>.svg`。本地页面地址不用于远端下载。未就绪或未知名称直接抛 Error；不做网络请求。

```javascript
await retromao.ready;
const url = retromao.icons.url("star");
```

<a id="api-zh-library-game"></a>

### retromao.library.game

```typescript
game(id: string): Promise<Game | null>
```

`library.game` · `0.9.90` · PAGE / ACTION / RESOURCE

id 为本机 Game.id 字符串；返回完整 Game，不存在返回 null。包含资料、媒体引用、收藏、最近记录、隐藏和用户编辑标记，不返回 ROM 正文。缺少 id 或无读权限会失败。

```javascript
const game = await retromao.library.game("game-demo");
```

<a id="api-zh-library-games"></a>

### retromao.library.games

```typescript
games(query?: Query): Promise<Page>
```

`library.games` · `0.9.90` · PAGE / ACTION / RESOURCE

query 可省略；platformId 可筛选机种，collection 为 ALL/FAVORITES/RECENT，默认 ALL；after 默认 null，limit 默认 40，范围 1–200。返回 Page，games 为 Game 数组，next 为下一页游标或 null。把 next 原样作为 after，RECENT 游标必须保留 lastPlayedAt（毫秒）。无效 limit／游标会失败。

```javascript
const page = await retromao.library.games({ limit: 40 });
if (page.next) {
  const nextPage = await retromao.library.games({ limit: 40, after: page.next });
}
```

<a id="api-zh-library-records"></a>

### retromao.library.records

```typescript
records(query?: Query): Promise<RecordPage>
```

`library.records` · `0.9.91` · PAGE / ACTION / RESOURCE

query 可省略；platformId 可筛选机种，collection 为 ALL/FAVORITES/RECENT，默认 ALL；after 默认 null，limit 默认 200，范围 1–200。返回 RecordPage，games 为 GameRecord 数组，next 为下一页游标或 null。把 next 原样作为 after，RECENT 游标必须保留 lastPlayedAt（毫秒）。无效 limit／游标会失败。 records 仅返回 id/platformId/title/romFileNames/favorite/recent，不含路径、媒体或哈希。

```javascript
const page = await retromao.library.records({ limit: 200 });
if (page.next) {
  const nextPage = await retromao.library.records({ limit: 200, after: page.next });
}
```

<a id="api-zh-library-edit"></a>

### retromao.library.edit

```typescript
edit(changes: Edit[], checkpoint?: Record<string, Json>): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

changes 为 1–200 个 Edit，同批 gameId 不可重复；每项至少修改一类字段。mode 默认 EDIT，FILL_MISSING 只补空缺且不覆盖用户编辑。metadata/recent/media/extensions 的 expected 来自刚读取的对象；冲突使整批失败。checkpoint 可省略，为插件私有 JSON 顶层补丁，null 删除键，与本批修改在同一事务提交；跨调用不构成事务。媒体或扩展字段不能修改已移除的本地条目。返回修改后的 Game[]。checkpoint 从 0.9.91 提供。metadata.values 用 MetadataField 枚举键和字符串值，RATING 也传字符串；字段格式由宿主校验。

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const updated = await retromao.library.edit([{
  gameId: game.id,
  metadata: { expected: game.metadata, values: { DESCRIPTION: "Example note" } }
}], { lastGame: game.id });
```

<a id="api-zh-library-apply"></a>

### retromao.library.apply

```typescript
apply(changes: Edit[], checkpoint?: Record<string, Json>): Promise<void>
```

`library.edit` · `0.9.91` · PAGE / ACTION / RESOURCE

changes 为 1–200 个 Edit，同批 gameId 不可重复；每项至少修改一类字段。mode 默认 EDIT，FILL_MISSING 只补空缺且不覆盖用户编辑。metadata/recent/media/extensions 的 expected 来自刚读取的对象；冲突使整批失败。checkpoint 可省略，为插件私有 JSON 顶层补丁，null 删除键，与本批修改在同一事务提交；跨调用不构成事务。媒体或扩展字段不能修改已移除的本地条目。与 edit 共享校验，设置 returnGames:false；Promise<void> 不读取返回值（桥接结果为 null），适合批量同步，避免大响应。

```javascript
await retromao.library.apply([{ gameId: "game-demo", favorite: true }], { lastGame: "game-demo" });
```

<a id="api-zh-favorites-list"></a>

### retromao.favorites.list

```typescript
list(query?: Query): Promise<Page>
```

`library.games` · `0.9.90` · PAGE / ACTION / RESOURCE

参数和 Page 返回与 library.games 相同，limit 默认 40；强制 collection=FAVORITES，即使 query 指定其他集合也会覆盖。游标必须来自同一集合和筛选条件；无效参数失败。

```javascript
const page = await retromao.favorites.list({ limit: 40 });
```

<a id="api-zh-recent-list"></a>

### retromao.recent.list

```typescript
list(query?: Query): Promise<Page>
```

`library.games` · `0.9.90` · PAGE / ACTION / RESOURCE

参数和 Page 返回与 library.games 相同，limit 默认 40；强制 collection=RECENT，即使 query 指定其他集合也会覆盖。游标必须来自同一集合和筛选条件；无效参数失败。

```javascript
const page = await retromao.recent.list({ limit: 40 });
```

<a id="api-zh-favorites-set"></a>

### retromao.favorites.set

```typescript
set(gameId: string, favorite: boolean): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

gameId 为本机 ID，favorite 为显式布尔值；返回 Game[]。通过原 library.edit 修改收藏，重复设置相同值不会反转；游戏不存在或未授权失败。仅设置不需要 LIBRARY_READ，先读取再决定则需读权限。

```javascript
const updated = await retromao.favorites.set("game-demo", true);
```

<a id="api-zh-recent-edit"></a>

### retromao.recent.edit

```typescript
edit(gameId: string, expected: Recent, value: Recent): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

gameId、expected、value 必填；expected 为最近读取的完整 Recent，value 为完整新记录。lastPlayedAt 是非负 Unix 毫秒或 null，playCount 非负整数，importedPlayTimeSeconds 非负秒或 null。返回 Game[]；当前值既非 expected 也非 value 时冲突。不会启动游戏或自动累计次数。

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const updated = await retromao.recent.edit(game.id, game.recent, { ...game.recent, playCount: game.recent.playCount + 1 });
```

<a id="api-zh-media-folders"></a>

### retromao.media.folders

```typescript
folders(platformId?: string): Promise<{ id: string; platformId: string; role: "ROM" | "MEDIA"; name: string }[]>
```

`media.folders` · `0.9.90` · PAGE / ACTION / RESOURCE

可选 platformId；省略时返回全部已配置文件夹。结果为 {id,platformId,role,name}[]，role 为 ROM/MEDIA；不暴露任意设备路径或目录授权。后续 assets 使用这里的 id；无权限失败。

```javascript
const folders = await retromao.media.folders("fc");
```

<a id="api-zh-media-assets"></a>

### retromao.media.assets

```typescript
assets(folderId: string, afterPath?: string | null, limit?: number): Promise<Asset[]>
```

`media.assets` · `0.9.90` · PAGE / ACTION / RESOURCE

folderId 必填；afterPath 默认 null，limit 默认 100，范围 1–200。返回 Asset[]（folderId/path/revision/bytes）；下一页用末项 path 作为 afterPath，空数组结束。只枚举已索引资产，不返回文件正文；文件夹已移除或 limit 无效失败。

```javascript
const assets = await retromao.media.assets("media-demo", null, 100);
if (assets.length) {
  const nextAssets = await retromao.media.assets("media-demo", assets[assets.length - 1].path, 100);
}
```

<a id="api-zh-media-edit"></a>

### retromao.media.edit

```typescript
edit(gameId: string, media: NonNullable<Edit["media"]>): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

gameId 和 media 数组必填，项为 {role,expected,asset}，同批 role 不重复；expected 是当前完整 Media 或 null，asset 是 assets 返回的完整 Asset，null 解除关联。返回 Game[]。机种、介质用途、文件格式和 revision/bytes 均会核对；引用变化或资料已移除失败，物理文件不会被删除。

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const expected = game.media.find(item => item.role === "COVER") || null;
const updated = await retromao.media.edit(game.id, [{ role: "COVER", expected, asset: null }]);
```

<a id="api-zh-index-patch"></a>

### retromao.index.patch

```typescript
patch(gameId: string, extensions: NonNullable<Edit["extensions"]>): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

gameId 和 extensions 映射必填，键为本插件字段名，值为 {expected?,value?}；只写 metadata.extensions[插件ID]。省略 expected 表示原值不存在，省略 value 删除键，显式 null 保存 JSON null。返回 Game[]；当前值既非 expected 也非 value 时冲突，不允许写其他插件命名空间。

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const expected = game.metadata.extensions?.["demo-plugin"]?.note;
const updated = await retromao.index.patch(game.id, { note: { expected, value: "Example note" } });
```

<a id="api-zh-settings-get"></a>

### retromao.settings.get

```typescript
get(): Promise<Record<string, string>>
```

`settings.get` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

无参数，返回本插件配置 Record<string,string>，未保存项使用清单默认值；SECRET 解密后也为字符串，不记录到日志。后台动作和资源回调使用开始时的配置快照。BOOLEAN/NUMBER 也需作者显式解析。该接口只读，配置保存由宿主界面负责；插件已替换或卸载失败。

```javascript
const settings = await retromao.settings.get();
```

<a id="api-zh-data-get"></a>

### retromao.data.get

```typescript
get(): Promise<Record<string, Json>>
```

`data.get` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

无参数；返回本插件私有 JSON 对象，首次为空对象。按来源仓库和插件 ID 隔离，配置页禁用时仍可读。它不是游戏库、账号凭据或自动云同步数据；插件已替换或卸载失败。

```javascript
const data = await retromao.data.get();
```

<a id="api-zh-data-patch"></a>

### retromao.data.patch

```typescript
patch(values: Record<string, Json>): Promise<Record<string, Json>>
```

`data.patch` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

values 为顶层 JSON 补丁：非 null 替换整个键值，null 删除键，不做嵌套深度合并。返回更新后的整个私有对象；与别次调用不是事务，修改游戏库并存 checkpoint 应用 library.edit/apply。配置页禁用时可写；已替换或卸载失败。

```javascript
const updated = await retromao.data.patch({ lastCursor: null, mode: "manual" });
```

<a id="api-zh-storage-sources"></a>

### retromao.storage.sources

```typescript
sources(): Promise<StorageSource[]>
```

`storage.sources` · `0.9.91` · PAGE / CONFIGURATION / ACTION / RESOURCE

无参数，返回已配置 StorageSource[]（id/name/provider/scope），不返回凭据。业务上下文需 STORAGE 授权；CONFIGURATION 只需清单声明 STORAGE，禁用时也能选择连接。scope 绑定账号与插件目录；保存完整来源对象，账号或目录变化后重新选择，不能只保存 id。

```javascript
const sources = await retromao.storage.sources();
```

<a id="api-zh-storage-read"></a>

### retromao.storage.read

```typescript
read(source: StorageSource, key: string): Promise<{ token: string; value: Record<string, Json> | null }>
```

`storage.read` · `0.9.91` · ACTION

source 为 sources 返回的完整对象；key 匹配 [a-zA-Z][a-zA-Z0-9._-]{0,79}\.json，不能含路径。返回 {token,value}，缺失文档 value:null，已有文档必须为 JSON 对象。最多 384 KiB；过大响应还受 512 KiB 消息限制。只在后台动作可调用，账号／目录 scope 变化、坏 JSON、网络失败会拒绝，不转读其他来源。

```javascript
const sources = await retromao.storage.sources();
if (!sources.length) throw new Error("No storage source");
const document = await retromao.storage.read(sources[0], "state.json");
```

<a id="api-zh-storage-write"></a>

### retromao.storage.write

```typescript
write(token: string, value: Record<string, Json>): Promise<void>
```

`storage.write` · `0.9.91` · ACTION

token 必须为同一后台动作最近一次 read 的令牌，value 是 JSON 对象，最大 384 KiB。返回 Promise<void>（桥接为 null）；内容未变不上传，实际写入后令牌失效。再读其他文档会取代旧令牌；不能跨动作保存令牌。账号／目录变化、令牌失效或远端冲突失败，应重新读取并由业务合并，不覆盖其他版本。

```javascript
const sources = await retromao.storage.sources();
if (!sources.length) throw new Error("No storage source");
const document = await retromao.storage.read(sources[0], "state.json");
await retromao.storage.write(document.token, { ...(document.value || {}), example: true });
```

<a id="api-zh-http-request"></a>

### retromao.http.request

```typescript
request(options: { url: string; method?: "GET" | "HEAD" | "POST" | "PUT" | "PATCH" | "DELETE"; headers?: Record<string, string>; body?: string }): Promise<{ status: number; headers: Record<string, string>; body: string }>
```

`http.request` · `0.9.90` · PAGE / ACTION / RESOURCE

options.url 必填 HTTP(S) 地址，method 默认 GET；支持 GET/HEAD/POST/PUT/PATCH/DELETE。headers 为字符串映射，body 为可选文本；POST/PUT/PATCH 无 body 发空正文。主机须匹配 networkHosts（非默认端口含 host:port）。返回 {status,headers,body}，headers 为字符串映射，body 为 UTF-8 文本；不跟随重定向。非 2xx 不自动抛错；网络、主机未声明、正文超过 256 KiB 或总消息过大失败，不提供流或二进制。

```javascript
const response = await retromao.http.request({ url: "https://example.com/api/state" });
if (response.status < 200 || response.status >= 300) {
  throw new Error(`HTTP ${response.status}`);
}
const value = JSON.parse(response.body);
```

<a id="api-zh-tasks-run"></a>

### retromao.tasks.run

```typescript
run(action: string, arguments_?: Record<string, Json>): Promise<Task>
```

`tasks.run` · `0.9.90` · PAGE

action 是清单 actions 与 define.actions 中声明的同一 ID；arguments_ 默认空 JSON 对象。返回新 Task，不是动作结果；本插件只能有一个活动任务。未声明动作或前一任务未结束时请求失败；配置在执行时校验，无效则任务进入 FAILED。仅业务页面可发起，不从后台递归创建任务。执行使用版本／配置快照，新任务替换上一次任务记录并清除旧结果。

```javascript
const task = await retromao.tasks.run("run", { dryRun: true });
```

<a id="api-zh-tasks-current"></a>

### retromao.tasks.current

```typescript
current(): Promise<Task | null>
```

`tasks.current` · `0.9.90` · PAGE / ACTION / RESOURCE

无参数；返回本插件最近保留的 Task 或 null，包括已成功／失败／取消的任务，并非只返回正在运行的任务。用于页面重开后接续状态；宿主只保留一个记录，不是任务历史列表。插件禁用或替换后调用失败。

```javascript
const task = await retromao.tasks.current();
```

<a id="api-zh-tasks-get"></a>

### retromao.tasks.get

```typescript
get(id: string): Promise<Task>
```

`tasks.get` · `0.9.90` · PAGE / ACTION / RESOURCE

id 为本插件仍保留的任务 ID，返回 Task；旧任务被新任务替换、ID 不存在或属于其他插件均失败。Task 时间为 Unix 毫秒，completed 为非负计数，total 为非负总数或 null，message 为业务状态说明；不要把消息当错误码。

```javascript
const task = await retromao.tasks.get("task-demo");
```

<a id="api-zh-tasks-result"></a>

### retromao.tasks.result

```typescript
result(id: string): Promise<Json>
```

`tasks.result` · `0.9.90` · PAGE / ACTION / RESOURCE

id 为本插件保留的任务 ID；仅 SUCCEEDED 可读取，返回动作返回的 Json，无返回值为 null。尚未成功、任务被替换或不属于本插件失败；不要依赖旧任务结果长期保存，必要数据写本插件 data 或正式库接口。

```javascript
const task = await retromao.tasks.get("task-demo");
if (task.state === "SUCCEEDED") {
  const result = await retromao.tasks.result(task.id);
}
```

<a id="api-zh-tasks-cancel"></a>

### retromao.tasks.cancel

```typescript
cancel(id: string): Promise<void>
```

`tasks.cancel` · `0.9.90` · PAGE

id 为本插件当前保留的任务；返回 Promise<void>，请求取消活动任务，已经结束不重复执行取消。取消保留已成功提交的批次，不回滚全部业务。其他插件或被替换 ID 失败。状态可能经历 CANCELLING，再以 current/get/watch 核对 CANCELLED 等最终状态；后台动作不能自行调用取消入口。

```javascript
await retromao.tasks.cancel("task-demo");
const task = await retromao.tasks.current();
```

<a id="api-zh-tasks-progress"></a>

### retromao.tasks.progress

```typescript
progress(completed: number, total?: number | null, message?: string): Promise<void>
```

`tasks.progress` · `0.9.90` · ACTION

completed 为非负整数，total 默认 null（未知）或不小于 completed 的整数，message 默认空字符串；返回 Promise<void>。仅运行中的后台动作有进度回调；页面、资源回调、已停止任务或无效计数失败。宿主节流保存约 300ms，完成计数会保存，不用它代替业务 checkpoint。

```javascript
await retromao.tasks.progress(1, 2, "Processing");
```

<a id="api-zh-tasks-watch"></a>

### retromao.tasks.watch

```typescript
watch(id: string, callback: (task: Task) => void): () => void
```

`LOCAL` · `0.9.90` · PAGE

id 与 callback 必填；同步返回无参数 unsubscribe 函数，不是 Promise。只监听宿主推送的同 ID Task；若 SDK 缓存过该任务，注册时立即回调；不主动请求状态，先用 current/get。页面销毁释放订阅，后台任务继续；不会保留完整历史。回调中自行处理异常并更新内容区，不阻断其他订阅。

```javascript
const task = await retromao.tasks.current();
if (task) {
  const stop = retromao.tasks.watch(task.id, value => { console.log(value.state); });
  stop();
}
```

<a id="api-zh-define"></a>

### retromao.define

```typescript
define(definition: { actions?: Record<string, (arguments_: Record<string, Json>) => Json | void | Promise<Json | void>>;
      resources?: Record<string, (arguments_: { games: ResourceGame[] }) => ResourceResolution[] | Promise<ResourceResolution[]>> }): void
```

`LOCAL` · `0.9.90` · ACTION / RESOURCE

后台入口顶层只注册一次 {actions?,resources?}，同步返回 void；重复注册直接抛 Error。actions 的键与清单 actions.id 一致，接收 Json 参数对象，返回 Json/void 或其 Promise；由宿主运行并保存任务结果。resources 从 0.9.98 提供，需 ROM_RESOURCES 及对应 resourceProviders，接收 {games:[{gameId,romNames}]}，返回 ResourceResolution[]；每个输入游戏恰好一项，路径为授权根下安全相对路径，不执行传输。回调抛错使动作／解析失败。不要调用内部 __run。

```javascript
retromao.define({
  actions: { run: async arguments_ => ({ dryRun: arguments_.dryRun === true }) }
});
```

## English

Generated from api.json by tools/check_api.py; edit the inventory and run --write. Contract 1.0.0, runtime API 1, checked against host 0.9.108. Types defines every data field; this reference covers each public member's signature, grants, contexts, arguments, results, constraints and example.

PAGE = enabled plugin business page; CONFIGURATION = dedicated configuration page, also available while disabled; ACTION = background action started with tasks.run; RESOURCE = host resource-resolution callback. Unlisted contexts are unsupported usage. Declare grants in plugin.json and obtain approval; see storage.sources for its configuration-page exception.

Await retromao.ready first. Promise failures reject with Error; local synchronous methods can throw Error. There are no stable numeric error codes; do not branch on message text. Disabled/replaced plugins, missing grants, invalid input, conflicts, network and closed sessions can fail. Expose the error in the page/task; reread conflicts before a new decision and never silently retry writes. Non-2xx HTTP returns a response object: check status.

game-demo, media-demo, task-demo and example.com are fixture identifiers: replace them with current library/task IDs and declared hosts. Write examples modify data; try them in fixture preview first. Each snippet stands alone; define belongs in the background entry. SDK concurrency is 4; each request/response is limited to 512 KiB. Background code has no DOM or Node.js. __run, __dispose, native bridges and transport messages are not public entry points.

| API | Since / 起始 / 初出 | Capability / 能力 / 権限 | Context / 上下文 / 実行場所 |
| --- | --- | --- | --- |
| [`version`](#api-en-version) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`ready`](#api-en-ready) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`icons.list`](#api-en-icons-list) | 0.9.92 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`icons.url`](#api-en-icons-url) | 0.9.92 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`library.game`](#api-en-library-game) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`library.games`](#api-en-library-games) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`library.records`](#api-en-library-records) | 0.9.91 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`library.edit`](#api-en-library-edit) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`library.apply`](#api-en-library-apply) | 0.9.91 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`favorites.list`](#api-en-favorites-list) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`recent.list`](#api-en-recent-list) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`favorites.set`](#api-en-favorites-set) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`recent.edit`](#api-en-recent-edit) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`media.folders`](#api-en-media-folders) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`media.assets`](#api-en-media-assets) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`media.edit`](#api-en-media-edit) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`index.patch`](#api-en-index-patch) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`settings.get`](#api-en-settings-get) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`data.get`](#api-en-data-get) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`data.patch`](#api-en-data-patch) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`storage.sources`](#api-en-storage-sources) | 0.9.91 | STORAGE | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`storage.read`](#api-en-storage-read) | 0.9.91 | STORAGE | ACTION |
| [`storage.write`](#api-en-storage-write) | 0.9.91 | STORAGE | ACTION |
| [`http.request`](#api-en-http-request) | 0.9.90 | NETWORK | PAGE, ACTION, RESOURCE |
| [`tasks.run`](#api-en-tasks-run) | 0.9.90 | — | PAGE |
| [`tasks.current`](#api-en-tasks-current) | 0.9.90 | — | PAGE, ACTION, RESOURCE |
| [`tasks.get`](#api-en-tasks-get) | 0.9.90 | — | PAGE, ACTION, RESOURCE |
| [`tasks.result`](#api-en-tasks-result) | 0.9.90 | — | PAGE, ACTION, RESOURCE |
| [`tasks.cancel`](#api-en-tasks-cancel) | 0.9.90 | — | PAGE |
| [`tasks.progress`](#api-en-tasks-progress) | 0.9.90 | — | ACTION |
| [`tasks.watch`](#api-en-tasks-watch) | 0.9.90 | — | PAGE |
| [`define`](#api-en-define) | 0.9.90 | — | ACTION, RESOURCE |

<a id="api-en-version"></a>

### retromao.version

```typescript
readonly version: 1
```

`LOCAL` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

Readonly value 1 identifies the protocol major. It does not imply support for every later addition in that major. Set minAppVersion for the features you use.

```javascript
const apiMajor = retromao.version;
```

<a id="api-en-ready"></a>

### retromao.ready

```typescript
readonly ready: Promise<{ locale?: string; appLocale?: string; defaultLocale?: string; locales?: readonly string[]; messages?: Readonly<Record<string, string>>; colors?: Record<string, string>; configuring?: boolean }>
```

`session.ready` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

Readonly Promise resolving to the session environment. locale is the selected plugin locale; appLocale is the app locale; defaultLocale/locales/messages come from the manifest (these fields require 0.9.94). colors contains page theme variables; configuring marks configuration pages from 0.9.96. Optional fields may be absent on older hosts. Bridge failure rejects. This environment does not expose account/system credentials.

```javascript
const environment = await retromao.ready;
```

<a id="api-en-icons-list"></a>

### retromao.icons.list

```typescript
list(): Promise<readonly IconName[]>
```

`LOCAL` · `0.9.92` · PAGE / CONFIGURATION / ACTION / RESOURCE

No arguments. Awaits ready and returns a readonly IconName array without another RPC. Rejects when the host does not provide public icons.

```javascript
const names = await retromao.icons.list();
```

<a id="api-en-icons-url"></a>

### retromao.icons.url

```typescript
url(name: IconName): string
```

`LOCAL` · `0.9.92` · PAGE / CONFIGURATION / ACTION / RESOURCE

name must be a public icon name. After ready, synchronously returns `/__retromao/icons/<name>.svg` for local page use, not remote download. Throws Error before readiness or for unknown names; no network request.

```javascript
await retromao.ready;
const url = retromao.icons.url("star");
```

<a id="api-en-library-game"></a>

### retromao.library.game

```typescript
game(id: string): Promise<Game | null>
```

`library.game` · `0.9.90` · PAGE / ACTION / RESOURCE

id is a local Game.id string. Returns the complete Game or null if absent: metadata, media references, favorite/recent state, visibility and user-edit markers, not ROM bodies. Invalid input or missing read grants can reject.

```javascript
const game = await retromao.library.game("game-demo");
```

<a id="api-en-library-games"></a>

### retromao.library.games

```typescript
games(query?: Query): Promise<Page>
```

`library.games` · `0.9.90` · PAGE / ACTION / RESOURCE

Optional query filters by platformId and collection (ALL/FAVORITES/RECENT, default ALL). after defaults to null; limit defaults to 40, allowed 1–200. Returns Page with a Game games array and next cursor or null. Pass next unchanged as after; RECENT cursors must retain lastPlayedAt (milliseconds). Invalid limits/cursors reject.

```javascript
const page = await retromao.library.games({ limit: 40 });
if (page.next) {
  const nextPage = await retromao.library.games({ limit: 40, after: page.next });
}
```

<a id="api-en-library-records"></a>

### retromao.library.records

```typescript
records(query?: Query): Promise<RecordPage>
```

`library.records` · `0.9.91` · PAGE / ACTION / RESOURCE

Optional query filters by platformId and collection (ALL/FAVORITES/RECENT, default ALL). after defaults to null; limit defaults to 200, allowed 1–200. Returns RecordPage with a GameRecord games array and next cursor or null. Pass next unchanged as after; RECENT cursors must retain lastPlayedAt (milliseconds). Invalid limits/cursors reject. records only includes id/platformId/title/romFileNames/favorite/recent, excluding paths, media and hashes.

```javascript
const page = await retromao.library.records({ limit: 200 });
if (page.next) {
  const nextPage = await retromao.library.records({ limit: 200, after: page.next });
}
```

<a id="api-en-library-edit"></a>

### retromao.library.edit

```typescript
edit(changes: Edit[], checkpoint?: Record<string, Json>): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

changes contains 1–200 Edit entries with distinct gameId values and at least one changed field each. mode defaults to EDIT; FILL_MISSING only fills eligible missing fields without overriding user edits. Use freshly read metadata/recent/media/extensions expected values; a conflict fails the whole batch. Optional checkpoint is a top-level private-data patch (null deletes keys), committed atomically with this batch, not across calls. Media/extension edits reject removed local entries. Returns updated Game[]. checkpoint requires 0.9.91. metadata.values uses MetadataField enum keys and string values, including RATING; the host validates field formats.

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const updated = await retromao.library.edit([{
  gameId: game.id,
  metadata: { expected: game.metadata, values: { DESCRIPTION: "Example note" } }
}], { lastGame: game.id });
```

<a id="api-en-library-apply"></a>

### retromao.library.apply

```typescript
apply(changes: Edit[], checkpoint?: Record<string, Json>): Promise<void>
```

`library.edit` · `0.9.91` · PAGE / ACTION / RESOURCE

changes contains 1–200 Edit entries with distinct gameId values and at least one changed field each. mode defaults to EDIT; FILL_MISSING only fills eligible missing fields without overriding user edits. Use freshly read metadata/recent/media/extensions expected values; a conflict fails the whole batch. Optional checkpoint is a top-level private-data patch (null deletes keys), committed atomically with this batch, not across calls. Media/extension edits reject removed local entries. Uses the same edit validation with returnGames:false. Treat the Promise<void> result as absent (the bridge sends null), suitable for batch sync without large responses.

```javascript
await retromao.library.apply([{ gameId: "game-demo", favorite: true }], { lastGame: "game-demo" });
```

<a id="api-en-favorites-list"></a>

### retromao.favorites.list

```typescript
list(query?: Query): Promise<Page>
```

`library.games` · `0.9.90` · PAGE / ACTION / RESOURCE

Same query parameters and Page result as library.games, with limit 40. Forces collection=FAVORITES, overriding any query collection. Keep cursors within the same collection/filter. Invalid parameters reject.

```javascript
const page = await retromao.favorites.list({ limit: 40 });
```

<a id="api-en-recent-list"></a>

### retromao.recent.list

```typescript
list(query?: Query): Promise<Page>
```

`library.games` · `0.9.90` · PAGE / ACTION / RESOURCE

Same query parameters and Page result as library.games, with limit 40. Forces collection=RECENT, overriding any query collection. Keep cursors within the same collection/filter. Invalid parameters reject.

```javascript
const page = await retromao.recent.list({ limit: 40 });
```

<a id="api-en-favorites-set"></a>

### retromao.favorites.set

```typescript
set(gameId: string, favorite: boolean): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

gameId is local; favorite is an explicit boolean. Returns Game[] through library.edit. Repeating the same value never toggles it. Missing games/grants reject. Setting alone needs no LIBRARY_READ; reading before deciding does.

```javascript
const updated = await retromao.favorites.set("game-demo", true);
```

<a id="api-en-recent-edit"></a>

### retromao.recent.edit

```typescript
edit(gameId: string, expected: Recent, value: Recent): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

Requires gameId, the freshly read complete expected Recent and complete new value. lastPlayedAt is nonnegative Unix milliseconds or null; playCount is a nonnegative integer; importedPlayTimeSeconds is nonnegative seconds or null. Returns Game[]. Conflicts when current matches neither expected nor value. Does not launch a game or increment counts automatically.

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const updated = await retromao.recent.edit(game.id, game.recent, { ...game.recent, playCount: game.recent.playCount + 1 });
```

<a id="api-en-media-folders"></a>

### retromao.media.folders

```typescript
folders(platformId?: string): Promise<{ id: string; platformId: string; role: "ROM" | "MEDIA"; name: string }[]>
```

`media.folders` · `0.9.90` · PAGE / ACTION / RESOURCE

Optional platformId; omission lists all configured folders. Returns {id,platformId,role,name}[] with role ROM/MEDIA, not arbitrary device paths or directory grants. Use these IDs for assets. Missing grants reject.

```javascript
const folders = await retromao.media.folders("fc");
```

<a id="api-en-media-assets"></a>

### retromao.media.assets

```typescript
assets(folderId: string, afterPath?: string | null, limit?: number): Promise<Asset[]>
```

`media.assets` · `0.9.90` · PAGE / ACTION / RESOURCE

Requires folderId; afterPath defaults to null; limit defaults to 100, allowed 1–200. Returns Asset[] with folderId/path/revision/bytes. Continue with the last path as afterPath until an empty array. Enumerates indexed assets, not file bodies. Removed folders and invalid limits reject.

```javascript
const assets = await retromao.media.assets("media-demo", null, 100);
if (assets.length) {
  const nextAssets = await retromao.media.assets("media-demo", assets[assets.length - 1].path, 100);
}
```

<a id="api-en-media-edit"></a>

### retromao.media.edit

```typescript
edit(gameId: string, media: NonNullable<Edit["media"]>): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

Requires gameId and media entries {role,expected,asset}, with distinct roles. expected is the current complete Media or null; asset is a complete indexed Asset, or null to unlink. Returns Game[]. Platform, medium role, format and revision/bytes are validated. Changed references or removed local entries reject. Unlinking does not delete files.

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const expected = game.media.find(item => item.role === "COVER") || null;
const updated = await retromao.media.edit(game.id, [{ role: "COVER", expected, asset: null }]);
```

<a id="api-en-index-patch"></a>

### retromao.index.patch

```typescript
patch(gameId: string, extensions: NonNullable<Edit["extensions"]>): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

Requires gameId and extensions mapping own field names to {expected?,value?}. Only writes metadata.extensions[pluginID]. Omitted expected means absent; omitted value deletes; explicit null stores JSON null. Returns Game[]. Conflicts if current matches neither expected nor value; other plugin namespaces cannot be written.

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const expected = game.metadata.extensions?.["demo-plugin"]?.note;
const updated = await retromao.index.patch(game.id, { note: { expected, value: "Example note" } });
```

<a id="api-en-settings-get"></a>

### retromao.settings.get

```typescript
get(): Promise<Record<string, string>>
```

`settings.get` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

No arguments. Returns this plugin's Record<string,string> settings, using manifest defaults for unsaved values. SECRET values are decrypted strings: do not log them. Actions/resolvers use the start-time snapshot. Parse BOOLEAN/NUMBER explicitly. Read-only; host UI owns saving settings. Replaced/uninstalled plugins reject.

```javascript
const settings = await retromao.settings.get();
```

<a id="api-en-data-get"></a>

### retromao.data.get

```typescript
get(): Promise<Record<string, Json>>
```

`data.get` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

No arguments. Returns the plugin's private JSON object, initially empty, isolated by repository origin and plugin ID. Configuration pages can read while disabled. This is not the game database, account credentials or automatically cloud-synced data. Replaced/uninstalled plugins reject.

```javascript
const data = await retromao.data.get();
```

<a id="api-en-data-patch"></a>

### retromao.data.patch

```typescript
patch(values: Record<string, Json>): Promise<Record<string, Json>>
```

`data.patch` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

values is a top-level JSON patch: non-null replaces the entire value; null deletes the key; no recursive merge. Returns the updated whole private object. Separate calls are not transactional; use library.edit/apply checkpoint for atomic library/data changes. Configuration pages can write while disabled. Replaced/uninstalled plugins reject.

```javascript
const updated = await retromao.data.patch({ lastCursor: null, mode: "manual" });
```

<a id="api-en-storage-sources"></a>

### retromao.storage.sources

```typescript
sources(): Promise<StorageSource[]>
```

`storage.sources` · `0.9.91` · PAGE / CONFIGURATION / ACTION / RESOURCE

No arguments. Returns configured StorageSource[] (id/name/provider/scope), without credentials. Business contexts require a STORAGE grant; CONFIGURATION only requires the STORAGE declaration and works while disabled. scope binds account and plugin directory. Save the complete source, not just id; reselect after account/directory changes.

```javascript
const sources = await retromao.storage.sources();
```

<a id="api-en-storage-read"></a>

### retromao.storage.read

```typescript
read(source: StorageSource, key: string): Promise<{ token: string; value: Record<string, Json> | null }>
```

`storage.read` · `0.9.91` · ACTION

source is the complete object from sources. key matches [a-zA-Z][a-zA-Z0-9._-]{0,79}\.json, without paths. Returns {token,value}; missing documents have value:null, existing documents must be JSON objects. Document limit is 384 KiB, also subject to the 512 KiB message limit. Background actions only; scope changes, invalid JSON and network failures reject without switching sources.

```javascript
const sources = await retromao.storage.sources();
if (!sources.length) throw new Error("No storage source");
const document = await retromao.storage.read(sources[0], "state.json");
```

<a id="api-en-storage-write"></a>

### retromao.storage.write

```typescript
write(token: string, value: Record<string, Json>): Promise<void>
```

`storage.write` · `0.9.91` · ACTION

token must come from the latest read in the same background action. value is a JSON object up to 384 KiB. Returns Promise<void> (bridge null). Unchanged content is not uploaded; an actual write invalidates the token. Reading another document replaces it; never persist tokens across actions. Changed account/directory, invalid tokens or remote conflicts reject. Reread and merge deliberately rather than overwrite another version.

```javascript
const sources = await retromao.storage.sources();
if (!sources.length) throw new Error("No storage source");
const document = await retromao.storage.read(sources[0], "state.json");
await retromao.storage.write(document.token, { ...(document.value || {}), example: true });
```

<a id="api-en-http-request"></a>

### retromao.http.request

```typescript
request(options: { url: string; method?: "GET" | "HEAD" | "POST" | "PUT" | "PATCH" | "DELETE"; headers?: Record<string, string>; body?: string }): Promise<{ status: number; headers: Record<string, string>; body: string }>
```

`http.request` · `0.9.90` · PAGE / ACTION / RESOURCE

options.url is required HTTP(S); method defaults to GET. Supports GET/HEAD/POST/PUT/PATCH/DELETE, string headers and optional text body; POST/PUT/PATCH without body sends empty content. networkHosts must allow the host (include host:port for non-default ports). Returns {status,headers,body}, string headers and UTF-8 text body, without redirects. Non-2xx does not automatically throw. Network errors, undeclared hosts, body over 256 KiB or oversized messages reject. No streaming/binary API.

```javascript
const response = await retromao.http.request({ url: "https://example.com/api/state" });
if (response.status < 200 || response.status >= 300) {
  throw new Error(`HTTP ${response.status}`);
}
const value = JSON.parse(response.body);
```

<a id="api-en-tasks-run"></a>

### retromao.tasks.run

```typescript
run(action: string, arguments_?: Record<string, Json>): Promise<Task>
```

`tasks.run` · `0.9.90` · PAGE

action must match manifest actions and define.actions. arguments_ defaults to an empty JSON object. Returns a new Task, not the action result; only one active task per plugin. Unknown actions or active predecessors reject the request. Settings are validated during execution; invalid settings make the task FAILED. Business pages only; no recursive background task creation. Execution uses version/settings snapshots. A new task replaces the last record and clears its result.

```javascript
const task = await retromao.tasks.run("run", { dryRun: true });
```

<a id="api-en-tasks-current"></a>

### retromao.tasks.current

```typescript
current(): Promise<Task | null>
```

`tasks.current` · `0.9.90` · PAGE / ACTION / RESOURCE

No arguments. Returns the plugin's retained latest Task or null, including terminal tasks, not just active ones. Use when reopening a page. The host retains one record, not task history. Disabled/replaced plugins reject.

```javascript
const task = await retromao.tasks.current();
```

<a id="api-en-tasks-get"></a>

### retromao.tasks.get

```typescript
get(id: string): Promise<Task>
```

`tasks.get` · `0.9.90` · PAGE / ACTION / RESOURCE

id must identify this plugin's retained task. Returns Task; replaced IDs, missing IDs and other plugin IDs reject. Task times are Unix milliseconds; completed is a nonnegative count; total is a nonnegative total or null; message is human-readable state, not an error code.

```javascript
const task = await retromao.tasks.get("task-demo");
```

<a id="api-en-tasks-result"></a>

### retromao.tasks.result

```typescript
result(id: string): Promise<Json>
```

`tasks.result` · `0.9.90` · PAGE / ACTION / RESOURCE

id is the retained own task. Only SUCCEEDED tasks return the action's Json result; no returned value becomes null. Non-success, replaced tasks and other owners reject. Results are not long-term storage; persist required data through data or library APIs.

```javascript
const task = await retromao.tasks.get("task-demo");
if (task.state === "SUCCEEDED") {
  const result = await retromao.tasks.result(task.id);
}
```

<a id="api-en-tasks-cancel"></a>

### retromao.tasks.cancel

```typescript
cancel(id: string): Promise<void>
```

`tasks.cancel` · `0.9.90` · PAGE

id is the retained own task. Returns Promise<void>, requesting cancellation if active; terminal tasks need no cancellation. Committed batches remain, without whole-action rollback. Other owners/replaced IDs reject. State can pass through CANCELLING; use current/get/watch to confirm a terminal state such as CANCELLED. Background actions cannot call this entry.

```javascript
await retromao.tasks.cancel("task-demo");
const task = await retromao.tasks.current();
```

<a id="api-en-tasks-progress"></a>

### retromao.tasks.progress

```typescript
progress(completed: number, total?: number | null, message?: string): Promise<void>
```

`tasks.progress` · `0.9.90` · ACTION

completed is a nonnegative integer; total defaults to null (unknown), otherwise an integer at least completed; message defaults to empty. Returns Promise<void>. Only running background actions have a progress callback. Pages, resolvers, stopped tasks and invalid counts reject. Host persistence is throttled around 300ms, with final counts saved; progress is not a business checkpoint.

```javascript
await retromao.tasks.progress(1, 2, "Processing");
```

<a id="api-en-tasks-watch"></a>

### retromao.tasks.watch

```typescript
watch(id: string, callback: (task: Task) => void): () => void
```

`LOCAL` · `0.9.90` · PAGE

Requires id and callback. Synchronously returns an unsubscribe function, not a Promise. Receives pushed Task updates for that ID, immediately replaying an SDK-cached match if present. It does not fetch state: use current/get first. Release subscriptions on page exit; background work continues. No complete event history. Handle callback failures in your page so other listeners are not interrupted.

```javascript
const task = await retromao.tasks.current();
if (task) {
  const stop = retromao.tasks.watch(task.id, value => { console.log(value.state); });
  stop();
}
```

<a id="api-en-define"></a>

### retromao.define

```typescript
define(definition: { actions?: Record<string, (arguments_: Record<string, Json>) => Json | void | Promise<Json | void>>;
      resources?: Record<string, (arguments_: { games: ResourceGame[] }) => ResourceResolution[] | Promise<ResourceResolution[]>> }): void
```

`LOCAL` · `0.9.90` · ACTION / RESOURCE

Register {actions?,resources?} once at the background entry's top level; returns void synchronously and throws on duplicate registration. actions keys match manifest actions.id, receive a Json argument object and return Json/void or a Promise; the host runs them and stores task results. resources requires 0.9.98, ROM_RESOURCES and matching resourceProviders; input {games:[{gameId,romNames}]} returns ResourceResolution[], exactly one per input game, with safe relative paths under the authorized root. It does not transfer files. Thrown callback errors fail execution/resolution. Never call internal __run.

```javascript
retromao.define({
  actions: { run: async arguments_ => ({ dryRun: arguments_.dryRun === true }) }
});
```

## 日本語

api.json から tools/check_api.py で生成します。一覧を編集して --write を実行してください。契約 1.0.0、実行 API 1、確認対象ホスト 0.9.108。全データ項目は Types を参照してください。各公開メンバーのシグネチャ、権限、実行場所、引数、戻り値、制限、例を記載します。

PAGE は有効なプラグインの業務ページ、CONFIGURATION は無効時にも利用できる独立設定ページ、ACTION は tasks.run のバックグラウンド処理、RESOURCE はホストのリソース解析コールバックです。記載のない場所での呼び出しはサポート対象外です。plugin.json で権限を宣言して許可を得てください。storage.sources の設定ページでの例外は個別説明を参照してください。

最初に retromao.ready を待ちます。Promise の失敗は Error で拒否され、ローカル同期メソッドは Error を送出する場合があります。安定した数値エラーコードはありません。メッセージ文字列で状態を判定しないでください。無効化・置換、権限不足、不正入力、競合、通信、セッション終了で失敗します。画面やタスクで原因を表示し、競合は再取得して判断してください。書き込みを黙って再試行してはいけません。HTTP の非 2xx は応答オブジェクトなので status を確認します。

game-demo、media-demo、task-demo、example.com はサンプルです。現在のライブラリ・タスク ID と宣言したホストに置き換えてください。書き込み例はデータを変更するため、まず独立プレビューのサンプルで試してください。各例は独立し、define はバックグラウンド入口に置きます。同時要求は最大 4 件、要求・応答は各 512 KiB です。バックグラウンドに DOM や Node.js はありません。__run、__dispose、ネイティブブリッジ、転送メッセージは公開入口ではありません。

| API | Since / 起始 / 初出 | Capability / 能力 / 権限 | Context / 上下文 / 実行場所 |
| --- | --- | --- | --- |
| [`version`](#api-ja-version) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`ready`](#api-ja-ready) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`icons.list`](#api-ja-icons-list) | 0.9.92 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`icons.url`](#api-ja-icons-url) | 0.9.92 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`library.game`](#api-ja-library-game) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`library.games`](#api-ja-library-games) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`library.records`](#api-ja-library-records) | 0.9.91 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`library.edit`](#api-ja-library-edit) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`library.apply`](#api-ja-library-apply) | 0.9.91 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`favorites.list`](#api-ja-favorites-list) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`recent.list`](#api-ja-recent-list) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`favorites.set`](#api-ja-favorites-set) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`recent.edit`](#api-ja-recent-edit) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`media.folders`](#api-ja-media-folders) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`media.assets`](#api-ja-media-assets) | 0.9.90 | LIBRARY_READ | PAGE, ACTION, RESOURCE |
| [`media.edit`](#api-ja-media-edit) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`index.patch`](#api-ja-index-patch) | 0.9.90 | LIBRARY_WRITE | PAGE, ACTION, RESOURCE |
| [`settings.get`](#api-ja-settings-get) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`data.get`](#api-ja-data-get) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`data.patch`](#api-ja-data-patch) | 0.9.90 | — | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`storage.sources`](#api-ja-storage-sources) | 0.9.91 | STORAGE | PAGE, CONFIGURATION, ACTION, RESOURCE |
| [`storage.read`](#api-ja-storage-read) | 0.9.91 | STORAGE | ACTION |
| [`storage.write`](#api-ja-storage-write) | 0.9.91 | STORAGE | ACTION |
| [`http.request`](#api-ja-http-request) | 0.9.90 | NETWORK | PAGE, ACTION, RESOURCE |
| [`tasks.run`](#api-ja-tasks-run) | 0.9.90 | — | PAGE |
| [`tasks.current`](#api-ja-tasks-current) | 0.9.90 | — | PAGE, ACTION, RESOURCE |
| [`tasks.get`](#api-ja-tasks-get) | 0.9.90 | — | PAGE, ACTION, RESOURCE |
| [`tasks.result`](#api-ja-tasks-result) | 0.9.90 | — | PAGE, ACTION, RESOURCE |
| [`tasks.cancel`](#api-ja-tasks-cancel) | 0.9.90 | — | PAGE |
| [`tasks.progress`](#api-ja-tasks-progress) | 0.9.90 | — | ACTION |
| [`tasks.watch`](#api-ja-tasks-watch) | 0.9.90 | — | PAGE |
| [`define`](#api-ja-define) | 0.9.90 | — | ACTION, RESOURCE |

<a id="api-ja-version"></a>

### retromao.version

```typescript
readonly version: 1
```

`LOCAL` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

読み取り専用の値 1 はプロトコルのメジャー版です。同じメジャー版で後から追加された全機能の対応を意味しません。使用する機能に応じて minAppVersion を指定します。

```javascript
const apiMajor = retromao.version;
```

<a id="api-ja-ready"></a>

### retromao.ready

```typescript
readonly ready: Promise<{ locale?: string; appLocale?: string; defaultLocale?: string; locales?: readonly string[]; messages?: Readonly<Record<string, string>>; colors?: Record<string, string>; configuring?: boolean }>
```

`session.ready` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

セッションの準備完了を待ち、環境を返す読み取り専用 Promise です。locale はプラグインの選択言語、appLocale はホスト言語、defaultLocale/locales/messages はマニフェスト由来で 0.9.94 以降です。colors はページのテーマ変数、configuring は 0.9.96 以降の設定ページ判定です。任意項目は旧ホストに存在しない場合があります。接続失敗は拒否されます。アカウントやシステムの認証情報は取得できません。

```javascript
const environment = await retromao.ready;
```

<a id="api-ja-icons-list"></a>

### retromao.icons.list

```typescript
list(): Promise<readonly IconName[]>
```

`LOCAL` · `0.9.92` · PAGE / CONFIGURATION / ACTION / RESOURCE

引数はありません。ready を待ち、追加 RPC なしで読み取り専用 IconName 配列を返します。公開アイコンに未対応のホストでは失敗します。

```javascript
const names = await retromao.icons.list();
```

<a id="api-ja-icons-url"></a>

### retromao.icons.url

```typescript
url(name: IconName): string
```

`LOCAL` · `0.9.92` · PAGE / CONFIGURATION / ACTION / RESOURCE

name は公開アイコン名です。ready の後で `/__retromao/icons/<name>.svg` を同期的に返します。ローカルページ用で、外部ダウンロード用ではありません。準備前や不明な名前は Error となり、通信しません。

```javascript
await retromao.ready;
const url = retromao.icons.url("star");
```

<a id="api-ja-library-game"></a>

### retromao.library.game

```typescript
game(id: string): Promise<Game | null>
```

`library.game` · `0.9.90` · PAGE / ACTION / RESOURCE

id は端末内の Game.id 文字列です。資料、メディア参照、お気に入り、履歴、非表示、利用者の編集印を含む Game を返し、存在しなければ null です。ROM 本文は返しません。不正入力や読み取り権限不足で失敗します。

```javascript
const game = await retromao.library.game("game-demo");
```

<a id="api-ja-library-games"></a>

### retromao.library.games

```typescript
games(query?: Query): Promise<Page>
```

`library.games` · `0.9.90` · PAGE / ACTION / RESOURCE

query は省略可です。platformId と collection（ALL/FAVORITES/RECENT、既定 ALL）で絞り込みます。after の既定は null、limit は 40、範囲は 1–200 です。Game の games 配列と next（次のカーソルまたは null）を含む Page を返します。next をそのまま after に渡し、RECENT では lastPlayedAt（ミリ秒）も保持します。不正な件数やカーソルは失敗します。

```javascript
const page = await retromao.library.games({ limit: 40 });
if (page.next) {
  const nextPage = await retromao.library.games({ limit: 40, after: page.next });
}
```

<a id="api-ja-library-records"></a>

### retromao.library.records

```typescript
records(query?: Query): Promise<RecordPage>
```

`library.records` · `0.9.91` · PAGE / ACTION / RESOURCE

query は省略可です。platformId と collection（ALL/FAVORITES/RECENT、既定 ALL）で絞り込みます。after の既定は null、limit は 200、範囲は 1–200 です。GameRecord の games 配列と next（次のカーソルまたは null）を含む RecordPage を返します。next をそのまま after に渡し、RECENT では lastPlayedAt（ミリ秒）も保持します。不正な件数やカーソルは失敗します。 records は id/platformId/title/romFileNames/favorite/recent のみで、パス、メディア、ハッシュは含みません。

```javascript
const page = await retromao.library.records({ limit: 200 });
if (page.next) {
  const nextPage = await retromao.library.records({ limit: 200, after: page.next });
}
```

<a id="api-ja-library-edit"></a>

### retromao.library.edit

```typescript
edit(changes: Edit[], checkpoint?: Record<string, Json>): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

changes は異なる gameId の Edit を 1–200 件指定し、各項目で一つ以上変更します。mode は既定 EDIT、FILL_MISSING は利用者の編集を上書きせず補完可能な空欄だけを埋めます。metadata/recent/media/extensions の expected は直前の読み取り値を使い、競合時はバッチ全体が失敗します。任意の checkpoint は専用 JSON の最上位パッチ（null でキー削除）で、このバッチと同一トランザクションで保存します。複数呼び出しは一つのトランザクションではありません。削除済みローカル項目のメディア・拡張編集は失敗します。更新後の Game[] を返します。checkpoint は 0.9.91 以降です。metadata.values は MetadataField の列挙キーと文字列値を使い、RATING も文字列です。形式はホストが検査します。

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const updated = await retromao.library.edit([{
  gameId: game.id,
  metadata: { expected: game.metadata, values: { DESCRIPTION: "Example note" } }
}], { lastGame: game.id });
```

<a id="api-ja-library-apply"></a>

### retromao.library.apply

```typescript
apply(changes: Edit[], checkpoint?: Record<string, Json>): Promise<void>
```

`library.edit` · `0.9.91` · PAGE / ACTION / RESOURCE

changes は異なる gameId の Edit を 1–200 件指定し、各項目で一つ以上変更します。mode は既定 EDIT、FILL_MISSING は利用者の編集を上書きせず補完可能な空欄だけを埋めます。metadata/recent/media/extensions の expected は直前の読み取り値を使い、競合時はバッチ全体が失敗します。任意の checkpoint は専用 JSON の最上位パッチ（null でキー削除）で、このバッチと同一トランザクションで保存します。複数呼び出しは一つのトランザクションではありません。削除済みローカル項目のメディア・拡張編集は失敗します。edit と同じ検査を使い returnGames:false を指定します。Promise<void> の結果は使用しません（ブリッジは null）。大きな応答を避けるバッチ同期に適します。

```javascript
await retromao.library.apply([{ gameId: "game-demo", favorite: true }], { lastGame: "game-demo" });
```

<a id="api-ja-favorites-list"></a>

### retromao.favorites.list

```typescript
list(query?: Query): Promise<Page>
```

`library.games` · `0.9.90` · PAGE / ACTION / RESOURCE

引数と Page は library.games と同じで、limit は既定 40 です。query に指定しても collection=FAVORITES に固定します。同じ集合・条件のカーソルを使ってください。不正な引数は失敗します。

```javascript
const page = await retromao.favorites.list({ limit: 40 });
```

<a id="api-ja-recent-list"></a>

### retromao.recent.list

```typescript
list(query?: Query): Promise<Page>
```

`library.games` · `0.9.90` · PAGE / ACTION / RESOURCE

引数と Page は library.games と同じで、limit は既定 40 です。query に指定しても collection=RECENT に固定します。同じ集合・条件のカーソルを使ってください。不正な引数は失敗します。

```javascript
const page = await retromao.recent.list({ limit: 40 });
```

<a id="api-ja-favorites-set"></a>

### retromao.favorites.set

```typescript
set(gameId: string, favorite: boolean): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

gameId は端末内 ID、favorite は明示的な真偽値です。library.edit 経由で Game[] を返します。同じ値を繰り返しても反転しません。対象不在や権限不足は失敗します。設定だけなら LIBRARY_READ は不要で、事前に読む場合は必要です。

```javascript
const updated = await retromao.favorites.set("game-demo", true);
```

<a id="api-ja-recent-edit"></a>

### retromao.recent.edit

```typescript
edit(gameId: string, expected: Recent, value: Recent): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

gameId、直前に読んだ完全な expected Recent、新しい完全な value が必要です。lastPlayedAt は非負の Unix ミリ秒または null、playCount は非負整数、importedPlayTimeSeconds は非負の秒または null です。Game[] を返し、現在値が expected と value のどちらでもなければ競合します。ゲーム起動や回数の自動加算はしません。

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const updated = await retromao.recent.edit(game.id, game.recent, { ...game.recent, playCount: game.recent.playCount + 1 });
```

<a id="api-ja-media-folders"></a>

### retromao.media.folders

```typescript
folders(platformId?: string): Promise<{ id: string; platformId: string; role: "ROM" | "MEDIA"; name: string }[]>
```

`media.folders` · `0.9.90` · PAGE / ACTION / RESOURCE

platformId は任意で、省略時は設定済みの全フォルダーを返します。結果は {id,platformId,role,name}[]、role は ROM/MEDIA です。任意の端末パスやディレクトリ権限は公開しません。この id を assets に使用します。権限不足は失敗します。

```javascript
const folders = await retromao.media.folders("fc");
```

<a id="api-ja-media-assets"></a>

### retromao.media.assets

```typescript
assets(folderId: string, afterPath?: string | null, limit?: number): Promise<Asset[]>
```

`media.assets` · `0.9.90` · PAGE / ACTION / RESOURCE

folderId が必要です。afterPath は既定 null、limit は既定 100、範囲 1–200 です。folderId/path/revision/bytes の Asset[] を返します。末尾の path を afterPath に渡し、空配列まで続けます。索引済み素材だけで本文は返しません。フォルダーの削除や不正な件数は失敗します。

```javascript
const assets = await retromao.media.assets("media-demo", null, 100);
if (assets.length) {
  const nextAssets = await retromao.media.assets("media-demo", assets[assets.length - 1].path, 100);
}
```

<a id="api-ja-media-edit"></a>

### retromao.media.edit

```typescript
edit(gameId: string, media: NonNullable<Edit["media"]>): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

gameId と {role,expected,asset} の配列が必要で、role は重複不可です。expected は現在の完全な Media または null、asset は索引済みの完全な Asset、解除時は null です。Game[] を返します。機種、媒体用途、形式、revision/bytes を検査し、参照の変更やローカル項目の削除は失敗します。ファイル自体は削除しません。

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const expected = game.media.find(item => item.role === "COVER") || null;
const updated = await retromao.media.edit(game.id, [{ role: "COVER", expected, asset: null }]);
```

<a id="api-ja-index-patch"></a>

### retromao.index.patch

```typescript
patch(gameId: string, extensions: NonNullable<Edit["extensions"]>): Promise<Game[]>
```

`library.edit` · `0.9.90` · PAGE / ACTION / RESOURCE

gameId と、専用項目名を {expected?,value?} に対応させる extensions が必要です。metadata.extensions[プラグインID] だけを書きます。expected 省略は元の値なし、value 省略は削除、明示的 null は JSON null 保存です。Game[] を返し、現在値が expected と value のどちらでもなければ競合します。他の名前空間には書けません。

```javascript
const game = await retromao.library.game("game-demo");
if (!game) throw new Error("Game missing");
const expected = game.metadata.extensions?.["demo-plugin"]?.note;
const updated = await retromao.index.patch(game.id, { note: { expected, value: "Example note" } });
```

<a id="api-ja-settings-get"></a>

### retromao.settings.get

```typescript
get(): Promise<Record<string, string>>
```

`settings.get` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

引数なしで専用設定 Record<string,string> を返し、未保存値はマニフェストの既定値です。SECRET も復号済み文字列なのでログに出さないでください。処理・解析では開始時のスナップショットを使います。BOOLEAN/NUMBER は明示的に変換します。読み取り専用で、設定保存はホスト画面が担当します。置換・削除後は失敗します。

```javascript
const settings = await retromao.settings.get();
```

<a id="api-ja-data-get"></a>

### retromao.data.get

```typescript
get(): Promise<Record<string, Json>>
```

`data.get` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

引数なしで専用 JSON オブジェクトを返します。初回は空で、配布元とプラグイン ID ごとに分離します。無効時も設定ページで読めます。ゲーム DB、認証情報、自動クラウド同期ではありません。置換・削除後は失敗します。

```javascript
const data = await retromao.data.get();
```

<a id="api-ja-data-patch"></a>

### retromao.data.patch

```typescript
patch(values: Record<string, Json>): Promise<Record<string, Json>>
```

`data.patch` · `0.9.90` · PAGE / CONFIGURATION / ACTION / RESOURCE

values は最上位 JSON のパッチです。非 null は値全体を置換し、null はキーを削除します。再帰的マージはしません。更新後の専用オブジェクト全体を返します。別呼び出しとはトランザクションにならず、ライブラリと同時保存する場合は library.edit/apply の checkpoint を使います。無効時も設定ページで書けます。置換・削除後は失敗します。

```javascript
const updated = await retromao.data.patch({ lastCursor: null, mode: "manual" });
```

<a id="api-ja-storage-sources"></a>

### retromao.storage.sources

```typescript
sources(): Promise<StorageSource[]>
```

`storage.sources` · `0.9.91` · PAGE / CONFIGURATION / ACTION / RESOURCE

引数なしで設定済み StorageSource[]（id/name/provider/scope）を返し、認証情報は返しません。業務では STORAGE の許可、CONFIGURATION では宣言だけが必要で無効時も選択できます。scope はアカウントと専用ディレクトリに結び付きます。id だけでなく全体を保存し、アカウントやディレクトリ変更後は再選択します。

```javascript
const sources = await retromao.storage.sources();
```

<a id="api-ja-storage-read"></a>

### retromao.storage.read

```typescript
read(source: StorageSource, key: string): Promise<{ token: string; value: Record<string, Json> | null }>
```

`storage.read` · `0.9.91` · ACTION

source は sources が返した完全なオブジェクトです。key は [a-zA-Z][a-zA-Z0-9._-]{0,79}\.json に一致し、パスは不可です。{token,value} を返し、不在は value:null、既存文書は JSON オブジェクトです。最大 384 KiB で、512 KiB のメッセージ制限も適用されます。バックグラウンド処理専用で、scope 変更、不正 JSON、通信失敗は拒否し、別の接続先へ切り替えません。

```javascript
const sources = await retromao.storage.sources();
if (!sources.length) throw new Error("No storage source");
const document = await retromao.storage.read(sources[0], "state.json");
```

<a id="api-ja-storage-write"></a>

### retromao.storage.write

```typescript
write(token: string, value: Record<string, Json>): Promise<void>
```

`storage.write` · `0.9.91` · ACTION

token は同じバックグラウンド処理内の最後の read のものです。value は最大 384 KiB の JSON オブジェクトです。Promise<void>（ブリッジでは null）を返し、未変更ならアップロードしません。実書き込み後は token が失効します。別文書の読み取りで旧 token は置き換わり、処理をまたいで保存できません。アカウント・ディレクトリ変更、失効、リモート競合は失敗します。再取得して業務上のマージを判断し、他版を上書きしないでください。

```javascript
const sources = await retromao.storage.sources();
if (!sources.length) throw new Error("No storage source");
const document = await retromao.storage.read(sources[0], "state.json");
await retromao.storage.write(document.token, { ...(document.value || {}), example: true });
```

<a id="api-ja-http-request"></a>

### retromao.http.request

```typescript
request(options: { url: string; method?: "GET" | "HEAD" | "POST" | "PUT" | "PATCH" | "DELETE"; headers?: Record<string, string>; body?: string }): Promise<{ status: number; headers: Record<string, string>; body: string }>
```

`http.request` · `0.9.90` · PAGE / ACTION / RESOURCE

options.url は必須の HTTP(S)、method は既定 GET です。GET/HEAD/POST/PUT/PATCH/DELETE、文字列 headers、任意の本文を使えます。POST/PUT/PATCH の本文省略時は空です。networkHosts にホスト（非標準ポートは host:port）を宣言します。{status,headers,body} を返し、headers は文字列、body は UTF-8 で、リダイレクトしません。非 2xx だけでは例外になりません。通信、未宣言ホスト、256 KiB 超の本文、過大メッセージは失敗します。ストリームやバイナリー API はありません。

```javascript
const response = await retromao.http.request({ url: "https://example.com/api/state" });
if (response.status < 200 || response.status >= 300) {
  throw new Error(`HTTP ${response.status}`);
}
const value = JSON.parse(response.body);
```

<a id="api-ja-tasks-run"></a>

### retromao.tasks.run

```typescript
run(action: string, arguments_?: Record<string, Json>): Promise<Task>
```

`tasks.run` · `0.9.90` · PAGE

action はマニフェストの actions と define.actions の同じ ID です。arguments_ は既定で空の JSON オブジェクトです。結果ではなく新しい Task を返し、同時実行は一つです。未宣言動作や前の処理が活動中の場合は要求を拒否します。設定は実行時に検査し、不正ならタスクが FAILED になります。業務ページ専用で再帰的な処理作成はできません。版と設定のスナップショットを使い、新規処理は前の記録と結果を置き換えます。

```javascript
const task = await retromao.tasks.run("run", { dryRun: true });
```

<a id="api-ja-tasks-current"></a>

### retromao.tasks.current

```typescript
current(): Promise<Task | null>
```

`tasks.current` · `0.9.90` · PAGE / ACTION / RESOURCE

引数なしで専用の最新 Task または null を返します。完了・失敗・キャンセルも含み、実行中だけではありません。ページを開き直したときに使用します。保持は一件で、履歴一覧ではありません。無効化・置換後は失敗します。

```javascript
const task = await retromao.tasks.current();
```

<a id="api-ja-tasks-get"></a>

### retromao.tasks.get

```typescript
get(id: string): Promise<Task>
```

`tasks.get` · `0.9.90` · PAGE / ACTION / RESOURCE

id は現在保持されている専用タスク ID です。Task を返し、置換済み、不在、他プラグインの ID は失敗します。時刻は Unix ミリ秒、completed は非負件数、total は非負合計または null、message は人向けの状態説明でエラーコードではありません。

```javascript
const task = await retromao.tasks.get("task-demo");
```

<a id="api-ja-tasks-result"></a>

### retromao.tasks.result

```typescript
result(id: string): Promise<Json>
```

`tasks.result` · `0.9.90` · PAGE / ACTION / RESOURCE

id は保持中の専用タスクです。SUCCEEDED の場合だけ動作の Json を返し、戻り値なしは null です。未成功、置換済み、他所有者は失敗します。長期保存として使わず、必要な値は data やライブラリ API で保存します。

```javascript
const task = await retromao.tasks.get("task-demo");
if (task.state === "SUCCEEDED") {
  const result = await retromao.tasks.result(task.id);
}
```

<a id="api-ja-tasks-cancel"></a>

### retromao.tasks.cancel

```typescript
cancel(id: string): Promise<void>
```

`tasks.cancel` · `0.9.90` · PAGE

id は保持中の専用タスクです。Promise<void> を返し、活動中ならキャンセルを要求します。終了済みには再実行しません。保存済みバッチは残り、全体を巻き戻しません。他所有者や置換済み ID は失敗します。CANCELLING を経る場合があるため current/get/watch で CANCELLED などの終状態を確認します。バックグラウンド自身からは使えません。

```javascript
await retromao.tasks.cancel("task-demo");
const task = await retromao.tasks.current();
```

<a id="api-ja-tasks-progress"></a>

### retromao.tasks.progress

```typescript
progress(completed: number, total?: number | null, message?: string): Promise<void>
```

`tasks.progress` · `0.9.90` · ACTION

completed は非負整数、total は既定 null（不明）または completed 以上の整数、message は既定空文字列です。Promise<void> を返します。実行中のバックグラウンド動作専用で、ページ、解析、停止済み、不正件数は失敗します。ホストは約 300ms 間隔で保存し、完了値も保存します。業務の checkpoint の代わりにはなりません。

```javascript
await retromao.tasks.progress(1, 2, "Processing");
```

<a id="api-ja-tasks-watch"></a>

### retromao.tasks.watch

```typescript
watch(id: string, callback: (task: Task) => void): () => void
```

`LOCAL` · `0.9.90` · PAGE

id と callback が必要で、Promise ではなく購読解除関数を同期的に返します。同じ ID の Task 通知だけを受け、SDK に一致するキャッシュがあれば登録時に即時通知します。状態は取得しないため、先に current/get を使います。終了時に購読を解放してもバックグラウンドは継続します。完全な履歴は保持しません。他の購読を妨げないようコールバックの失敗はページ側で処理してください。

```javascript
const task = await retromao.tasks.current();
if (task) {
  const stop = retromao.tasks.watch(task.id, value => { console.log(value.state); });
  stop();
}
```

<a id="api-ja-define"></a>

### retromao.define

```typescript
define(definition: { actions?: Record<string, (arguments_: Record<string, Json>) => Json | void | Promise<Json | void>>;
      resources?: Record<string, (arguments_: { games: ResourceGame[] }) => ResourceResolution[] | Promise<ResourceResolution[]>> }): void
```

`LOCAL` · `0.9.90` · ACTION / RESOURCE

バックグラウンド入口のトップレベルで {actions?,resources?} を一度登録し、同期的に void を返します。重複は Error です。actions のキーはマニフェスト actions.id と一致し、Json オブジェクトを受け、Json/void または Promise を返します。ホストが実行して結果を保存します。resources は 0.9.98、ROM_RESOURCES、対応する resourceProviders が必要です。{games:[{gameId,romNames}]} を受け、入力ゲームごとにちょうど一つの ResourceResolution[] を返します。権限ルート内の安全な相対パスだけで、転送はしません。例外は動作・解析を失敗させます。内部 __run を呼ばないでください。

```javascript
retromao.define({
  actions: { run: async arguments_ => ({ dryRun: arguments_.dryRun === true }) }
});
```
