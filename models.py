from pydantic import BaseModel


class RandomVerbCriteria(BaseModel):
    use_irregular: bool
    use_vosotros: bool
