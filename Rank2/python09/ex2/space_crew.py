from datetime import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    model_validator,
)


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    def validate_mission_id(self) -> None:
        """Misson IDがMで始まるか検証する"""
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with M")

    def validate_commander(self) -> None:
        """CommanderまたはCaptainが1人以上存在するか検証する"""
        if not any(
            member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
            for member in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

    def validate_experience(self) -> None:
        """365日を超えるミッションで経験5年以上の乗組員が50%以上いるか検証する"""
        if self.duration_days <= 365:
            return

        experienced = sum(member.years_experience >= 5 for member in self.crew)

        if experienced * 2 < len(self.crew):
            raise ValueError(
                "Long missions require at least 50% experienced crew"
            )

    def validate_active_crew(self) -> None:
        """すべての乗組員が活動中であるか検証する"""
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        self.validate_mission_id()
        self.validate_commander()
        self.validate_experience()
        self.validate_active_crew()
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 40)

    crew = [
        CrewMember(
            member_id="CM001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=42,
            specialization="Mission Command",
            years_experience=15,
        ),
        CrewMember(
            member_id="CM002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=35,
            specialization="Navigation",
            years_experience=8,
        ),
        CrewMember(
            member_id="CM003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=28,
            specialization="Engineering",
            years_experience=3,
        ),
    ]

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2026, 11, 8, 12, 0, 0),
        duration_days=900,
        crew=crew,
        budget_millions=2500.0,
    )

    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")

    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value})"
            f" - {member.specialization}"
        )

    print()
    print("=" * 40)

    try:
        SpaceMission(
            mission_id="M2024_TEST",
            mission_name="Test Mission",
            destination="Moon",
            launch_date=datetime(2026, 11, 8, 12, 0, 0),
            duration_days=30,
            crew=[
                CrewMember(
                    member_id="CM004",
                    name="Bob Wilson",
                    rank=Rank.OFFICER,
                    age=30,
                    specialization="Engineering",
                    years_experience=5,
                )
            ],
            budget_millions=100.0,
        )

    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
