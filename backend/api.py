#our main file for handling API requests for the ghostwire agent

from fastapi import APIRouter
from backend.db import fetch_all_connections, fetch_all_alerts, fetch_bandwidth_summary

router = APIRouter() #this is for handling API requests for the ghostwire agent

#this one is for fetching connections from the database and returning it to the user
@router.get("/connections")
def get_connections(limit: int = 100):
    return fetch_all_connections(limit)

#this one is for fetching alerts from the database and returning it to the user
@router.get("/alerts")
def get_alerts(limit: int = 100):
    return fetch_all_alerts(limit)

#this one is for fetching bandwidth summary data from the database and returning it to the user
@router.get("/bandwidth_summary")
def get_bandwidth_summary(limit: int = 100):
    return fetch_bandwidth_summary(limit)

# alias endpoint for older clients
@router.get("/bandwidth")
def get_bandwidth(limit: int = 100):
    return fetch_bandwidth_summary(limit)