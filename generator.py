"""
Random generator for UK occult cities (alternate 1980s setting).
"""
import random
from typing import Optional
from models import (
    City, Region, District, OccultSite, LeyLine, Faction,
    FactionRelationship, DistrictType, OccultSiteType, FactionType,
    ThreatLevel, RelationshipType,
)

# ---------------------------------------------------------------------------
# Word lists
# ---------------------------------------------------------------------------

_CITY_PREFIXES = [
    "Ash", "Black", "Brim", "Cold", "Crow", "Dark", "Dun", "Elder",
    "Fenn", "Grim", "Hallow", "Hollow", "Iron", "Moor", "Nether",
    "Old", "Raven", "Salt", "Stone", "Thorn", "Wither", "Wraith",
]
_CITY_SUFFIXES = [
    "borough", "bridge", "burn", "bury", "by", "caster", "church",
    "dale", "field", "ford", "gate", "ham", "haven", "heath", "hull",
    "hurst", "ley", "mere", "mouth", "pool", "wick", "worth",
]

_DISTRICT_NAMES = [
    "Aldgate", "Benwick", "Blackmere", "Caldwick", "Charnfield",
    "Crookbridge", "Dunholm", "Eastgate", "Ferncross", "Gallowshill",
    "Greystone", "Hawthorn End", "Ironside", "Jericho", "Kettleford",
    "Lowgate", "Marshgate", "Nighthollow", "Old Ditch", "Pilgrim Row",
    "Quarry Bank", "Rookwood", "Saltburn", "Thornhaven", "Undergate",
    "Vestry Lane", "Wailing Row", "Ximena Cross", "Yew Tree Green", "Zeal Hollow",
]

_COUNTIES = [
    "Albionshire", "Bremenshire", "Caldorshire", "Dunmoreshire",
    "Eastmarch", "Fenshire", "Grimspire", "Hartwell County",
    "Ironwick County", "Jarrowdale",
]

_REGION_GEOGRAPHY = [
    "Low-lying fens and silted river channels",
    "Grimy post-industrial moorland scored by rail cuttings",
    "Limestone plateau riddled with caves and sink-holes",
    "Wide estuary mudflats beneath leaden skies",
    "Dense ancient woodland broken by quarries",
    "Coastal cliffs and shingle beaches shrouded in sea-mist",
    "Former coal-field valley towns strung along a river",
    "Rolling chalk downs cut by prehistoric drove roads",
    "Marshland reclaimed by drains and pumping stations",
    "Urban sprawl abutting a dark and reputedly haunted forest",
]

_REGION_OCCULT = [
    "A place where the veil between worlds has always been thin.",
    "Witchcraft trials in the 17th century left deep psychic scars.",
    "Said to be the convergence point of three ancient ley lines.",
    "Locals speak in hushed tones of the Hollow Men seen at crossroads.",
    "Every census loses a small percentage of residents with no explanation.",
    "Folk memory of a pre-Christian cult persists in festival customs.",
    "The Church of England has quietly suppressed records of local 'incidents'.",
    "Amateur occultists have been arriving since a 1970s BBC documentary.",
    "MI5 maintains a small, deniable listening post monitoring 'unusual activity'.",
    "Strange lights have been reported over the moors since Roman times.",
]

_ATMOSPHERE = [
    "Perpetual drizzle, sodium-orange streetlamps, the smell of coal smoke.",
    "Sunday-quiet streets, net curtains twitching, the distant bark of a dog.",
    "Punks and skinheads jostle at the precinct; NF graffiti on the underpass.",
    "Terraced houses, garden walls crumbling, satellite dishes yet to arrive.",
    "Industrial fog rolls in from the canal; the air tastes of rust.",
    "Brutalist tower blocks loom over a derelict market square.",
    "Cobblestoned alleys between Victorian warehouses; gaslights still fitted.",
    "Strike pickets outside the plant gates; police transit vans parked nearby.",
    "A half-demolished high street, squatters in the boarded-up Woolworths.",
    "Quiet Georgian terraces where academics and occultists share dinner tables.",
]

