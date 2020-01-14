# coding: utf-8
from sqlalchemy import Column, Date, Float, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class EastConferenceStandingsByDay(Base):
    __tablename__ = 'east_conference_standings_by_day'

    id = Column(Integer, primary_key=True, server_default=text("nextval('east_conference_standings_by_day_id_seq'::regclass)"))
    team_id = Column(Integer)
    league_id = Column(Integer)
    season_id = Column(Integer)
    standings_date = Column(Date)
    conference = Column(String)
    team = Column(String)
    games = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    w_pct = Column(Float(53))
    home_record = Column(String)
    road_record = Column(String)


class LastMeeting(Base):
    __tablename__ = 'last_meeting'

    id = Column(Integer, primary_key=True, server_default=text("nextval('last_meeting_id_seq'::regclass)"))
    game_id = Column(Integer)
    last_game_id = Column(Integer)
    last_game_date_est = Column(Date)
    last_game_home_team_id = Column(Integer)
    last_game_home_team_city = Column(String)
    last_game_home_team_name = Column(String)
    last_game_home_team_abbreviation = Column(String)
    last_game_home_team_points = Column(Integer)
    last_game_visitor_team_id = Column(Integer)
    last_game_visitor_team_city = Column(String)
    last_game_visitor_team_name = Column(String)
    last_game_visitor_team_city1 = Column(String)
    last_game_visitor_team_points = Column(Integer)


class LineScore(Base):
    __tablename__ = 'line_score'

    id = Column(Integer, primary_key=True, server_default=text("nextval('line_score_id_seq'::regclass)"))
    away_game_date_est = Column(Date)
    away_game_sequence = Column(Integer)
    away_game_id = Column(Integer)
    away_team_id = Column(Integer)
    away_team_abbreviation = Column(String(3))
    away_team_city_name = Column(String)
    away_team_wins_losses = Column(String(6))
    away_pts_qtr1 = Column(Integer)
    away_pts_qtr2 = Column(Integer)
    away_pts_qtr3 = Column(Integer)
    away_pts_qtr4 = Column(Integer)
    away_pts_ot1 = Column(Integer)
    away_pts_ot2 = Column(Integer)
    away_pts_ot3 = Column(Integer)
    away_pts_ot4 = Column(Integer)
    away_pts_ot5 = Column(Integer)
    away_pts_ot6 = Column(Integer)
    away_pts_ot7 = Column(Integer)
    away_pts_ot8 = Column(Integer)
    away_pts_ot9 = Column(Integer)
    away_pts_ot10 = Column(Integer)
    away_pts = Column(Integer)
    away_fg_pct = Column(Float(53))
    away_ft_pct = Column(Float(53))
    away_fg3_pct = Column(Float(53))
    away_assists = Column(Integer)
    away_rebounds = Column(Integer)
    away_turnovers = Column(Integer)
    home_game_date_est = Column(Date)
    home_game_sequence = Column(Integer)
    home_game_id = Column(Integer)
    home_team_id = Column(Integer)
    home_team_abbreviation = Column(String(3))
    home_team_city_name = Column(String)
    home_team_wins_losses = Column(String(6))
    home_pts_qtr1 = Column(Integer)
    home_pts_qtr2 = Column(Integer)
    home_pts_qtr3 = Column(Integer)
    home_pts_qtr4 = Column(Integer)
    home_pts_ot1 = Column(Integer)
    home_pts_ot2 = Column(Integer)
    home_pts_ot3 = Column(Integer)
    home_pts_ot4 = Column(Integer)
    home_pts_ot5 = Column(Integer)
    home_pts_ot6 = Column(Integer)
    home_pts_ot7 = Column(Integer)
    home_pts_ot8 = Column(Integer)
    home_pts_ot9 = Column(Integer)
    home_pts_ot10 = Column(Integer)
    home_pts = Column(Integer)
    home_fg_pct = Column(Float(53))
    home_ft_pct = Column(Float(53))
    home_fg3_pct = Column(Float(53))
    home_assists = Column(Integer)
    home_rebounds = Column(Integer)
    home_turnovers = Column(Integer)


class SeriesStanding(Base):
    __tablename__ = 'series_standing'

    id = Column(Integer, primary_key=True, server_default=text("nextval('series_standing_id_seq'::regclass)"))
    game_id = Column(Integer)
    home_team_id = Column(Integer)
    visitor_team_id = Column(Integer)
    game_date_est = Column(Date)
    home_team_wins = Column(Integer)
    home_team_losses = Column(Integer)
    series_leader = Column(String)


class WestConferenceStandingsByDay(Base):
    __tablename__ = 'west_conference_standings_by_day'

    id = Column(Integer, primary_key=True, server_default=text("nextval('west_conference_standings_by_day_id_seq'::regclass)"))
    team_id = Column(Integer)
    league_id = Column(Integer)
    season_id = Column(Integer)
    standings_date = Column(Date)
    conference = Column(String)
    team = Column(String)
    games = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    w_pct = Column(Float(53))
    home_record = Column(String)
    road_record = Column(String)
