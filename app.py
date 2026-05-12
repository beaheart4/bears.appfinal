from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, func, SQLModel
from typing import Optional, Dict, Any, List
import os

from models import (
    Roster, Passing, Rushing, Receiving, Tackles, 
    Interceptions, FieldGoals
)
from database import get_session, engine

# Create tables
SQLModel.metadata.create_all(engine)

app = FastAPI(title="Chicago Bears Stats API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/roster")
def get_roster(session: Session = Depends(get_session)):
    """Get all roster records sorted by position and name"""
    rows = session.exec(
        select(Roster).order_by(Roster.position, Roster.name)
    ).all()
    return rows

@app.get("/api/passing")
def get_passing(session: Session = Depends(get_session)):
    """Get passing stats (distinct players) sorted by yards DESC"""
    rows = session.exec(
        select(
            Passing.player,
            Passing.att,
            Passing.comp,
            Passing.yds,
            Passing.comp_pct,
            Passing.yds_per_att,
            Passing.td,
            Passing.int_thrown,
            Passing.sck,
            Passing.rate
        ).distinct().order_by(Passing.yds.desc())
    ).all()
    # Convert tuples to dicts
    result = []
    for row in rows:
        result.append({
            "player": row[0],
            "att": row[1],
            "comp": row[2],
            "yds": row[3],
            "comp_pct": row[4],
            "yds_per_att": row[5],
            "td": row[6],
            "int_thrown": row[7],
            "sck": row[8],
            "rate": row[9]
        })
    return result

@app.get("/api/rushing")
def get_rushing(session: Session = Depends(get_session)):
    """Get rushing stats (distinct players) sorted by yards DESC"""
    rows = session.exec(
        select(
            Rushing.player,
            Rushing.att,
            Rushing.yds,
            Rushing.yds_per_att,
            Rushing.long,
            Rushing.td
        ).distinct().order_by(Rushing.yds.desc())
    ).all()
    
    result = []
    for row in rows:
        result.append({
            "player": row[0],
            "att": row[1],
            "yds": row[2],
            "yds_per_att": row[3],
            "long": row[4],
            "td": row[5]
        })
    return result

@app.get("/api/receiving")
def get_receiving(session: Session = Depends(get_session)):
    """Get receiving stats (distinct players) sorted by yards DESC"""
    rows = session.exec(
        select(
            Receiving.player,
            Receiving.rec,
            Receiving.yds,
            Receiving.yds_per_rec,
            Receiving.long,
            Receiving.td
        ).distinct().order_by(Receiving.yds.desc())
    ).all()
    
    result = []
    for row in rows:
        result.append({
            "player": row[0],
            "rec": row[1],
            "yds": row[2],
            "yds_per_rec": row[3],
            "long": row[4],
            "td": row[5]
        })
    return result

@app.get("/api/tackles")
def get_tackles(session: Session = Depends(get_session)):
    """Get tackles stats (distinct players) sorted by total DESC"""
    rows = session.exec(
        select(
            Tackles.player,
            Tackles.total,
            Tackles.solo,
            Tackles.assist,
            Tackles.sck,
            Tackles.forced_fmbl
        ).distinct().order_by(Tackles.total.desc())
    ).all()
    
    result = []
    for row in rows:
        result.append({
            "player": row[0],
            "total": row[1],
            "solo": row[2],
            "assist": row[3],
            "sck": row[4],
            "forced_fmbl": row[5]
        })
    return result

@app.get("/api/interceptions")
def get_interceptions(session: Session = Depends(get_session)):
    """Get interceptions stats (distinct players) sorted by int_caught DESC"""
    rows = session.exec(
        select(
            Interceptions.player,
            Interceptions.int_caught,
            Interceptions.yds,
            Interceptions.yds_per_ret,
            Interceptions.long,
            Interceptions.tds
        ).distinct().order_by(Interceptions.int_caught.desc())
    ).all()
    
    result = []
    for row in rows:
        result.append({
            "player": row[0],
            "int_caught": row[1],
            "yds": row[2],
            "yds_per_ret": row[3],
            "long": row[4],
            "tds": row[5]
        })
    return result

@app.get("/api/field_goals")
def get_field_goals(session: Session = Depends(get_session)):
    """Get field goals stats (distinct players)"""
    rows = session.exec(
        select(
            FieldGoals.player,
            FieldGoals.fg_1_19,
            FieldGoals.fg_20_29,
            FieldGoals.fg_30_39,
            FieldGoals.fg_40_49,
            FieldGoals.fg_50_59,
            FieldGoals.fg_60_plus
        ).distinct()
    ).all()
    
    result = []
    for row in rows:
        result.append({
            "player": row[0],
            "fg_1_19": row[1],
            "fg_20_29": row[2],
            "fg_30_39": row[3],
            "fg_40_49": row[4],
            "fg_50_59": row[5],
            "fg_60_plus": row[6]
        })
    return result

@app.get("/api/stats/summary")
def get_summary(session: Session = Depends(get_session)):
    """Get aggregated stats summary"""
    roster_count = session.exec(
        select(func.count(Roster.id))
    ).one()
    
    top_passer = session.exec(
        select(Passing.player, Passing.yds, Passing.td)
        .order_by(Passing.yds.desc())
        .limit(1)
    ).first()
    
    top_rusher = session.exec(
        select(Rushing.player, Rushing.yds, Rushing.td)
        .order_by(Rushing.yds.desc())
        .limit(1)
    ).first()
    
    top_receiver = session.exec(
        select(Receiving.player, Receiving.yds, Receiving.td)
        .order_by(Receiving.yds.desc())
        .limit(1)
    ).first()
    
    top_tackler = session.exec(
        select(Tackles.player, Tackles.total)
        .order_by(Tackles.total.desc())
        .limit(1)
    ).first()
    
    return {
        "roster_count": roster_count,
        "top_passer": {
            "player": top_passer[0],
            "yds": top_passer[1],
            "td": top_passer[2]
        } if top_passer else None,
        "top_rusher": {
            "player": top_rusher[0],
            "yds": top_rusher[1],
            "td": top_rusher[2]
        } if top_rusher else None,
        "top_receiver": {
            "player": top_receiver[0],
            "yds": top_receiver[1],
            "td": top_receiver[2]
        } if top_receiver else None,
        "top_tackler": {
            "player": top_tackler[0],
            "total": top_tackler[1]
        } if top_tackler else None,
    }

@app.get("/api/positions")
def get_positions(session: Session = Depends(get_session)):
    """Get position counts sorted by count DESC"""
    rows = session.exec(
        select(Roster.position, func.count(Roster.id).label("count"))
        .group_by(Roster.position)
        .order_by(func.count(Roster.id).desc())
    ).all()
    
    result = []
    for row in rows:
        result.append({
            "position": row[0],
            "count": row[1]
        })
    return result

@app.get("/", include_in_schema=False)
def serve_index():
    """Serve the index.html file at root"""
    from fastapi.responses import FileResponse
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    return FileResponse(os.path.join(static_dir, "index.html"), media_type="text/html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