_DISTRICT_FEATURES = [
    "An abandoned textile mill repurposed as squats",
    "A Victorian cemetery overgrown with elder and yew",
    "A 1960s shopping precinct stained by years of rain",
    "A canal basin with moored narrowboats of dubious provenance",
    "A working mens' club frequented by lodge members",
    "A council estate with a notorious lift-shaft rumoured to be haunted",
    "A covered market where contraband herbs are openly sold",
    "A deconsecrated chapel converted to a nightclub",
    "An old police 'black museum' in the station basement",
    "A bookshop specialising in occult and banned political texts",
    "A disused railway station sealed with chains and warnings",
    "A Victorian public baths still in use, with a peculiar basement pool",
    "A newspaper office whose archives go suspiciously dark for 1963–67",
    "A post office that has never been fully explained in planning records",
    "A grim tower block with the top two floors permanently cordoned off",
]

_SITE_NAMES = {
    OccultSiteType.LEY_NODE: [
        "The Blind Crossing", "Hag's Elbow", "The Null Point",
        "Gallows Confluence", "The Spinning Place",
    ],
    OccultSiteType.BARROW: [
        "Gibbeting Hill", "The Long Barrow of Ealdwic", "Worm's Hump",
        "The Sleeping King's Mound", "Three Sisters Barrow",
    ],
    OccultSiteType.STANDING_STONE: [
        "The Stump", "Witchfinger Stone", "The Grey Man",
        "Old Meg", "The Preaching Stone",
    ],
    OccultSiteType.CURSED_CHURCH: [
        "St Aelred's, Blackgate", "The Church of the Annulled",
        "Our Lady of Perpetual Sorrow", "St Ignatius of the Marsh",
        "The Ruin of St Wulfric's",
    ],
    OccultSiteType.HAUNTED_PUB: [
        "The Hanged Reeve", "The Bellman's Arms", "The Quiet Shepherd",
        "The Hollow Crown", "The Stumps Inn",
    ],
    OccultSiteType.UNDERGROUND_CHAMBER: [
        "The Lazar Vault", "The Counting Room", "Mithraeum Beneath Broad Street",
        "The Chalk Tunnel", "The Charnel Repository",
    ],
    OccultSiteType.RITUAL_SITE: [
        "The Ring of Charred Earth", "The Unmarked Clearing",
        "Hexworthy Hollow", "The Scored Floor", "The Burning Ground",
    ],
    OccultSiteType.MIRROR_POOL: [
        "Black Mere", "The Staring Pool", "Nunpool",
        "The Drowned Face", "Lady's Mirror",
    ],
    OccultSiteType.WITCHES_MARKET: [
        "Rag-and-Bone Alley", "Mother Croft's Passage",
        "The Thursday Stalls", "The Cunning Market", "Wisewomen's Row",
    ],
    OccultSiteType.FORGOTTEN_SHRINE: [
        "The Hollow in the Wall", "St Nobody's Niche",
        "The Votive Alcove", "The Bone Chapel", "The Painted Cellar",
    ],
    OccultSiteType.ALCHEMY_WORKSHOP: [
        "Furnival's Back Room", "The Philosopher's Flat",
        "The Retort on Irongate", "Dr Mourne's Lab", "The Still Works",
    ],
    OccultSiteType.ASTRAL_ANCHOR: [
        "The Tethering Stone", "The Dreamer's Plinth",
        "The Nail of Heaven", "The Copper Disc", "The Anchor Chain",
    ],
    OccultSiteType.GATE: [
        "The Old Toll Gate", "The Veil Door", "The Between Place",
        "The Opened Arch", "The Seam",
    ],
}

