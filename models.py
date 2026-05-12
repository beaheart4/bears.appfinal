from typing import Optional
from sqlmodel import SQLModel, Field


class Roster(SQLModel, table=True):
    __tablename__ = "roster"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    number: str
    position: str
    height: Optional[str] = None
    weight: Optional[int] = None
    age: Optional[int] = None
    experience: Optional[int] = None
    college: Optional[str] = None



class Passing(SQLModel, table=True):
    __tablename__ = "passing"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    player: str
    att: int
    comp: int
    yds: int
    comp_pct: float
    yds_per_att: float
    td: int
    td_pct: float
    int_thrown: int
    int_pct: float
    long: int
    sck: int
    sck_yds: int
    rate: float


class Rushing(SQLModel, table=True):
    __tablename__ = "rushing"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    player: str
    att: int
    yds: int
    yds_per_att: float
    long: int
    td: int


class Receiving(SQLModel, table=True):
    __tablename__ = "receiving"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    player: str
    rec: int
    yds: int
    yds_per_rec: float
    long: int
    td: int


class Tackles(SQLModel, table=True):
    __tablename__ = "tackles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    player: str
    total: int
    solo: int
    assist: int
    sck: float
    sfty: int
    forced_fmbl: int


class Interceptions(SQLModel, table=True):
    __tablename__ = "interceptions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    player: str
    int_caught: int
    yds: int
    yds_per_ret: float
    long: int
    tds: int


class FieldGoals(SQLModel, table=True):
    __tablename__ = "field_goals"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    player: str
    fg_1_19: Optional[str] = None
    fg_20_29: Optional[str] = None
    fg_30_39: Optional[str] = None
    fg_40_49: Optional[str] = None
    fg_50_59: Optional[str] = None
    fg_60_plus: Optional[str] = None


class Punting(SQLModel, table=True):
    __tablename__ = "punting"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    player: str
    punts: int
    yds: int
    long: int
    avg: float
    blk: int
    ret: int
    ret_yds: int
    in_20: int
    net_avg: float


class PuntReturns(SQLModel, table=True):
    __tablename__ = "punt_returns"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    player: str
    ret: int
    fc: int
    yds_per_ret: float
    long: int
    td: int


class KickReturns(SQLModel, table=True):
    __tablename__ = "kick_returns"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    player: str
    ret: int
    fc: int
    yds: int
    yds_per_ret: float
    long: int
    td: int
