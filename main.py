#!/usr/bin/env python3
"""
Occult UK City Generator — Alternate 1980s TTRPG Tool
======================================================
Commands
--------
  new           Generate a new city
  load          Load a saved city
  list          List saved cities
  show          Display city overview
  districts     List / view districts
  sites         List / view occult sites
  ley           List / view ley lines
  factions      List / view factions
  add           Add a new element (district/site/faction/ley)
  edit          Edit notes on any element
  delete        Remove an element
  save          Save current city
  help          Show this help
  quit / exit   Exit the program
"""
import sys
import textwrap
from typing import Optional

from models import (
    City, District, OccultSite, LeyLine, Faction, FactionRelationship,
    DistrictType, OccultSiteType, FactionType, ThreatLevel, RelationshipType,
)
from generator import CityGenerator
from storage import save_city, load_city, list_cities

# ── ANSI colours ────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
PURPLE = "\033[35m"
WHITE  = "\033[37m"

THREAT_COLOUR = {
    ThreatLevel.DORMANT:  DIM + WHITE,
    ThreatLevel.STIRRING: YELLOW,
    ThreatLevel.ACTIVE:   RED,
    ThreatLevel.CRITICAL: BOLD + RED,
}


def c(colour: str, text: str) -> str:
    return f"{colour}{text}{RESET}"


def hr(char: str = "─", width: int = 72) -> str:
    return c(DIM, char * width)


def header(title: str) -> str:
    pad = max(0, 72 - len(title) - 4)
    return f"\n{c(BOLD + PURPLE, '╔══ ')}{c(BOLD, title)}{c(PURPLE, ' ' + '═' * pad + '╗')}"


def wrap(text: str, indent: int = 4) -> str:
    prefix = " " * indent
    return textwrap.fill(text, width=76, initial_indent=prefix, subsequent_indent=prefix)


def prompt(msg: str = "> ") -> str:
    try:
        return input(c(CYAN, msg)).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "quit"


def choose(options: list[str], label: str = "Choose") -> Optional[int]:
    for i, opt in enumerate(options, 1):
        print(f"  {c(CYAN, str(i)+'.')} {opt}")
    raw = prompt(f"{label} [1-{len(options)}]: ")
    if raw.lower() in ("q", "quit", "back", ""):
        return None
    try:
        idx = int(raw) - 1
        if 0 <= idx < len(options):
            return idx
        print(c(RED, "  Out of range."))
        return None
    except ValueError:
        print(c(RED, "  Enter a number."))
        return None


def choose_enum(enum_cls) -> Optional[object]:
    members = list(enum_cls)
    idx = choose([m.value for m in members], "Choose type")
    return members[idx] if idx is not None else None


# ── Display helpers ──────────────────────────────────────────────────────────

def display_city_overview(city: City) -> None:
    print(header(f"CITY: {city.name.upper()}"))
    print(wrap(city.description))
    print()
    print(wrap(f"Region: {city.region.name}, {city.region.county}"))
    print(wrap(f"Population: ~{city.population_approx:,}"))
    print(wrap(f"Geography: {city.region.geography}"))
    print(wrap(f"Occult reputation: {city.region.occult_reputation}"))
    print()
    print(c(BOLD, "  History:"))
    print(wrap(city.history))
    print()
    print(c(BOLD, "  Current Events (Alt-1980s):"))
    print(wrap(city.current_events))
    print()
    print(c(BOLD, "  Summary:"))
    print(wrap(f"{len(city.districts)} districts  ·  {len(city.occult_sites)} occult sites  ·  "
               f"{len(city.ley_lines)} ley lines  ·  {len(city.factions)} factions"))
    if city.notes:
        print()
        print(c(BOLD, "  GM Notes:"))
        print(wrap(city.notes))


