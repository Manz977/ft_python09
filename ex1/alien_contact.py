from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Optional


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def check_operational_conditions(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type == ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )
        return self


def main():
    print("Alien Contact Log Validation")
    print("=" * 40)

    try:
        valid_station = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            contact_type=ContactType.RADIO,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True
        )
        print("Valid contact report: ")
        print(f"ID: {valid_station.contact_id}")
        print(f"Type: {valid_station.contact_type.value}")
        print(f"Location: {valid_station.location}")
        print(f"Signal: {valid_station.signal_strength}")
        print(f"Duration: {valid_station.duration_minutes} minutes")
        print(f"Witnesses: {valid_station.witness_count}")
        print(f"Message: {valid_station.message_received}")
        verified = "verified" if valid_station.is_verified else "Not verified"
        print(f"Verification status: {verified}\n")

    except ValidationError as e:
        print(f"Expected validation error:\n{e}")
    print("=" * 40)

    try:
        valid_station = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received="Greetings from Zeta Reticuli",
            is_verified=False
        )
    except ValidationError as e:
        print("Unexpected error: ")
        print(e.errors()[0]['msg'])


if __name__ == "__main__":
    main()
