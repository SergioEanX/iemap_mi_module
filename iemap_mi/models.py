from pydantic import BaseModel, constr
from typing import List, Any


class AuthData(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)


class ProjectResponse(BaseModel):
    skip: int
    page_size: int
    page_number: int
    page_tot: int
    number_docs: int
    data: list


class AffiliationCount(BaseModel):
    affiliation: str
    n: int


class StatsData(BaseModel):
    totalProj: int
    totalUsers: int
    countProj: List[AffiliationCount]
    countFiles: List[AffiliationCount]
    totalUsersRegistered: int


class StatsResponse(BaseModel):
    data: StatsData


class AuthData(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)


class ProjectResponse(BaseModel):
    skip: int
    page_size: int
    page_number: int
    page_tot: int
    number_docs: int
    data: List[Any]