def display_district(city: City, district: District) -> None:
    print(header(f"DISTRICT: {district.name}"))
    print(wrap(f"Type: {district.district_type.value}   Occult Activity: {'▮' * district.occult_activity + '▯' * (5 - district.occult_activity)} ({district.occult_activity}/5)"))
    print()
    print(wrap(district.atmosphere))
    print()
    print(c(BOLD, "  Population:"))
    print(wrap(district.population))
    print()
    print(c(BOLD, "  Notable Features:"))
    for feat in district.notable_features:
        print(f"    • {feat}")
    # Linked sites
    linked = [s for s in city.occult_sites if s.district_id == district.id]
    if linked:
        print()
        print(c(BOLD, "  Occult Sites in District:"))
        for s in linked:
            tc = THREAT_COLOUR.get(s.threat_level, RESET)
            print(f"    {c(tc, '●')} {s.name} [{s.site_type.value}] — {c(tc, s.threat_level.value)}")
    if district.notes:
        print()
        print(c(BOLD, "  GM Notes:"))
        print(wrap(district.notes))


def display_site(city: City, site: OccultSite) -> None:
    tc = THREAT_COLOUR.get(site.threat_level, RESET)
    print(header(f"SITE: {site.name}"))
    print(wrap(f"Type: {site.site_type.value}   Threat: {c(tc, site.threat_level.value)}"))
    district = city.get_district(site.district_id)
    if district:
        print(wrap(f"District: {district.name}"))
    print()
    print(wrap(site.description))
    if site.ley_line_ids:
        print()
        print(c(BOLD, "  Connected Ley Lines:"))
        for lid in site.ley_line_ids:
            ll = city.get_ley_line(lid)
            if ll:
                print(f"    • {ll.name} (strength {ll.strength}/5, {ll.direction})")
    if site.controlling_faction_id:
        f = city.get_faction(site.controlling_faction_id)
        if f:
            print()
            print(c(BOLD + RED, f"  Controlled by: {f.name}"))
    if site.notes:
        print()
        print(c(BOLD, "  GM Notes:"))
        print(wrap(site.notes))


def display_ley_line(city: City, ll: LeyLine) -> None:
    print(header(f"LEY LINE: {ll.name}"))
    print(wrap(f"Direction: {ll.direction}   Strength: {'▮' * ll.strength + '▯' * (5 - ll.strength)} ({ll.strength}/5)"))
    if ll.sites:
        print()
        print(c(BOLD, "  Connected Sites:"))
        for sid in ll.sites:
            s = city.get_site(sid)
            if s:
                tc = THREAT_COLOUR.get(s.threat_level, RESET)
                print(f"    • {s.name} [{s.site_type.value}] — {c(tc, s.threat_level.value)}")
    if ll.notes:
        print()
        print(c(BOLD, "  GM Notes:"))
        print(wrap(ll.notes))


def display_faction(city: City, faction: Faction) -> None:
    tc = THREAT_COLOUR.get(faction.threat_level, RESET)
    print(header(f"FACTION: {faction.name}"))
    print(wrap(f"Type: {faction.faction_type.value}   Threat: {c(tc, faction.threat_level.value)}"))
    print(wrap(f"Members: {faction.member_count}"))
    print()
    print(wrap(faction.description))
    print()
    print(c(BOLD, "  Goals:"))
    print(wrap(faction.goals))
    print()
    print(c(BOLD, "  Methods:"))
    print(wrap(faction.methods))
    if faction.hq_site_id:
        s = city.get_site(faction.hq_site_id)
        if s:
            print()
            print(wrap(f"HQ: {s.name} [{s.site_type.value}]"))
    if faction.relationships:
        print()
        print(c(BOLD, "  Known Relationships:"))
        for rel in faction.relationships:
            other = city.get_faction(rel.faction_id)
            if other:
                rel_colours = {
                    RelationshipType.ALLIED:  GREEN,
                    RelationshipType.NEUTRAL: WHITE,
                    RelationshipType.RIVAL:   YELLOW,
                    RelationshipType.HOSTILE: RED,
                    RelationshipType.PUPPET:  PURPLE,
                    RelationshipType.UNKNOWN: DIM,
                }
                rc = rel_colours.get(rel.relationship, WHITE)
                print(f"    {c(rc, rel.relationship.value):20}  {other.name}")
    if faction.notes:
        print()
        print(c(BOLD, "  GM Notes:"))
        print(wrap(faction.notes))


