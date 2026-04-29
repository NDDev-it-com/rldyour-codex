# rldyour-mcps

`rldyour-mcps` — базовый набор MCP-серверов для Codex.

Этот плагин содержит только подключение MCP-серверов. Правила работы, отдельные workflows, memory-политики и специализированные skills под каждый MCP будут выноситься в отдельные плагины.

## Правило запуска

Все локальные MCP-серверы запускаются только через разрешенные владельцем рантаймы:

- `uv` / `uvx`;
- `bun` / `bunx`;
- `dart`.

В этом плагине не используются `npx`, `npm`, `node` как прямые команды MCP. Удаленные MCP с `url` остаются URL-подключениями и не запускают локальный процесс.

## Подключенные MCP

- `serena` — семантическая навигация и редактирование кода. Запускается через `uvx`, headless: dashboard не открывается автоматически.
- `sequential-thinking` — структурированное пошаговое мышление через `bunx`. Логирование thought-информации отключено через `DISABLE_THOUGHT_LOGGING=true`.
- `playwright` — браузерная автоматизация через `bunx @playwright/mcp@latest`. Запускается в headless-режиме.
- `chrome-devtools` — Chrome DevTools MCP через `bunx`. Запускается headless, isolated, без usage statistics и без CrUX-запросов.
- `context7` — актуальная документация библиотек через `bunx`. API key берется только из `CONTEXT7_API_KEY`.
- `deepwiki` — удаленный MCP `https://mcp.deepwiki.com/mcp` для документации репозиториев.
- `grep` — удаленный Grep by Vercel `https://mcp.grep.app` для поиска по публичным GitHub-репозиториям.
- `semgrep` — локальный Semgrep MCP через `uvx semgrep-mcp`.
- `shadcn` — MCP для registry shadcn/ui через `bunx shadcn@latest mcp`.
- `dart-flutter` — официальный Dart/Flutter MCP через `dart mcp-server`.
- `figma` — удаленный Figma MCP `https://mcp.figma.com/mcp`; авторизация выполняется отдельно через браузер/OAuth.

## Секреты

Не записывай ключи в `.mcp.json`.

Для Context7 нужен environment variable:

```bash
export CONTEXT7_API_KEY="ctx7sk_..."
```

Текущий ключ владельца намеренно не сохранен в репозиторий.

## Локальные зависимости

Перед использованием проверь, что доступны команды:

```bash
uv --version
uvx --version
bun --version
bunx --help
dart --version
```

## Figma

Для Figma используется удаленный MCP:

```text
https://mcp.figma.com/mcp
```

После установки плагина может потребоваться browser/OAuth авторизация. Если Codex не запросит ее автоматически, используй механизм входа MCP для сервера `figma`.

## Serena

Serena настроена без автоматического открытия dashboard:

```text
uvx --from serena-agent@latest --python 3.13 --prerelease allow serena start-mcp-server --project-from-cwd --context=codex --open-web-dashboard False
```

Если dashboard понадобится вручную, его можно открыть через инструменты Serena или напрямую через локальный URL, который Serena покажет в логах.

## Источники

- Serena: https://oraios.github.io/serena/02-usage/030_clients.html
- Serena dashboard: https://oraios.github.io/serena/02-usage/060_dashboard.html
- Context7: https://www.mintlify.com/upstash/context7/mcp/configuration
- Playwright MCP: https://playwright.dev/mcp/configuration/options
- Chrome DevTools MCP: https://github.com/ChromeDevTools/chrome-devtools-mcp
- DeepWiki MCP: https://mcp.deepwiki.com/
- Grep by Vercel: https://vercel.com/blog/grep-a-million-github-repositories-via-mcp-1H5Bmvo4XKswf0TpZIOmEI
- Semgrep MCP: https://github.com/semgrep/mcp
- shadcn MCP: https://ui.shadcn.com/docs/mcp
- Dart/Flutter MCP: https://docs.flutter.dev/ai/mcp-server
- Figma MCP: https://help.figma.com/hc/en-us/articles/39888629089175-Codex-and-Figma-Set-up-the-MCP-server
