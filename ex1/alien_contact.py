from enum import Enum
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from datetime import datetime
from typing import Optional


class ContactType(Enum):
  RADIO = "radio"
  VISUAL = "visual"
  PHYSICAL = "physical"
  TELEPATHIC = "telepathic"

  