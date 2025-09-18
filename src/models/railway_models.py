from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TrainType(Enum):
    SUPERFAST = "Superfast"
    EXPRESS = "Express"
    PASSENGER = "Passenger"
    FREIGHT = "Freight"

class TrainStatus(Enum):
    ON_TIME = "On Time"
    DELAYED = "Delayed"
    HALTED = "Halted"

class TrackType(Enum):
    SINGLE_LINE = "Single Line"
    DOUBLE_LINE = "Double Line"

class CongestionLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class BlockStatus(Enum):
    FREE = "Free"
    OCCUPIED = "Occupied"
    UNDER_MAINTENANCE = "Under Maintenance"

class PowerStatus(Enum):
    NORMAL = "Normal"
    POWER_BLOCK = "Power Block"
    TRIPPED = "Tripped"

class SignalStatus(Enum):
    NORMAL = "Normal"
    FAILURE = "Failure"
    MANUAL_WORKING = "Manual Working"

class WeatherCondition(Enum):
    CLEAR = "Clear"
    FOG = "Fog"
    RAIN = "Rain"
    STORM = "Storm"

class ExternalFactorType(Enum):
    FESTIVAL = "Festival"
    STRIKE = "Strike"
    EXAM_RUSH = "Exam Rush"
    NATURAL_DISASTER = "Natural Disaster"

class Severity(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class IncidentType(Enum):
    ACCIDENT = "Accident"
    DERAILMENT = "Derailment"
    LEVEL_CROSSING = "Level Crossing"
    FIRE = "Fire"
    SECURITY = "Security"
    TECHNICAL_FAILURE = "Technical Failure"

class Outcome(Enum):
    RESOLVED = "Resolved"
    PARTIALLY_RESOLVED = "Partially Resolved"
    ESCALATED = "Escalated"

@dataclass
class Train:
    train_id: int
    train_no: str
    train_type: TrainType
    priority: int
    current_status: TrainStatus
    delay_minutes: int = 0
    crew_status: Optional[str] = None
    loco_health: Optional[str] = None
    linked_train_id: Optional[int] = None

@dataclass
class Section:
    section_id: int
    name: str
    track_type: TrackType
    congestion_level: CongestionLevel
    block_status: BlockStatus
    power_status: PowerStatus
    signal_status: SignalStatus
    weather_condition: WeatherCondition

@dataclass
class Station:
    station_id: int
    section_id: int
    num_platforms: int
    yard_capacity: int
    current_occupancy: int = 0
    special_facility: Optional[str] = None

@dataclass
class ExternalFactor:
    factor_id: int
    section_id: int
    type: ExternalFactorType
    severity: Severity
    remarks: Optional[str] = None

@dataclass
class Incident:
    incident_id: int
    section_id: int
    type: IncidentType
    timestamp: datetime
    train_id: Optional[int] = None
    resolution: Optional[str] = None

@dataclass
class Decision:
    decision_id: int
    section_id: int
    controller_action: str
    timestamp: datetime
    outcome: Outcome
    issue_id: Optional[int] = None
