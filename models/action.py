""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Action:
    action_type: str        # e.g. "ADMIT_BED", "DISCHARGE", "VITAL_SIGN"
    description: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
    restore_data: dict = field(default_factory=dict)
