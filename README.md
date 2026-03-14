# Occult UK City Generator

A command-line tool for TTRPG game masters to generate and manage cities and regions set in an **alternate 1980s Britain** where the occult is real, the government knows about it, and nobody is talking.

Suitable for games in the style of *Unknown Armies*, *Delta Green*, *Kult*, or any modern-occult investigation system.

---

## Features

- **Procedural city generation** — named UK cities with history, geography, and alt-1980s current events (strikes, disappearances, suppressed council minutes)
- **Districts** — typed neighbourhoods (council estate, docklands, ecclesiastical, industrial…) each with an occult activity rating
- **Occult sites** — 13 site types including ley nodes, ancient barrows, haunted pubs, underground chambers, and Gates, each with threat levels and flavoured descriptions
- **Ley lines** — directional, variable-strength lines connecting sites across the city
- **Factions** — eight types (covens, hermetic orders, government agencies, street cults, crime syndicates, otherworldly entities…) with goals, methods, threat levels, and inter-faction relationship webs
- **Reproducible seeds** — generate the same city again with the same integer seed
- **Full CRUD** — add, view, edit GM notes, and delete any element
- **JSON persistence** — cities save to `cities/<name>.json` and reload cleanly

---

## Requirements

- Python 3.10+
- No third-party dependencies

---

## Usage

```bash
python3 main.py
```

### Commands

| Command | Description |
|---|---|
| `new [seed]` | Generate a new city (optional integer seed) |
| `load` | Load a previously saved city |
| `list` | List all saved cities |
| `show` | City overview |
| `districts` | List / view districts |
| `sites` | List / view occult sites |
| `ley` | List / view ley lines |
| `factions` | List / view factions |
| `add district\|site\|ley\|faction` | Add a new element |
| `edit city\|district\|site\|ley\|faction` | Edit GM notes |
| `delete district\|site\|ley\|faction` | Remove an element |
| `save` | Save current city to disk |
| `help` | Show command reference |
| `quit` / `exit` | Exit (prompts to save) |

---

## Example Output

```
╔══ CITY: HALLOWBY ════════════════════════════════════════════════════════╗

    Hallowby is a university city of roughly 444,505 souls in Grimspire.
    It carries the weight of religious controversy and the air of collective
    amnesia.

    Region: The Grimspire Region, Grimspire
    Population: ~444,505
    Geography: Dense ancient woodland broken by quarries
    Occult reputation: Every census loses a small percentage of residents
    with no explanation.

  Current Events (Alt-1980s):
    A suspicious gas-main explosion has left a crater on Gallows Street
    for three months.

  Summary:
    6 districts  ·  8 occult sites  ·  3 ley lines  ·  5 factions
```

```
  Districts:
  1. Dunholm                        [Industrial      ]  Occult: ▮▮▮▮▮
  2. Kettleford                     [Industrial      ]  Occult: ▮▮▮▮▮
  3. Jericho                        [Industrial      ]  Occult: ▮▮▯▯▯
  4. Quarry Bank                    [Residential     ]  Occult: ▮▮▯▯▯
  5. Ironside                       [Residential     ]  Occult: ▮▮▮▮▮
  6. Nighthollow                    [Old Town        ]  Occult: ▮▮▯▯▯
```

```
  Occult Sites:
  1. Three Sisters Barrow           [Ancient Barrow     ]  Critical
  2. The Chalk Tunnel               [Underground Chamber]  Dormant
  3. The Seam                       [Gate               ]  Active
  4. The Nail of Heaven             [Astral Anchor      ]  Critical
  5. Old Meg                        [Standing Stone     ]  Dormant
  6. The Null Point                 [Ley Node           ]  Critical
```

```
  Factions:
  1. The Special Phenomena Unit         [Government Agency  ]  Stirring
  2. The Galloway Firm                  [Crime Syndicate    ]  Dormant
  3. The Pale Congregation              [Otherworldly Entity]  Active
  4. The Folklore Society (Irreg.)      [Academic Circle    ]  Dormant
```

---

## File Structure

```
.
├── models.py      # Dataclasses: City, Region, District, OccultSite,
│                  #   LeyLine, Faction, FactionRelationship + enums
├── generator.py   # CityGenerator — seeded random generation from
│                  #   curated UK/occult word tables
├── storage.py     # JSON save/load helpers
├── main.py        # Interactive REPL with ANSI colour
└── cities/        # Generated save files (git-ignored)
```

---

## Setting Notes

The game world sits in a Britain that diverged from ours sometime in the mid-20th century. The differences are subtle:

- The occult is real, and certain parts of the state know it
- Some ancient bargains between humans and land-spirits are still in force
- The 1980s economic disruption is happening, but it's mixed up with supernatural pressures that nobody is officially acknowledging
- Ley lines follow the old straight tracks; the new motorways have cut through several, with consequences

Cities generated by this tool are deliberately unnamed on the national map — drop them into any English county that suits your campaign.