_SITE_DESCRIPTIONS = {
    OccultSiteType.LEY_NODE: [
        "Three lines of earth-energy converge here; compasses spin and dogs refuse to approach.",
        "A patch of ground where nothing grows, inexplicably warm in winter.",
        "Standing here at dawn brings visions of the land before enclosure.",
    ],
    OccultSiteType.BARROW: [
        "A grass-covered mound predating the Romans, never fully excavated.",
        "Local children dare each other to sleep atop it; none who do sleep soundly again.",
        "The archaeology department stopped digging here in 1974 after three students vanished.",
    ],
    OccultSiteType.STANDING_STONE: [
        "An eight-foot grey monolith of unknown origin. The council wants it moved; the stone disagrees.",
        "Inscribed with marks that don't match any known script but resemble something older.",
        "Folklore says it walks to the river and back every Midsummer Eve.",
    ],
    OccultSiteType.CURSED_CHURCH: [
        "A Church of England parish that hasn't had a permanent vicar since 1971.",
        "The east window depicts saints nobody has ever been able to identify.",
        "Services are still held but the congregation is dwindling, and pale.",
    ],
    OccultSiteType.HAUNTED_PUB: [
        "The landlord won't discuss the cellar. The regulars won't discuss the landlord.",
        "A CAMRA-listed free house where the back bar is always colder than the rest.",
        "Photographs taken here often show an extra person who wasn't there.",
    ],
    OccultSiteType.UNDERGROUND_CHAMBER: [
        "An undocumented Victorian tunnel system that doesn't appear on any council map.",
        "Discovered during roadworks in 1982; sealed again within a week by men in plain clothes.",
        "Roman construction on top of something older. Much older.",
    ],
    OccultSiteType.RITUAL_SITE: [
        "The grass here is scorched in a precise geometric pattern that regrows the same way every year.",
        "Used by a group whose membership overlaps disconcertingly with the local council.",
        "Abandoned paraphernalia collected here has a habit of disappearing from evidence lockers.",
    ],
    OccultSiteType.MIRROR_POOL: [
        "A still, peat-dark pool that reflects the sky even on cloudy days.",
        "Bodies deposited here for millennia; some are offered willingly.",
        "The reflection always shows the pool in a different season than the one you're standing in.",
    ],
    OccultSiteType.WITCHES_MARKET: [
        "A Tuesday stall that sells herbs, bones, and things in jars, alongside the regular veg.",
        "The sellers seem to know your name before you give it.",
        "Licensed by the council as a 'craft market'; the council's planning officer has since retired to somewhere unspecified.",
    ],
    OccultSiteType.FORGOTTEN_SHRINE: [
        "A niche in a wall that no planning record mentions, pre-dating the wall itself.",
        "Offerings are left regularly; nobody admits to leaving them.",
        "The face carved here was described as pre-Roman but resembles no known deity.",
    ],
    OccultSiteType.ALCHEMY_WORKSHOP: [
        "A terraced house whose owner runs it as a 'chemistry tutor' service.",
        "The smell changes by day: sulphur on Mondays, roses on Fridays.",
        "Equipment dates from three separate centuries, all of it functional.",
    ],
    OccultSiteType.ASTRAL_ANCHOR: [
        "A heavy stone object of ambiguous function that stops things drifting between planes.",
        "Dreamers in the area all share one recurring location they call 'the tethered place'.",
        "Moving it caused three weeks of poltergeist activity across the whole neighbourhood.",
    ],
    OccultSiteType.GATE: [
        "An archway that opens onto a different place depending on what you're carrying.",
        "Active only at certain hours; locals know not to use that alleyway after dark.",
        "The other side isn't the same city. It isn't the same year, either.",
    ],
}

