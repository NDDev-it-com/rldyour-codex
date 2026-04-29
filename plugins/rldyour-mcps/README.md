# rldyour-mcps

`rldyour-mcps` — рабочий набор MCP-серверов, которые владелец использует в Codex.

Плагин написан для русскоязычной работы: все пользовательские описания, подсказки и документация внутри плагина ведутся на русском. Технические идентификаторы остаются ASCII и kebab-case, чтобы не ломать совместимость Codex, MCP-клиентов и tooling.

## Граница ответственности

Плагин отвечает только за подключение MCP-серверов.

Он не задает глобальные правила поведения агента, не хранит память, не включает workflow-команды, не подменяет security-политику и не добавляет skills. Эти части будут вынесены в отдельные плагины: `rldyour-rules`, `rldyour-flow`, `rldyour-memories`, `rldyour-sec` и отдельные MCP-specific плагины.

## Правило запуска

Все локальные MCP-серверы запускаются только через разрешенные владельцем рантаймы:

- `uv` / `uvx`;
- `bun` / `bunx`;
- `dart`.

В этом плагине не используются `npx`, `npm`, `node` как прямые команды MCP. Удаленные MCP с `url` остаются URL-подключениями и не запускают локальный процесс.

## Правило языка

- Общение с владельцем ведется на русском.
- Описания plugin/marketplace metadata ведутся на русском.
- Названия MCP, package names, команды, env vars и URL не переводятся.
- Если MCP возвращает данные на английском, агент кратко объясняет результат владельцу на русском.

## Правило безопасности

- Секреты не записываются в `.mcp.json`, `plugin.json`, README или marketplace.
- Write-инструменты MCP используются только когда задача явно требует изменения состояния.
- Для destructive-действий нужно отдельное подтверждение владельца.
- Remote MCP используются только по явно указанным URL.
- Локальные MCP запускаются только через `uv`, `uvx`, `bun`, `bunx` или `dart`.

## Подключенные MCP

| MCP | Назначение | Запуск |
| --- | --- | --- |
| `serena` | Семантическая навигация, анализ и точечное редактирование кода | `uvx`, headless |
| `sequential-thinking` | Структурирование сложных рассуждений и планов | `bunx` |
| `playwright` | Браузерная автоматизация и проверки UI | `bunx`, headless |
| `chrome-devtools` | Диагностика страниц через Chrome DevTools | `bunx`, headless, isolated |
| `context7` | Актуальная документация библиотек | `bunx`, `CONTEXT7_API_KEY` |
| `deepwiki` | Документация и объяснение репозиториев | remote URL |
| `grep` | Поиск по публичным GitHub-репозиториям | remote URL |
| `semgrep` | Статический анализ и security-проверки кода | `uvx` |
| `shadcn` | Работа с registry shadcn/ui | `bunx` |
| `dart-flutter` | Dart/Flutter MCP для проектов на Dart и Flutter | `dart` |
| `figma` | Контекст дизайна из Figma | remote URL, OAuth |

## Секреты

Не записывай ключи в `.mcp.json`.

Для Context7 нужен environment variable:

```bash
export CONTEXT7_API_KEY="ctx7sk_..."
```

Текущий ключ владельца намеренно не сохранен в репозиторий.

## Проверка в Codex

После установки или обновления плагина проверь:

```bash
codex mcp list
codex mcp get serena
codex mcp get figma
```

Ожидаемое состояние:

- `serena` запускается через `uvx` и не открывает dashboard автоматически.
- `figma` использует OAuth.
- `context7` берет ключ только из `CONTEXT7_API_KEY`.
- Локальные MCP не используют `npx`, `npm` или `node` как прямую команду.

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
