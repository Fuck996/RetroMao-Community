declare namespace RetroMao {
  type Json = null | boolean | number | string | Json[] | { [key: string]: Json };
  type IconName = "plugin" | "star" | "history" | "sync" | "cloud" | "library" | "image" | "language" | "palette" | "gamepad" | "chart" | "settings";
  type MediaRole = "COVER" | "CARTRIDGE" | "DISC" | "LOGO" | "VIDEO" | "SCREENSHOT" | "BACK" | "SPINE" | "MANUAL";
  type MetadataField = "TITLE" | "DESCRIPTION" | "DEVELOPER" | "PUBLISHER" | "GENRE" | "RELEASE_DATE" | "PLAYERS" | "RATING" | "SORT_TITLE";
  interface Metadata { title: string; description: string; developer: string; publisher: string; genre: string; releaseDate: string; players: string; rating: number | null; sortTitle: string; extensions?: Record<string, Record<string, Json>>; }
  interface Recent { lastPlayedAt: number | null; playCount: number; importedPlayTimeSeconds: number | null; }
  interface Asset { folderId: string; path: string; revision: string; bytes: number; }
  interface Media { role: MediaRole; fileId: string; folderId: string | null; path: string; localPresence: "PRESENT" | "ABSENT" | "UNKNOWN"; remotePresence: "PRESENT" | "ABSENT" | "UNKNOWN"; cached: boolean; }
  interface Game { id: string; platformId: string; metadata: Metadata; media: Media[]; favorite: boolean; recent: Recent; hidden: boolean; localEntryRemoved: boolean; userEditedFields: string[]; userEditedMediaRoles: MediaRole[]; }
  interface Query { platformId?: string; collection?: "ALL" | "FAVORITES" | "RECENT"; after?: { gameId: string; lastPlayedAt?: number | null } | null; limit?: number; }
  interface Page { games: Game[]; next: Query["after"]; }
  interface GameRecord { id: string; platformId: string; title: string; romFileNames: string[]; favorite: boolean; recent: Recent; }
  interface RecordPage { games: GameRecord[]; next: Query["after"]; }
  interface StorageSource { id: string; name: string; provider: string; scope: string; }
  interface Edit { gameId: string; metadata?: { expected: Metadata; values: Partial<Record<MetadataField, string>> }; favorite?: boolean; recent?: { expected: Recent; value: Recent }; media?: { role: MediaRole; expected: Media | null; asset: Asset | null }[]; extensions?: Record<string, { expected?: Json; value?: Json }>; mode?: "EDIT" | "FILL_MISSING"; }
  interface Task { id: string; pluginId: string; version: string; actionId: string; state: "WAITING" | "RUNNING" | "CANCELLING" | "SUCCEEDED" | "FAILED" | "CANCELLED"; message: string; completed: number; total: number | null; createdAt: number; updatedAt: number; }
  interface Api {
    readonly version: 1;
    readonly ready: Promise<{ locale?: string; colors?: Record<string, string> }>;
    icons: { list(): Promise<readonly IconName[]>; url(name: IconName): string };
    library: { game(id: string): Promise<Game | null>; games(query?: Query): Promise<Page>; records(query?: Query): Promise<RecordPage>; edit(changes: Edit[], checkpoint?: Record<string, Json>): Promise<Game[]>; apply(changes: Edit[], checkpoint?: Record<string, Json>): Promise<void> };
    favorites: { list(query?: Query): Promise<Page>; set(gameId: string, favorite: boolean): Promise<Game[]> };
    recent: { list(query?: Query): Promise<Page>; edit(gameId: string, expected: Recent, value: Recent): Promise<Game[]> };
    media: { folders(platformId?: string): Promise<{ id: string; platformId: string; role: "ROM" | "MEDIA"; name: string }[]>; assets(folderId: string, afterPath?: string | null, limit?: number): Promise<Asset[]>; edit(gameId: string, media: NonNullable<Edit["media"]>): Promise<Game[]> };
    index: { patch(gameId: string, extensions: NonNullable<Edit["extensions"]>): Promise<Game[]> };
    settings: { get(): Promise<Record<string, string>> };
    data: { get(): Promise<Record<string, Json>>; patch(values: Record<string, Json>): Promise<Record<string, Json>> };
    storage: { sources(): Promise<StorageSource[]>; read(source: StorageSource, key: string): Promise<{ token: string; value: Record<string, Json> | null }>; write(token: string, value: Record<string, Json>): Promise<void> };
    http: { request(options: { url: string; method?: "GET" | "HEAD" | "POST" | "PUT" | "PATCH" | "DELETE"; headers?: Record<string, string>; body?: string }): Promise<{ status: number; headers: Record<string, string>; body: string }> };
    tasks: { run(action: string, arguments_?: Record<string, Json>): Promise<Task>; current(): Promise<Task | null>; get(id: string): Promise<Task>; result(id: string): Promise<Json>; cancel(id: string): Promise<void>; progress(completed: number, total?: number | null, message?: string): Promise<void>; watch(id: string, callback: (task: Task) => void): () => void };
    define(definition: { actions: Record<string, (arguments_: Record<string, Json>) => Json | void | Promise<Json | void>> }): void;
  }
}
declare const retromao: RetroMao.Api;