_FACTION_NAMES = {
    FactionType.COVEN: [
        "The Circle of the Scouring Wind", "The Hearthbound Thirteen",
        "Daughters of the Black Hag", "The Waxing Compact",
        "The Thornwood Assembly",
    ],
    FactionType.HERMETIC_ORDER: [
        "The Invisible College (Northern Chapter)", "The Order of the Ashen Rose",
        "Lodge Malkuth", "The Hyperborean Fellowship",
        "The Seekers of the Unwritten Law",
    ],
    FactionType.GOVERNMENT_AGENCY: [
        "Department S (Suppression)", "The Special Phenomena Unit",
        "The Crown's Irregulars", "Branch Null",
        "The Registry of Unusual Occurrences",
    ],
    FactionType.CHURCH_SECT: [
        "The Penitent Watchers", "The Order of St Wulfric",
        "The Ecumenical Anomaly Board", "The Reclaimers",
        "The Society of the Sacred Threshold",
    ],
    FactionType.STREET_CULT: [
        "The Moth Boys", "The Hollow Church",
        "The Rust Gospel", "Children of the Blind Eye",
        "The Lash Congregation",
    ],
    FactionType.ACADEMIC_CIRCLE: [
        "The Dunholme Parapsychology Group", "The Folklore Society (Irregular Session)",
        "The Anomalous History Collective", "The Unexplained Phenomena Seminar",
        "Professor Aldring's Tuesday Circle",
    ],
    FactionType.CRIME_SYNDICATE: [
        "The Galloway Firm", "The Salt Road Crew",
        "The Long Hammers", "Whittaker & Sons (Import/Export)",
        "The Midnight Charter",
    ],
    FactionType.OTHERWORLDLY: [
        "The Bound Ones", "The Harrowmen",
        "The Pale Congregation", "The Sleepers-Who-Walk",
        "The Unnamed Compact",
    ],
}

_FACTION_GOALS = {
    FactionType.COVEN: [
        "Maintain the old bargains with the land-spirits before the developers destroy the last sites.",
        "Identify and recruit the new generation of witches before a rival faction does.",
        "Prevent a long-sealed Gate from being reopened by well-meaning amateurs.",
    ],
    FactionType.HERMETIC_ORDER: [
        "Complete the Great Work before the century turns and the stars align against it.",
        "Recover a stolen grimoire currently in the hands of a government department.",
        "Establish a new astral anchor to replace one destroyed in 1941 by a bombing raid.",
    ],
    FactionType.GOVERNMENT_AGENCY: [
        "Contain and suppress all public knowledge of occult activity in the region.",
        "Weaponise or neutralise a newly discovered ley node before foreign powers find it.",
        "Compile a census of all active practitioners for future 'management'.",
    ],
    FactionType.CHURCH_SECT: [
        "Perform a binding ritual to keep something from crossing the threshold permanently.",
        "Retrieve holy relics that were sold off during church closures and are now causing problems.",
        "Convert or neutralise a coven occupying a church ruin they consider sacred ground.",
    ],
    FactionType.STREET_CULT: [
        "Open the Gate without understanding what will come through it.",
        "Accumulate enough sacrifice to wake their god from beneath the estate.",
        "Prove their devotion by eliminating a faction they see as heretical.",
    ],
    FactionType.ACADEMIC_CIRCLE: [
        "Document everything before the evidence disappears or is suppressed.",
        "Achieve genuine peer-reviewed publication of proof of the paranormal.",
        "Stop a colleague from doing something catastrophic in the name of research.",
    ],
    FactionType.CRIME_SYNDICATE: [
        "Monopolise the trade in occult materials and services in the region.",
        "Use knowledge of the supernatural as leverage against rivals and officials.",
        "Keep the city stable enough to profit from — no apocalypses, please.",
    ],
    FactionType.OTHERWORLDLY: [
        "Re-establish a foothold in the mortal world after centuries of exile.",
        "Gather enough belief-energy to manifest fully without a host.",
        "Prevent their ancient enemies from doing the same.",
    ],
}

