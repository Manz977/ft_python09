from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from datetime import datetime
from typing import Optional

class SpaceStation(BaseModel):
  station_id:str =  Field(min_length=3, max_length=10)
  name:str = Field(min_length=1, max_length=50)
  crew_size:int = Field(ge=1, le=20)
  power_level:float = Field(ge=0.0, le=100.0)
  oxygen_level:float = Field(ge=0.0, le=100.0)
  last_maintenance: datetime
  is_operational:bool = Field(default=True)
  notes:Optional[str] = Field(default=None, max_length=200)
  
  
  @model_validator(mode="after")
  def check_operational_conditions(self) -> "SpaceStation":
    if not self.is_operational and self.power_level > 0:
      raise ValueError(
        "Non-operational station can not have power level above 0"
      )
    if self.oxygen_level < 20 and self.is_operational:
      raise ValueError(
        "Station with oxygen level below 20% can not be operational"
      )
      
    return self
  

def main():
  print("Space Station Data Validation")
  print("=" * 40)
  
  try:
    valid_station = SpaceStation(
      station_id= "ISS0001",
      name="International Space Station",
      crew_size=6,
      power_level=85.5,
      oxygen_level=92.3,
      last_maintenance=datetime.now(),
      is_operational=True,
      notes="The international space station is operational"
    )
    print("Valid station created:")
    print(f"ID: {valid_station.station_id}")
    print(f"Name: {valid_station.name}")
    print(f"Crew {valid_station.crew_size} people")
    print(f"Power: {valid_station.power_level}%")
    print(f"Oxygen: {valid_station.oxygen_level}%")
    print(f"Status:" " Operational" if valid_station.is_operational else " Non-Operational")
    print(f"maintenance {valid_station.last_maintenance}")
    print(f"Notes: {valid_station.notes}")
    
    print("=" * 40)
  except ValidationError as e:
    print(f"Unexpected error: {e}")
  
  try:
    valid_station = SpaceStation(
      station_id= "ISS0001",
      name="Unfunctional Space Station",
      crew_size=21,
      power_level=50.5,
      oxygen_level=40.3,
      last_maintenance=datetime.fromisoformat("2020-10-06 09:30:00"),
      is_operational=True,
      notes="This unfunctional space station"
    )
    
  except ValidationError as e:
    print(f"Unexpected error: ")
    for error in e.errors():
      print(error['msg'])
    
  
if __name__ == "__main__":
  main()