from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Optional, List


class CrewRanks(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: CrewRanks
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    desination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: Optional[str] = Field(default="planned")
    budgeet_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_operational_conditions(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission id must start with 'M'")

        has_leadership = False
        experienced_count = 0

        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active")

            if (member.rank == CrewRanks.COMMANDER
                    or member.rank == CrewRanks.CAPTAIN):
                has_leadership = True
            if member.years_experience >= 5:
                experienced_count += 1

        if not has_leadership:
            raise ValueError("Must have at least one Commander or Captain")
        if self.duration_days > 365 and experienced_count < len(self.crew) / 2:
            raise ValueError(
                "For missions longer than 365 days 50% of the crew "
                "should be (5+years) experienced"
            )

        return self


def main():
    print("Space Mission Crew Validation")
    print("=" * 40)

    try:
        valid_crew = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            desination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=[
                CrewMember(
                    member_id="CM_001",
                    name="Sarah Connor",
                    rank=CrewRanks.COMMANDER,
                    age=45,
                    specialization="Mission Command",
                    years_experience=12,
                    is_active=True
                ),
                CrewMember(
                    member_id="CM_002",
                    name="John Smith",
                    rank=CrewRanks.LIEUTENANT,
                    age=50,
                    specialization="Navigation",
                    years_experience=20,
                    is_active=True
                ),
                CrewMember(
                    member_id="CM_003",
                    name="Alice Johnson",
                    rank=CrewRanks.OFFICER,
                    age=35,
                    specialization="Mission Enginnering",
                    years_experience=10,
                    is_active=True
                )
            ],
            mission_status="planned",
            budgeet_millions=2500
        )
        print("Valid mission created:")
        print(f"Mission: {valid_crew.mission_name}")
        print(f"ID: {valid_crew.mission_id}")
        print(f"Destination: {valid_crew.desination}")
        print(f"Duration: {valid_crew.duration_days} days")
        print(f"Budget: {valid_crew.budgeet_millions}")
        print(f"Crew size: {len(valid_crew.crew)}")
        print("Crew members: ")
        for crew in valid_crew.crew:
            print(f"- {crew.name} ({crew.rank.value}) - {crew.specialization}")

    except ValidationError as e:
        print(f"Expected validation error:\n {e}")
    print()
    print("=" * 40)

    try:
        valid_crew = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            desination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=[
                CrewMember(
                    member_id="CM_001",
                    name="Sarah Connor",
                    rank=CrewRanks.CADET,
                    age=45,
                    specialization="Mission Command",
                    years_experience=12,
                    is_active=True
                ),
                CrewMember(
                    member_id="CM_002",
                    name="John Smith",
                    rank=CrewRanks.LIEUTENANT,
                    age=50,
                    specialization="Navigation",
                    years_experience=20,
                    is_active=True
                ),
                CrewMember(
                    member_id="CM_003",
                    name="Alice Johnson",
                    rank=CrewRanks.OFFICER,
                    age=35,
                    specialization="Mission Enginnering",
                    years_experience=10,
                    is_active=True
                )
            ],
            mission_status="planned",
            budgeet_millions=2500
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])


if __name__ == "__main__":
    main()