_FACTION_METHODS = {
    FactionType.COVEN: "Ritual work, herbalism, community protection, occasional prophetic intervention.",
    FactionType.HERMETIC_ORDER: "Ceremonial magic, scholarly research, cautious recruitment of suitable candidates.",
    FactionType.GOVERNMENT_AGENCY: "Surveillance, disinformation, suppression, occasional wet work.",
    FactionType.CHURCH_SECT: "Prayer, exorcism, infiltration of parishes, manipulation of church hierarchy.",
    FactionType.STREET_CULT: "Coercion, street-level recruitment, violence, reckless ritual.",
    FactionType.ACADEMIC_CIRCLE: "Research, observation, publication attempts, cautious field-work.",
    FactionType.CRIME_SYNDICATE: "Bribery, intimidation, black-market logistics, protection rackets.",
    FactionType.OTHERWORLDLY: "Possession, dreams, manipulation through proxies, long games spanning centuries.",
}

_MEMBER_COUNTS = [
    "Three or four core members, wider circle unknown",
    "A dozen committed members, perhaps fifty fellow-travellers",
    "Twenty active operatives, backed by a shadowy support structure",
    "Unknown — estimates range from six to sixty",
    "A single known face; the full extent of the organisation is unclear",
    "Hundreds of nominal members, only a handful know the truth",
]

_LEY_DIRECTIONS = [
    "N to S", "NE to SW", "E to W", "SE to NW",
    "NNE to SSW", "ENE to WSW",
]

_LEY_NAMES = [
    "The Watcher's Road", "The Hag's Path", "The Old Straight",
    "The Blind Way", "The Corpse Road", "The Dragon's Vein",
    "The Pale Line", "The Unseen Meridian", "The Bone Track",
    "The Sleeping Shepherd's Route",
]

_CURRENT_EVENTS = [
    "Miners' strike solidarity marches clash with police near the town hall.",
    "A suspicious gas-main explosion has left a crater on Gallows Street for three months.",
    "The local MP is under investigation for accepting gifts from an unnamed 'heritage trust'.",
    "A series of animal mutilations in the north district; police attribute it to 'ritual abuse'.",
    "The new shopping centre development threatens to demolish the oldest part of the old town.",
    "A BBC crew filming a docudrama about folk customs has gone curiously native.",
    "Unusual radio interference has been blocking all transmissions within a quarter-mile radius of the canal.",
    "Three teenagers missing from the council estate; their parents say the police aren't trying.",
    "A local newspaper ran a headline about 'devil worship' and has since been bought by a national.",
    "Council minutes from 1962–1966 have been declared lost; a clerk retired immediately after.",
]