# ── Input helpers ────────────────────────────────────────────────────────────

def ask(label: str, default: str = "") -> str:
    if default:
        raw = prompt(f"  {label} [{default}]: ")
        return raw if raw else default
    return prompt(f"  {label}: ")


def ask_int(label: str, lo: int = 1, hi: int = 5, default: int = 1) -> int:
    raw = prompt(f"  {label} ({lo}–{hi}) [{default}]: ")
    if not raw:
        return default
    try:
        val = int(raw)
        return max(lo, min(hi, val))
    except ValueError:
        return default


# ── CRUD operations ──────────────────────────────────────────────────────────

def add_district(city: City) -> None:
    print(c(BOLD, "\n  Add District"))
    name = ask("Name")
    if not name:
        return
    print("  District type:")
    dtype = choose_enum(DistrictType)
    if dtype is None:
        return
    atmosphere = ask("Atmosphere (one sentence)", "Drizzle and silence.")
    occult = ask_int("Occult Activity (1–5)", default=1)
    features_raw = ask("Notable features (comma-separated)")
    features = [f.strip() for f in features_raw.split(",") if f.strip()]
    notes = ask("GM Notes")
    d = District(
        name=name, district_type=dtype, description=atmosphere,
        atmosphere=atmosphere, notable_features=features,
        occult_activity=occult,
        population="Unknown.",
        notes=notes,
    )
    city.districts.append(d)
    print(c(GREEN, f"  District '{name}' added (id: {d.id})."))


def add_site(city: City) -> None:
    print(c(BOLD, "\n  Add Occult Site"))
    name = ask("Name")
    if not name:
        return
    print("  Site type:")
    stype = choose_enum(OccultSiteType)
    if stype is None:
        return
    print("  Threat level:")
    threat = choose_enum(ThreatLevel)
    if threat is None:
        return
    desc = ask("Description")

    district_id = ""
    if city.districts:
        print("  District:")
        idx = choose([d.name for d in city.districts] + ["(none)"], "Assign to")
        if idx is not None and idx < len(city.districts):
            district_id = city.districts[idx].id

    notes = ask("GM Notes")
    s = OccultSite(
        name=name, site_type=stype, district_id=district_id,
        description=desc, threat_level=threat, notes=notes,
    )
    city.occult_sites.append(s)
    print(c(GREEN, f"  Site '{name}' added (id: {s.id})."))


def add_ley_line(city: City) -> None:
    print(c(BOLD, "\n  Add Ley Line"))
    name = ask("Name")
    if not name:
        return
    direction = ask("Direction (e.g. N to S)", "N to S")
    strength = ask_int("Strength (1–5)", default=3)
    notes = ask("GM Notes")
    ll = LeyLine(name=name, direction=direction, strength=strength, notes=notes)

    if city.occult_sites:
        print("  Connect sites (enter site numbers, blank to skip):")
        for i, s in enumerate(city.occult_sites, 1):
            print(f"    {c(CYAN, str(i)+'.')} {s.name}")
        raw = prompt("  Numbers (space-separated): ")
        for tok in raw.split():
            try:
                idx = int(tok) - 1
                if 0 <= idx < len(city.occult_sites):
                    site = city.occult_sites[idx]
                    if ll.id not in site.ley_line_ids:
                        site.ley_line_ids.append(ll.id)
                    if site.id not in ll.sites:
                        ll.sites.append(site.id)
            except ValueError:
                pass

    city.ley_lines.append(ll)
    print(c(GREEN, f"  Ley line '{name}' added (id: {ll.id})."))


