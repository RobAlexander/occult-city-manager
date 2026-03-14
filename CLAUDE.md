# Occult UK City Generator — Claude Code Guide

## What this project is

A Python CLI tool for TTRPG game masters. Procedurally generates cities set in alternate 1980s Britain where the occult is real. No external dependencies — pure stdlib.

Run with: `python main.py`

## File map

| File | Role |
|------|------|
| `models.py` | Dataclasses: `City`, `Region`, `District`, `OccultSite`, `LeyLine`, `Faction`, `FactionRelationship`. All enums live here too. |
| `generator.py` | `CityGenerator` class — seeded RNG, all word lists, factory methods. |
| `storage.py` | `save_city()` / `load_city()` — JSON in `cities/` directory. |
| `main.py` | Interactive REPL, ANSI display helpers, all CRUD commands. |

## Data model

```
City
├── Region
├── District[]          (occult_activity: 1–5)
├── OccultSite[]        (district_id FK, ley_line_ids[], controlling_faction_id FK)
├── LeyLine[]           (strength: 1–5, sites[] = site IDs)
└── Faction[]           (hq_site_id FK, relationships[FactionRelationship])
```

All entities have an 8-char UUID `id` and a `notes` field for GM freetext.
All entities implement `to_dict()` / `from_dict()` for JSON round-tripping.

## Enums

- `DistrictType`: Industrial, Residential, Commercial, Docklands, University, Old Town, Council Estate, Suburb, Parkland, Ecclesiastical
- `OccultSiteType`: Ley Node, Ancient Barrow, Standing Stone, Cursed Church, Haunted Pub, Underground Chamber, Ritual Site, Mirror Pool, Witches' Market, Forgotten Shrine, Alchemy Workshop, Astral Anchor, Gate
- `FactionType`: Coven, Hermetic Order, Government Agency, Church Sect, Street Cult, Academic Circle, Crime Syndicate, Otherworldly Entity
- `ThreatLevel`: Dormant → Stirring → Active → Critical
- `RelationshipType`: Allied, Neutral, Rival, Hostile, Puppet, Unknown

All enums inherit from `str, Enum` so their `.value` is the display string.

## Generation

`CityGenerator(seed=None)` — pass an integer seed for reproducible output.

Key method: `generate_city(num_districts=6, num_sites=8, num_ley_lines=3, num_factions=5)`

Word lists are module-level constants in `generator.py` prefixed with `_`. To expand the vocabulary (more names, descriptions, events), just add strings to the relevant list.

## REPL commands

```
new [seed]        generate city
load / list       load saved city / list saves
show              city overview
districts / sites / ley / factions   list + drill-down
add district|site|ley|faction
edit city|district|site|ley|faction  (edits GM notes only)
delete district|site|ley|faction
save / quit
```

## ANSI colour conventions (main.py)

- Threat colours: Dormant=dim white, Stirring=yellow, Active=red, Critical=bold red
- Relationship colours: Allied=green, Neutral=white, Rival=yellow, Hostile=red, Puppet=purple, Unknown=dim
- UI chrome uses purple/cyan; errors use yellow for warnings, red for hard errors.

## Adding new content

- **New district/site/faction/ley types**: add to the relevant `Enum` in `models.py`, then add corresponding entries to the word-list dicts in `generator.py` (`_SITE_NAMES`, `_SITE_DESCRIPTIONS`, `_FACTION_NAMES`, etc.).
- **New city-level fields**: add to `City` dataclass, update `to_dict()` / `from_dict()`, add display in `display_city_overview()`.
- **New commands**: add an `elif cmd == "..."` branch in `run()` and update `HELP_TEXT`.

## Persistence

Cities saved to `cities/<cityname>.json` (git-ignored). The `cities/` directory is created on first save.
