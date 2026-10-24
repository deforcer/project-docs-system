# Project Docs System

Скилл для проектной документации: требования, решения, проверки и контекст для продолжения работы. Помогает создать структуру документов, адаптировать существующую и поддерживать её при изменениях.

Подходит для разработки, QA, исследований и организационных проектов. Работает в Codex, Claude Code и других клиентах с поддержкой Agent Skills.

## Быстрая установка через агента

Скопируйте этот промпт в свой ассистент:

```text
Установи project-docs-system из https://github.com/deforcer/project-docs-system для
текущего пользователя.

В Claude Code добавь marketplace deforcer/project-docs-system и установи плагин
project-docs-system@project-docs-system в user scope. В Codex и других клиентах Agent
Skills установи папку skills/project-docs-system целиком как личный скилл.

Выбери каталог по настройкам клиента и ОС. Сохрани существующие пользовательские правки
и источник обновлений, не создавай дубли. Проверь комплектность пакета и доступность
скилла. Если нужна новая сессия, сообщи об этом. Автообновление настраивай только по
отдельному запросу.
```

## Установка вручную

### Claude Code

В терминале:

```sh
claude plugin marketplace add deforcer/project-docs-system
claude plugin install project-docs-system@project-docs-system --scope user
```

Откройте новую сессию. Скилл доступен по команде:

```text
/project-docs-system:project-docs-system
```

### Codex

Попросите Codex установить скилл:

```text
Используй $skill-installer: установи скилл из
https://github.com/deforcer/project-docs-system/tree/main/skills/project-docs-system
```

Откройте новую сессию и вызовите `$project-docs-system`.

### Установка папкой

Если установщик недоступен, скачайте ZIP репозитория или клонируйте его в любое удобное место:

```sh
git clone https://github.com/deforcer/project-docs-system.git
```

Скопируйте папку **`skills/project-docs-system` целиком** в каталог скиллов клиента:

| Клиент | Каталог личных скиллов |
| --- | --- |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Другой клиент | Каталог, указанный в его настройках или документации |

`~` — домашняя папка пользователя; в Windows PowerShell используйте `$HOME`. Для одного проекта используйте `.agents/skills/` или `.claude/skills/` внутри него. Существующую установку сначала сравните с новой, сохранив свои правки.

В пакете должны остаться `SKILL.md`, `agents/`, `references/` и `assets/`. Символические ссылки не нужны. При установке папкой команда Claude Code — `/project-docs-system`.

## Как пользоваться

Откройте целевой проект и опишите первую задачу:

```text
Примени скилл project-docs-system.
Я тестировщик. Нужно организовать регрессионное тестирование.
Документы храни в docs, сохрани существующую структуру.
Начни со сценариев проверки авторизации.
```

Скилл изучит проект и подготовит нужные документы, связи и следующие шаги. Можно также попросить адаптировать готовую документацию или обновить её после изменения. Если нужен только план, укажите это в запросе.

## Обновление

**Claude Code — плагин:**

```sh
claude plugin marketplace update project-docs-system
claude plugin update project-docs-system@project-docs-system --scope user
```

После обновления откройте новую сессию.

**Codex и установка папкой:** попросите агента:

```text
Обнови project-docs-system из https://github.com/deforcer/project-docs-system. Проверь
существующую установку, сохрани мои правки и проверь результат.
```

<details>
<summary>Разработка и проверка</summary>

Версия скилла: **0.1.0**. Исходники: [skills/project-docs-system](skills/project-docs-system/).

```sh
python3 scripts/validate.py
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

Проверки выполняются локально: комплектность, внутренние ссылки, переносимость и манифесты. Поведение ассистента проверяется отдельно: [сценарии](tests/scenarios.md), [результаты](tests/results-v0.1.0.md).

Документация клиентов: [Codex](https://developers.openai.com/codex/skills/), [Claude Code Skills](https://code.claude.com/docs/en/skills), [Claude Code Marketplace](https://code.claude.com/docs/en/plugin-marketplaces).

</details>