def add_faction(city: City) -> None:
    print(c(BOLD, "\n  Add Faction"))
    name = ask("Name")
    if not name:
        return
    print("  Faction type:")
    ftype = choose_enum(FactionType)
    if ftype is None:
        return
    print("  Threat level:")
    threat = choose_enum(ThreatLevel)
    if threat is None:
        return
    desc = ask("Description")
    goals = ask("Goals")
    methods = ask("Methods")
    members = ask("Member count descriptor", "Unknown")
    notes = ask("GM Notes")

    hq_site_id = None
    if city.occult_sites:
        raw = prompt("  HQ site? (y/n): ")
        if raw.lower() == "y":
            idx = choose([s.name for s in city.occult_sites], "HQ Site")
            if idx is not None:
                hq_site_id = city.occult_sites[idx].id

    f = Faction(
        name=name, faction_type=ftype, description=desc, goals=goals,
        methods=methods, threat_level=threat, hq_site_id=hq_site_id,
        member_count=members, notes=notes,
    )
    city.factions.append(f)
    print(c(GREEN, f"  Faction '{name}' added (id: {f.id})."))


def edit_notes(obj) -> None:
    print(c(DIM, f"  Current notes: {obj.notes or '(none)'}"))
    new_notes = prompt("  New notes (blank to clear, ENTER to keep): ")
    if new_notes == "":
        keep = prompt("  Clear existing notes? (y/n): ")
        if keep.lower() == "y":
            obj.notes = ""
            print(c(GREEN, "  Notes cleared."))
    else:
        obj.notes = new_notes
        print(c(GREEN, "  Notes updated."))


def delete_element(city: City, collection_name: str) -> None:
    collections = {
        "districts": city.districts,
        "sites": city.occult_sites,
        "ley": city.ley_lines,
        "factions": city.factions,
    }
    coll = collections.get(collection_name)
    if not coll:
        print(c(RED, "  Unknown collection."))
        return
    names = [getattr(x, "name", str(x)) for x in coll]
    idx = choose(names, "Delete which")
    if idx is None:
        return
    item = coll[idx]
    confirm = prompt(f"  Delete '{item.name}'? (yes/no): ")
    if confirm.lower() == "yes":
        coll.pop(idx)
        print(c(GREEN, f"  Deleted '{item.name}'."))
    else:
        print("  Cancelled.")


# ── Main REPL ────────────────────────────────────────────────────────────────

BANNER = f"""
{c(BOLD + PURPLE, '╔══════════════════════════════════════════════════════════════════════╗')}
{c(BOLD + PURPLE, '║')}  {c(BOLD, 'OCCULT UK CITY GENERATOR')}  {c(DIM, '— Alternate 1980s Edition')}                  {c(BOLD + PURPLE, '║')}
{c(BOLD + PURPLE, '║')}  {c(DIM, 'A tool for TTRPG game masters.')}  Type {c(CYAN, 'help')} to begin.               {c(BOLD + PURPLE, '║')}
{c(BOLD + PURPLE, '╚══════════════════════════════════════════════════════════════════════╝')}
"""

HELP_TEXT = f"""
{c(BOLD, 'Commands:')}

  {c(CYAN, 'new [seed]')}       Generate a new city (optional integer seed for reproducibility)
  {c(CYAN, 'load')}             Load a previously saved city
  {c(CYAN, 'list')}             List all saved cities
  {c(CYAN, 'show')}             City overview
  {c(CYAN, 'districts')}        List / view districts
  {c(CYAN, 'sites')}            List / view occult sites
  {c(CYAN, 'ley')}              List / view ley lines
  {c(CYAN, 'factions')}         List / view factions
  {c(CYAN, 'add district')}     Add a new district
  {c(CYAN, 'add site')}         Add a new occult site
  {c(CYAN, 'add ley')}          Add a new ley line
  {c(CYAN, 'add faction')}      Add a new faction
  {c(CYAN, 'edit district')}    Edit GM notes on a district
  {c(CYAN, 'edit site')}        Edit GM notes on a site
  {c(CYAN, 'edit ley')}         Edit GM notes on a ley line
  {c(CYAN, 'edit faction')}     Edit GM notes on a faction
  {c(CYAN, 'edit city')}        Edit city-level GM notes
  {c(CYAN, 'delete district')}  Delete a district
  {c(CYAN, 'delete site')}      Delete a site
  {c(CYAN, 'delete ley')}       Delete a ley line
  {c(CYAN, 'delete faction')}   Delete a faction
  {c(CYAN, 'save')}             Save current city to disk
  {c(CYAN, 'help')}             Show this message
  {c(CYAN, 'quit')} / {c(CYAN, 'exit')}     Exit
"""