_POPULATION_DESCRIPTORS = {
    DistrictType.INDUSTRIAL: "Working-class, mostly employed or recently redundant; tight-knit.",
    DistrictType.RESIDENTIAL: "Mixed; older families alongside young professionals priced out of the south.",
    DistrictType.COMMERCIAL: "Daytime population of office workers; few permanent residents.",
    DistrictType.DOCKLANDS: "Declining longshore community; immigrants and students filling the vacancies.",
    DistrictType.UNIVERSITY: "Students and lecturers; high turnover; eccentric permanent residents.",
    DistrictType.OLD_TOWN: "A dwindling settled community; some families have been here for centuries.",
    DistrictType.COUNCIL_ESTATE: "Dense; high unemployment; strong local identity; distrustful of outsiders.",
    DistrictType.SUBURB: "Lower-middle class; aspirational; curtain-twitching; politically volatile.",
    DistrictType.PARKLAND: "Almost none; groundskeepers and the occasional rough-sleeper.",
    DistrictType.ECCLESIASTICAL: "Clergy, scholars, and the quietly devout; secretive about parish business.",
}


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class CityGenerator:
    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)

    def _pick(self, seq):
        return self.rng.choice(seq)

    def _picks(self, seq, k):
        return self.rng.sample(seq, min(k, len(seq)))

    # --- sub-generators ---

    def generate_region(self) -> Region:
        county = self._pick(_COUNTIES)
        return Region(
            name=f"The {county} Region",
            county=county,
            description=f"A {self._pick(['grimly', 'quietly', 'notoriously', 'nominally'])} "
                        f"{self._pick(['unremarkable', 'depressed', 'prosperous', 'contested'])} "
                        f"part of England, known for its {self._pick(['mills', 'mines', 'moorland', 'ports', 'universities'])}.",
            geography=self._pick(_REGION_GEOGRAPHY),
            history=(
                f"Settled since the {self._pick(['Bronze Age', 'Iron Age', 'Roman period', 'Dark Ages', 'Norman Conquest'])}, "
                f"it industrialised rapidly in the {self._pick(['late 18th', '19th', 'early 20th'])} century "
                f"and has been in {self._pick(['slow', 'rapid', 'patchy', 'contested'])} decline since."
            ),
            occult_reputation=self._pick(_REGION_OCCULT),
        )

    def generate_district(self, used_names: set) -> District:
        avail = [n for n in _DISTRICT_NAMES if n not in used_names]
        name = self._pick(avail) if avail else f"District {self.rng.randint(1, 99)}"
        dtype = self._pick(list(DistrictType))
        features = self._picks(_DISTRICT_FEATURES, self.rng.randint(2, 4))
        return District(
            name=name,
            district_type=dtype,
            description=(
                f"A {self._pick(['sprawling', 'tight', 'declining', 'lively', 'forgotten'])} "
                f"{dtype.value.lower()} district characterised by {self._pick(_ATMOSPHERE).lower()}"
            ),
            atmosphere=self._pick(_ATMOSPHERE),
            notable_features=features,
            occult_activity=self.rng.randint(1, 5),
            population=_POPULATION_DESCRIPTORS[dtype],
        )

    def generate_occult_site(self, district_ids: list) -> OccultSite:
        stype = self._pick(list(OccultSiteType))
        names = _SITE_NAMES.get(stype, ["The Unknown Place"])
        descs = _SITE_DESCRIPTIONS.get(stype, ["A place of unsettling aspect."])
        return OccultSite(
            name=self._pick(names),
            site_type=stype,
            district_id=self._pick(district_ids) if district_ids else "",
            description=self._pick(descs),
            threat_level=self._pick(list(ThreatLevel)),
        )

    def generate_ley_line(self, site_ids: list) -> LeyLine:
        connected = self._picks(site_ids, self.rng.randint(2, min(4, len(site_ids))))
        return LeyLine(
            name=self._pick(_LEY_NAMES),
            direction=self._pick(_LEY_DIRECTIONS),
            strength=self.rng.randint(1, 5),
            sites=connected,
        )

    def generate_faction(self, site_ids: list) -> Faction:
        ftype = self._pick(list(FactionType))
        names = _FACTION_NAMES.get(ftype, ["The Unnamed Group"])
        goals = _FACTION_GOALS.get(ftype, ["Survive."])
        hq = self._pick(site_ids) if site_ids and self.rng.random() > 0.3 else None
        return Faction(
            name=self._pick(names),
            faction_type=ftype,
            description=(
                f"A {self._pick(['secretive', 'brazen', 'fractured', 'disciplined', 'desperate'])} "
                f"{ftype.value.lower()} operating in the city's {self._pick(['shadows', 'margins', 'institutions', 'streets', 'underbelly'])}."
            ),
            goals=self._pick(goals),
            methods=_FACTION_METHODS.get(ftype, "Unknown."),
            threat_level=self._pick(list(ThreatLevel)),
            hq_site_id=hq,
            member_count=self._pick(_MEMBER_COUNTS),
        )

    def _add_faction_relationships(self, factions: list[Faction]) -> None:
        for i, f in enumerate(factions):
            for j, other in enumerate(factions):
                if i >= j:
                    continue
                if self.rng.random() > 0.5:
                    rel = self._pick(list(RelationshipType))
                    f.relationships.append(FactionRelationship(faction_id=other.id, relationship=rel))
                    # mirror
                    mirror_map = {
                        RelationshipType.ALLIED: RelationshipType.ALLIED,
                        RelationshipType.NEUTRAL: RelationshipType.NEUTRAL,
                        RelationshipType.RIVAL: RelationshipType.RIVAL,
                        RelationshipType.HOSTILE: RelationshipType.HOSTILE,
                        RelationshipType.PUPPET: RelationshipType.NEUTRAL,
                        RelationshipType.UNKNOWN: RelationshipType.UNKNOWN,
                    }
                    other.relationships.append(
                        FactionRelationship(faction_id=f.id, relationship=mirror_map.get(rel, RelationshipType.NEUTRAL))
                    )

    def generate_city(
        self,
        num_districts: int = 6,
        num_sites: int = 8,
        num_ley_lines: int = 3,
        num_factions: int = 5,
    ) -> City:
        prefix = self._pick(_CITY_PREFIXES)
        suffix = self._pick(_CITY_SUFFIXES)
        name = f"{prefix}{suffix}"

        region = self.generate_region()

        # Districts
        used_names: set = set()
        districts: list[District] = []
        for _ in range(num_districts):
            d = self.generate_district(used_names)
            used_names.add(d.name)
            districts.append(d)

        district_ids = [d.id for d in districts]

        # Occult sites
        sites: list[OccultSite] = []
        used_site_names: set = set()
        for _ in range(num_sites):
            s = self.generate_occult_site(district_ids)
            if s.name in used_site_names:
                s.name = s.name + " (II)"
            used_site_names.add(s.name)
            sites.append(s)

        site_ids = [s.id for s in sites]

        # Ley lines (link sites)
        ley_lines: list[LeyLine] = []
        used_ley_names: set = set()
        for _ in range(num_ley_lines):
            ll = self.generate_ley_line(site_ids)
            if ll.name in used_ley_names:
                ll.name = ll.name + " (Branch)"
            used_ley_names.add(ll.name)
            ley_lines.append(ll)
            for sid in ll.sites:
                site = next((s for s in sites if s.id == sid), None)
                if site and ll.id not in site.ley_line_ids:
                    site.ley_line_ids.append(ll.id)

        # Factions
        factions: list[Faction] = []
        used_faction_names: set = set()
        for _ in range(num_factions):
            f = self.generate_faction(site_ids)
            if f.name in used_faction_names:
                f.name = f.name + " (Splinter)"
            used_faction_names.add(f.name)
            factions.append(f)
        self._add_faction_relationships(factions)

        population = self.rng.randint(50_000, 600_000)

        return City(
            name=name,
            region=region,
            population_approx=population,
            description=(
                f"{name} is a {self._pick(['post-industrial', 'university', 'port', 'market', 'garrison'])} city "
                f"of roughly {population:,} souls in {region.county}. "
                f"It carries the weight of {self._pick(['centuries of trade', 'industrial decline', 'religious controversy', 'forgotten wars', 'suppressed scholarship'])} "
                f"and the air of {self._pick(['barely contained secrets', 'polite denial', 'collective amnesia', 'muted dread', 'grim persistence'])}."
            ),
            history=(
                f"Founded as a {self._pick(['Roman fort', 'Saxon burh', 'monastic settlement', 'Norman market town'])}, "
                f"{name} grew through the {self._pick(['wool', 'coal', 'steel', 'cotton', 'salt'])} trade "
                f"before {self._pick(['suffering catastrophic decline', 'diversifying awkwardly', 'being absorbed into a larger conurbation', 'surviving on spite and memory'])} "
                f"in the post-war decades."
            ),
            current_events=self._pick(_CURRENT_EVENTS),
            districts=districts,
            occult_sites=sites,
            ley_lines=ley_lines,
            factions=factions,
        )


