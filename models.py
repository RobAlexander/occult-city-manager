"""
Data models for the Occult UK City Generator.
Alternate 1980s setting.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import uuid


class DistrictType(str, Enum):
    INDUSTRIAL = "Industrial"
    RESIDENTIAL = "Residential"
    COMMERCIAL = "Commercial"
    DOCKLANDS = "Docklands"
    UNIVERSITY = "University"
    OLD_TOWN = "Old Town"
    COUNCIL_ESTATE = "Council Estate"
    SUBURB = "Suburb"
    PARKLAND = "Parkland"
    ECCLESIASTICAL = "Ecclesiastical"


class OccultSiteType(str, Enum):
    LEY_NODE = "Ley Node"
    BARROW = "Ancient Barrow"
    STANDING_STONE = "Standing Stone"
    CURSED_CHURCH = "Cursed Church"
    HAUNTED_PUB = "Haunted Pub"
    UNDERGROUND_CHAMBER = "Underground Chamber"
    RITUAL_SITE = "Ritual Site"
    MIRROR_POOL = "Mirror Pool"
    WITCHES_MARKET = "Witches' Market"
    FORGOTTEN_SHRINE = "Forgotten Shrine"
    ALCHEMY_WORKSHOP = "Alchemy Workshop"
    ASTRAL_ANCHOR = "Astral Anchor"
    GATE = "Gate"


class FactionType(str, Enum):
    COVEN = "Coven"
    HERMETIC_ORDER = "Hermetic Order"
    GOVERNMENT_AGENCY = "Government Agency"
    CHURCH_SECT = "Church Sect"
    STREET_CULT = "Street Cult"
    ACADEMIC_CIRCLE = "Academic Circle"
    CRIME_SYNDICATE = "Crime Syndicate"
    OTHERWORLDLY = "Otherworldly Entity"


class ThreatLevel(str, Enum):
    DORMANT = "Dormant"
    STIRRING = "Stirring"
    ACTIVE = "Active"
    CRITICAL = "Critical"


class RelationshipType(str, Enum):
    ALLIED = "Allied"
    NEUTRAL = "Neutral"
    RIVAL = "Rival"
    HOSTILE = "Hostile"
    PUPPET = "Puppet"
    UNKNOWN = "Unknown"


@dataclass
class LeyLine:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    direction: str = ""           # e.g. "NW to SE"
    strength: int = 1             # 1–5
    sites: list[str] = field(default_factory=list)   # site IDs connected
    notes: str = ""

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "LeyLine":
        return cls(**d)


@dataclass
class OccultSite:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    site_type: OccultSiteType = OccultSiteType.RITUAL_SITE
    district_id: str = ""
    description: str = ""
    threat_level: ThreatLevel = ThreatLevel.DORMANT
    ley_line_ids: list[str] = field(default_factory=list)
    controlling_faction_id: Optional[str] = None
    notes: str = ""

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["site_type"] = self.site_type.value
        d["threat_level"] = self.threat_level.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "OccultSite":
        d = d.copy()
        d["site_type"] = OccultSiteType(d["site_type"])
        d["threat_level"] = ThreatLevel(d["threat_level"])
        return cls(**d)


@dataclass
class District:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    district_type: DistrictType = DistrictType.RESIDENTIAL
    description: str = ""
    atmosphere: str = ""
    notable_features: list[str] = field(default_factory=list)
    occult_activity: int = 1     # 1 (none) – 5 (saturated)
    population: str = ""         # rough descriptor
    notes: str = ""

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["district_type"] = self.district_type.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "District":
        d = d.copy()
        d["district_type"] = DistrictType(d["district_type"])
        return cls(**d)


@dataclass
class FactionRelationship:
    faction_id: str = ""
    relationship: RelationshipType = RelationshipType.NEUTRAL
    notes: str = ""

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["relationship"] = self.relationship.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "FactionRelationship":
        d = d.copy()
        d["relationship"] = RelationshipType(d["relationship"])
        return cls(**d)


@dataclass
class Faction:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    faction_type: FactionType = FactionType.COVEN
    description: str = ""
    goals: str = ""
    methods: str = ""
    threat_level: ThreatLevel = ThreatLevel.DORMANT
    hq_site_id: Optional[str] = None
    member_count: str = ""       # rough descriptor
    relationships: list[FactionRelationship] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["faction_type"] = self.faction_type.value
        d["threat_level"] = self.threat_level.value
        d["relationships"] = [r.to_dict() for r in self.relationships]
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Faction":
        d = d.copy()
        d["faction_type"] = FactionType(d["faction_type"])
        d["threat_level"] = ThreatLevel(d["threat_level"])
        d["relationships"] = [FactionRelationship.from_dict(r) for r in d.get("relationships", [])]
        return cls(**d)


@dataclass
class Region:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    county: str = ""
    description: str = ""
    geography: str = ""
    history: str = ""
    occult_reputation: str = ""
    notes: str = ""

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "Region":
        return cls(**d)


@dataclass
class City:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    region: Region = field(default_factory=Region)
    population_approx: int = 0
    description: str = ""
    history: str = ""
    current_events: str = ""      # alt-1980s flavour
    districts: list[District] = field(default_factory=list)
    occult_sites: list[OccultSite] = field(default_factory=list)
    ley_lines: list[LeyLine] = field(default_factory=list)
    factions: list[Faction] = field(default_factory=list)
    notes: str = ""

    # --- helpers ---
    def get_district(self, district_id: str) -> Optional[District]:
        return next((d for d in self.districts if d.id == district_id), None)

    def get_site(self, site_id: str) -> Optional[OccultSite]:
        return next((s for s in self.occult_sites if s.id == site_id), None)

    def get_faction(self, faction_id: str) -> Optional[Faction]:
        return next((f for f in self.factions if f.id == faction_id), None)

    def get_ley_line(self, ley_id: str) -> Optional[LeyLine]:
        return next((l for l in self.ley_lines if l.id == ley_id), None)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "region": self.region.to_dict(),
            "population_approx": self.population_approx,
            "description": self.description,
            "history": self.history,
            "current_events": self.current_events,
            "districts": [d.to_dict() for d in self.districts],
            "occult_sites": [s.to_dict() for s in self.occult_sites],
            "ley_lines": [l.to_dict() for l in self.ley_lines],
            "factions": [f.to_dict() for f in self.factions],
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "City":
        return cls(
            id=d["id"],
            name=d["name"],
            region=Region.from_dict(d["region"]),
            population_approx=d["population_approx"],
            description=d["description"],
            history=d["history"],
            current_events=d["current_events"],
            districts=[District.from_dict(x) for x in d.get("districts", [])],
            occult_sites=[OccultSite.from_dict(x) for x in d.get("occult_sites", [])],
            ley_lines=[LeyLine.from_dict(x) for x in d.get("ley_lines", [])],
            factions=[Faction.from_dict(x) for x in d.get("factions", [])],
            notes=d.get("notes", ""),
        )
