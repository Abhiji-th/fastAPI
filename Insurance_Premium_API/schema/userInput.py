from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
from utils.city_categories import tier_1_cities, tier_2_cities

class UserInput(BaseModel):
    age: int = Field(...)
    weight: float = Field(...)
    height: float = Field(...)
    income_lpa: float = Field(...)
    smoker: bool = Field(...)
    city: str = Field(...)
    occupation: Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'] = Field(...)
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3