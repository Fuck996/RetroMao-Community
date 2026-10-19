"""Validate the public API inventory, generated reference and immutable releases."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("中文", "English", "日本語")
CONTEXTS = {"PAGE", "CONFIGURATION", "ACTION", "RESOURCE"}
CAPABILITIES = {"LIBRARY_READ", "LIBRARY_WRITE", "NETWORK", "STORAGE", "ROM_RESOURCES"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def version(value):
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", value):
        raise ValueError(f"Invalid API release version: {value}")
    return tuple(map(int, value.split(".")))


def members(body):
    start, depth = 0, 0
    for index, character in enumerate(body):
        if character in "{([":
            depth += 1
        elif character in "})]":
            depth -= 1
        elif character == ";" and depth == 0:
            yield body[start:index].strip()
            start = index + 1
    if body[start:].strip():
        yield body[start:].strip()


def declarations(types):
    body = types.split("interface Api {", 1)[1].rsplit("}", 2)[0].strip()
    result = {}
    for member in members(body):
        match = re.match(r"(?:readonly\s+)?(\w+)\s*([:(])", member)
        if not match:
            raise ValueError(f"Cannot parse public declaration: {member}")
        name = match[1]
        value = member[match.end():].lstrip()
        if match[2] == ":" and value.startswith("{"):
            for child in members(value[1:value.rfind("}")]):
                method = re.match(r"(\w+)\s*\(", child)
                if not method:
                    raise ValueError(f"Cannot parse public method: {child}")
                result[f"{name}.{method[1]}"] = child
        else:
            result[name] = member
    return result


def normalize(value):
    return re.sub(r"\s+", "", value)


def source_hash(path):
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def reference(manifest):
    lines = ["# API 调用手册 / API reference / API リファレンス", "",
             "[中文](#中文) · [English](#english) · [日本語](#日本語)", "",
             "[SDK](README.md) · [Types](retromao.d.ts) · [Inventory](api.json) · "
             "[Versioning](API_VERSIONING.md) · [Changes](API_CHANGELOG.md) · [All contracts](../docs/INTERFACES.md)", ""]
    introductions = [
        "本文件由 tools/check_api.py 从 api.json 生成，请编辑清单后运行 --write。当前契约 {version}，运行时 API {apiVersion}，对照宿主 {verifiedHostVersion}。完整字段见 Types；本页覆盖每个公开成员的签名、权限、上下文、参数、返回值、限制与示例。",
        "Generated from api.json by tools/check_api.py; edit the inventory and run --write. Contract {version}, runtime API {apiVersion}, checked against host {verifiedHostVersion}. Types defines every data field; this reference covers each public member's signature, grants, contexts, arguments, results, constraints and example.",
        "api.json から tools/check_api.py で生成します。一覧を編集して --write を実行してください。契約 {version}、実行 API {apiVersion}、確認対象ホスト {verifiedHostVersion}。全データ項目は Types を参照してください。各公開メンバーのシグネチャ、権限、実行場所、引数、戻り値、制限、例を記載します。",
    ]
    guides = [
        "PAGE = 已启用插件的业务页面；CONFIGURATION = 独立配置页，可在插件禁用时使用；ACTION = tasks.run 发起的后台动作；RESOURCE = 宿主资源解析回调。标记未列出的上下文不属于受支持调用方式。权限须在 plugin.json 声明并授权；storage.sources 的配置页例外见该接口。",
        "PAGE = enabled plugin business page; CONFIGURATION = dedicated configuration page, also available while disabled; ACTION = background action started with tasks.run; RESOURCE = host resource-resolution callback. Unlisted contexts are unsupported usage. Declare grants in plugin.json and obtain approval; see storage.sources for its configuration-page exception.",
        "PAGE は有効なプラグインの業務ページ、CONFIGURATION は無効時にも利用できる独立設定ページ、ACTION は tasks.run のバックグラウンド処理、RESOURCE はホストのリソース解析コールバックです。記載のない場所での呼び出しはサポート対象外です。plugin.json で権限を宣言して許可を得てください。storage.sources の設定ページでの例外は個別説明を参照してください。",
    ]
    errors = [
        "调用前等待 retromao.ready。所有 Promise 失败以 Error 拒绝，部分本地同步方法直接抛 Error；没有稳定数字错误码，不按提示文本判断业务状态。插件被禁用／替换、缺权限、输入无效、并发冲突、网络或会话关闭均可能失败。向界面或任务返回真实错误；冲突先重读，禁止静默重试写入。HTTP 非 2xx 是正常响应对象，作者须检查 status。",
        "Await retromao.ready first. Promise failures reject with Error; local synchronous methods can throw Error. There are no stable numeric error codes; do not branch on message text. Disabled/replaced plugins, missing grants, invalid input, conflicts, network and closed sessions can fail. Expose the error in the page/task; reread conflicts before a new decision and never silently retry writes. Non-2xx HTTP returns a response object: check status.",
        "最初に retromao.ready を待ちます。Promise の失敗は Error で拒否され、ローカル同期メソッドは Error を送出する場合があります。安定した数値エラーコードはありません。メッセージ文字列で状態を判定しないでください。無効化・置換、権限不足、不正入力、競合、通信、セッション終了で失敗します。画面やタスクで原因を表示し、競合は再取得して判断してください。書き込みを黙って再試行してはいけません。HTTP の非 2xx は応答オブジェクトなので status を確認します。",
    ]
    limits = [
        "示例中的 game-demo、media-demo、task-demo 和 example.com 是样本标识，须替换为当前库、任务和已声明主机；含写入的示例会修改数据，应先在独立预览样本运行。每段可独立调用，define 只用于后台入口。SDK 最多同时发送 4 个请求；单条请求／响应最大 512 KiB。后台无 DOM 或 Node.js。__run、__dispose、原生桥和传输协议不是公开调用入口。",
        "game-demo, media-demo, task-demo and example.com are fixture identifiers: replace them with current library/task IDs and declared hosts. Write examples modify data; try them in fixture preview first. Each snippet stands alone; define belongs in the background entry. SDK concurrency is 4; each request/response is limited to 512 KiB. Background code has no DOM or Node.js. __run, __dispose, native bridges and transport messages are not public entry points.",
        "game-demo、media-demo、task-demo、example.com はサンプルです。現在のライブラリ・タスク ID と宣言したホストに置き換えてください。書き込み例はデータを変更するため、まず独立プレビューのサンプルで試してください。各例は独立し、define はバックグラウンド入口に置きます。同時要求は最大 4 件、要求・応答は各 512 KiB です。バックグラウンドに DOM や Node.js はありません。__run、__dispose、ネイティブブリッジ、転送メッセージは公開入口ではありません。",
    ]
    for index, locale in enumerate(LOCALES):
        lines += [f"## {locale}", "", introductions[index].format(**manifest), "", guides[index], "", errors[index], "", limits[index], "",
                  "| API | Since / 起始 / 初出 | Capability / 能力 / 権限 | Context / 上下文 / 実行場所 |", "| --- | --- | --- | --- |"]
        for entry in manifest["members"]:
            anchor = f"api-{('zh', 'en', 'ja')[index]}-{entry['path'].replace('.', '-')}"
            lines.append(f"| [`{entry['path']}`](#{anchor}) | {entry['since']} | {', '.join(entry['capabilities']) or '—'} | {', '.join(entry['contexts'])} |")
        lines.append("")
        for entry in manifest["members"]:
            anchor = f"api-{('zh', 'en', 'ja')[index]}-{entry['path'].replace('.', '-')}"
            lines += [f'<a id="{anchor}"></a>', "", f"### retromao.{entry['path']}", "", f"```typescript\n{entry['declaration']}\n```", "",
                      f"`{entry['rpc'] or 'LOCAL'}` · `{entry['since']}` · {' / '.join(entry['contexts'])}", "",
                      entry["description"][locale], "", f"```javascript\n{entry['example']}\n```", ""]
    return "\n".join(lines)


def check_history(manifest, base):
    subprocess.run(["git", "rev-parse", "--verify", f"{base}^{{commit}}"], cwd=ROOT, check=True, stdout=subprocess.PIPE)
    names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", base, "sdk/releases"], cwd=ROOT, text=True).splitlines()
    for name in names:
        old = subprocess.check_output(["git", "show", f"{base}:{name}"], cwd=ROOT)
        if not (ROOT / name).is_file() or (ROOT / name).read_bytes() != old:
            raise ValueError(f"Published API snapshot is immutable: {name}")
    if not names:
        return
    previous = max((json.loads(subprocess.check_output(["git", "show", f"{base}:{name}"], cwd=ROOT)) for name in names), key=lambda item: version(item["version"]))
    if manifest == previous:
        return
    old_version, new_version = version(previous["version"]), version(manifest["version"])
    if new_version <= old_version:
        raise ValueError("API inventory changes require a new release version and snapshot")
    before = {entry["path"]: entry for entry in previous["members"]}
    after = {entry["path"]: entry for entry in manifest["members"]}
    incompatible = any(name not in after or any(before[name][field] != after[name][field] for field in ("declaration", "capabilities", "contexts", "rpc")) for name in before)
    if incompatible and new_version[0] <= old_version[0]:
        raise ValueError("Removed/changed signatures, grants, contexts or RPC mappings require a major release")
    if set(after) - set(before) and new_version[:2] <= old_version[:2]:
        raise ValueError("Additional API members require a minor release")


def check_api(*, write=False, base=None):
    manifest = load(ROOT / "sdk/api.json")
    release_version = version(manifest["version"])
    if manifest["schemaVersion"] != 1 or manifest["apiVersion"] != release_version[0]:
        raise ValueError("API release major must match the implemented runtime API version")
    types = (ROOT / "sdk/retromao.d.ts").read_text(encoding="utf-8")
    declared = declarations(types)
    inventory = {entry["path"]: entry for entry in manifest["members"]}
    if len(inventory) != len(manifest["members"]) or inventory.keys() != declared.keys():
        raise ValueError(f"API inventory/type members differ: {set(inventory) ^ set(declared)}")
    for name, entry in inventory.items():
        if normalize(entry["declaration"]) != normalize(declared[name]):
            raise ValueError(f"API signature differs from TypeScript: {name}")
        if not entry["example"].strip() or set(entry["description"]) != set(LOCALES) or not all(value.strip() for value in entry["description"].values()):
            raise ValueError(f"API needs an example and three descriptions: {name}")
        if not entry["contexts"] or set(entry["contexts"]) - CONTEXTS or set(entry["capabilities"]) - CAPABILITIES:
            raise ValueError(f"Invalid API context/grants: {name}")
        version(entry["since"])
    if manifest.get("sourceEncoding") != "UTF-8/LF":
        raise ValueError("API source hashes must use UTF-8/LF")
    if set(manifest["sources"]) != {"sdk/runtime/retromao.js", "sdk/retromao.d.ts"}:
        raise ValueError("API inventory must track runtime and type source hashes")
    for name, expected in manifest["sources"].items():
        actual = source_hash(ROOT / name)
        if actual != expected:
            raise ValueError(f"SDK source changed; review the API, version and snapshot: {name}")
    if f"version: {manifest['apiVersion']}" not in (ROOT / "sdk/runtime/retromao.js").read_text(encoding="utf-8"):
        raise ValueError("API version differs from the shipped runtime")
    snapshot = ROOT / "sdk/releases" / f"{manifest['version']}.json"
    if not snapshot.is_file() or load(snapshot) != manifest:
        raise ValueError("Current API inventory needs a matching versioned snapshot")
    releases = []
    for path in snapshot.parent.glob("*.json"):
        release = load(path)
        if path.stem != release["version"]:
            raise ValueError(f"API snapshot filename differs from version: {path.name}")
        releases.append(release)
    if max(version(item["version"]) for item in releases) != release_version:
        raise ValueError("Current API release must be the latest snapshot")
    changelog = (ROOT / "sdk/API_CHANGELOG.md").read_text(encoding="utf-8")
    sections = re.split(r"^## (?:中文|English|日本語)\s*$", changelog, flags=re.M)
    if len(sections) != 4:
        raise ValueError("API changelog needs three language sections")
    for section in sections[1:]:
        for release in releases:
            if f"### {release['version']} · {release['date']}" not in section:
                raise ValueError(f"Missing translated API release notes: {release['version']}")
    if base:
        check_history(manifest, base)
    target = ROOT / "sdk/API_REFERENCE.md"
    rendered = reference(manifest)
    if write:
        target.write_text(rendered, encoding="utf-8", newline="\n")
    elif not target.is_file() or target.read_text(encoding="utf-8") != rendered:
        raise ValueError("API_REFERENCE.md is stale; run python tools/check_api.py --write")
    print(f"API {manifest['version']}: {len(inventory)} members, signatures, sources, snapshots and three languages checked")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--base", help="Git commit/ref used to enforce immutable historical releases")
    args = parser.parse_args()
    try:
        check_api(write=args.write, base=args.base)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"ERROR: {error}\n")