def cmd_new(args: list[str], _city: Optional[City]) -> Optional[City]:
    seed = None
    if args:
        try:
            seed = int(args[0])
        except ValueError:
            print(c(YELLOW, "  Seed must be an integer — ignoring."))
    raw_districts = prompt("  Number of districts [6]: ")
    raw_sites     = prompt("  Number of occult sites [8]: ")
    raw_ley       = prompt("  Number of ley lines [3]: ")
    raw_factions  = prompt("  Number of factions [5]: ")

    def parse(raw, default):
        try:
            return max(1, int(raw)) if raw else default
        except ValueError:
            return default

    gen = CityGenerator(seed=seed)
    city = gen.generate_city(
        num_districts=parse(raw_districts, 6),
        num_sites=parse(raw_sites, 8),
        num_ley_lines=parse(raw_ley, 3),
        num_factions=parse(raw_factions, 5),
    )
    print(c(GREEN, f"\n  Generated: {city.name}"))
    display_city_overview(city)
    return city


def cmd_load(_args, _city) -> Optional[City]:
    cities = list_cities()
    if not cities:
        print(c(YELLOW, "  No saved cities found."))
        return None
    idx = choose([p.stem for p in cities], "Load city")
    if idx is None:
        return None
    city = load_city(cities[idx])
    print(c(GREEN, f"  Loaded: {city.name}"))
    return city


def cmd_list(_args, _city) -> None:
    cities = list_cities()
    if not cities:
        print(c(YELLOW, "  No saved cities."))
        return
    print(c(BOLD, "\n  Saved cities:"))
    for p in cities:
        print(f"    • {p.stem}  {c(DIM, str(p))}")


def cmd_districts(city: City) -> None:
    if not city.districts:
        print(c(YELLOW, "  No districts defined."))
        return
    print(c(BOLD, "\n  Districts:"))
    for i, d in enumerate(city.districts, 1):
        bar = "▮" * d.occult_activity + "▯" * (5 - d.occult_activity)
        print(f"  {c(CYAN, str(i)+'.')} {d.name:30} [{d.district_type.value:15}]  Occult: {bar}")
    print()
    raw = prompt("  View detail? [number / enter to skip]: ")
    if raw:
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(city.districts):
                display_district(city, city.districts[idx])
        except ValueError:
            pass


def cmd_sites(city: City) -> None:
    if not city.occult_sites:
        print(c(YELLOW, "  No occult sites defined."))
        return
    print(c(BOLD, "\n  Occult Sites:"))
    for i, s in enumerate(city.occult_sites, 1):
        tc = THREAT_COLOUR.get(s.threat_level, RESET)
        print(f"  {c(CYAN, str(i)+'.')} {s.name:35} [{s.site_type.value:20}]  {c(tc, s.threat_level.value)}")
    print()
    raw = prompt("  View detail? [number / enter to skip]: ")
    if raw:
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(city.occult_sites):
                display_site(city, city.occult_sites[idx])
        except ValueError:
            pass


def cmd_ley(city: City) -> None:
    if not city.ley_lines:
        print(c(YELLOW, "  No ley lines defined."))
        return
    print(c(BOLD, "\n  Ley Lines:"))
    for i, ll in enumerate(city.ley_lines, 1):
        bar = "▮" * ll.strength + "▯" * (5 - ll.strength)
        print(f"  {c(CYAN, str(i)+'.')} {ll.name:35} {ll.direction:12}  Strength: {bar}  Sites: {len(ll.sites)}")
    print()
    raw = prompt("  View detail? [number / enter to skip]: ")
    if raw:
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(city.ley_lines):
                display_ley_line(city, city.ley_lines[idx])
        except ValueError:
            pass


def cmd_factions(city: City) -> None:
    if not city.factions:
        print(c(YELLOW, "  No factions defined."))
        return
    print(c(BOLD, "\n  Factions:"))
    for i, f in enumerate(city.factions, 1):
        tc = THREAT_COLOUR.get(f.threat_level, RESET)
        print(f"  {c(CYAN, str(i)+'.')} {f.name:40} [{f.faction_type.value:20}]  {c(tc, f.threat_level.value)}")
    print()
    raw = prompt("  View detail? [number / enter to skip]: ")
    if raw:
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(city.factions):
                display_faction(city, city.factions[idx])
        except ValueError:
            pass


def require_city(city: Optional[City]) -> bool:
    if city is None:
        print(c(YELLOW, "  No city loaded. Use 'new' or 'load' first."))
        return False
    return True


def run() -> None:
    print(BANNER)
    city: Optional[City] = None

    while True:
        raw = prompt(f"\n[{city.name if city else 'no city'}] > ")
        parts = raw.strip().split()
        if not parts:
            continue
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ("quit", "exit", "q"):
            if city:
                raw2 = prompt("  Save before quitting? (y/n): ")
                if raw2.lower() == "y":
                    path = save_city(city)
                    print(c(GREEN, f"  Saved to {path}"))
            print(c(DIM, "  Farewell."))
            sys.exit(0)

        elif cmd == "help":
            print(HELP_TEXT)

        elif cmd == "new":
            city = cmd_new(args, city)

        elif cmd == "load":
            loaded = cmd_load(args, city)
            if loaded:
                city = loaded

        elif cmd == "list":
            cmd_list(args, city)

        elif cmd == "save":
            if require_city(city):
                path = save_city(city)
                print(c(GREEN, f"  Saved to {path}"))

        elif cmd == "show":
            if require_city(city):
                display_city_overview(city)

        elif cmd == "districts":
            if require_city(city):
                cmd_districts(city)

        elif cmd == "sites":
            if require_city(city):
                cmd_sites(city)

        elif cmd == "ley":
            if require_city(city):
                cmd_ley(city)

        elif cmd == "factions":
            if require_city(city):
                cmd_factions(city)

        elif cmd == "add":
            if require_city(city):
                sub = args[0].lower() if args else ""
                if sub == "district":
                    add_district(city)
                elif sub == "site":
                    add_site(city)
                elif sub == "ley":
                    add_ley_line(city)
                elif sub == "faction":
                    add_faction(city)
                else:
                    print(c(YELLOW, "  Usage: add [district|site|ley|faction]"))

        elif cmd == "edit":
            if require_city(city):
                sub = args[0].lower() if args else ""
                if sub == "city":
                    edit_notes(city)
                elif sub == "district":
                    if city.districts:
                        idx = choose([d.name for d in city.districts], "Edit district")
                        if idx is not None:
                            edit_notes(city.districts[idx])
                    else:
                        print(c(YELLOW, "  No districts."))
                elif sub == "site":
                    if city.occult_sites:
                        idx = choose([s.name for s in city.occult_sites], "Edit site")
                        if idx is not None:
                            edit_notes(city.occult_sites[idx])
                    else:
                        print(c(YELLOW, "  No sites."))
                elif sub == "ley":
                    if city.ley_lines:
                        idx = choose([l.name for l in city.ley_lines], "Edit ley line")
                        if idx is not None:
                            edit_notes(city.ley_lines[idx])
                    else:
                        print(c(YELLOW, "  No ley lines."))
                elif sub == "faction":
                    if city.factions:
                        idx = choose([f.name for f in city.factions], "Edit faction")
                        if idx is not None:
                            edit_notes(city.factions[idx])
                    else:
                        print(c(YELLOW, "  No factions."))
                else:
                    print(c(YELLOW, "  Usage: edit [city|district|site|ley|faction]"))

        elif cmd == "delete":
            if require_city(city):
                sub = args[0].lower() if args else ""
                if sub in ("district", "site", "ley", "faction"):
                    delete_element(city, sub)
                else:
                    print(c(YELLOW, "  Usage: delete [district|site|ley|faction]"))

        else:
            print(c(YELLOW, f"  Unknown command '{cmd}'. Type 'help' for commands."))


if __name__ == "__main__":
    run()
