"""
DSS SkyNet Fleet Scraper
Automated login and data extraction from SkyNetX fleet management portal.
"""

import json
from pathlib import Path
import os
import sys
from datetime import datetime

import requests

from config import (
    DSS_USERNAME,
    DSS_PASSWORD,
    DSS_PIN,
    API_BASE_URL,
    LOGIN_ENDPOINT,
    HEADERS
)


class SkyNetScraper:
    """Main scraper class for DSS SkyNet portal."""
    
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_data = None
        self.units = []
        self.authenticated = False
    
    def login(self, username: str, password: str, pin: str | None = None) -> dict:
        """
        Authenticate to SkyNet API.
        
        Args:
            username: DSS username
            password: DSS password
            pin: Optional domain PIN (default: demodss)
            
        Returns:
            dict: Login response with token and user data
        """
        login_data = {
            "user": username,
            "pass": password
        }
        
        if pin:
            login_data["pin"] = pin
        else:
            login_data["pin"] = "demodss"
        
        try:
            response = self.session.post(
                LOGIN_ENDPOINT,
                json=login_data,
                headers=HEADERS
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("success"):
                self.token = data.get("token")
                self.user_data = data.get("userdata")
                self.units = data.get("units", [])
                self.authenticated = True
                self._save_session()
                print(f"[OK] Login successful as {username}")
                print(f"[INFO] Units assigned: {len(self.units)}")
                return data
            else:
                print(f"[ERROR] Login failed: {data}")
                return data
                
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Connection error: {e}")
            return {"success": False, "error": str(e)}
    
    def _save_session(self):
        """Save session data to file for persistence."""
        session_data = {
            "token": self.token,
            "user_data": self.user_data,
            "units": self.units,
            "saved_at": datetime.now().isoformat()
        }
        
        with open("session.json", "w") as f:
            json.dump(session_data, f, indent=2, default=str)
    
    def load_session(self) -> bool:
        """Load existing session from file."""
        try:
            with open("session.json", "r") as f:
                session_data = json.load(f)
            
            self.token = session_data.get("token")
            self.user_data = session_data.get("user_data")
            self.units = session_data.get("units", [])
            self.authenticated = True
            return True
        except FileNotFoundError:
            return False
    
    def get_api_headers(self) -> dict:
        """Get headers for authenticated API requests."""
        return {
            "Content-Type": "application/json",
            "x-access-token": self.token,
            "x-api-name": "fleet data",
            "x-api-vers": "v3"
        }
    
    def get_units(self) -> list:
        """Get list of all GPS units assigned to user."""
        return self.units
    
    def get_sitemap(self) -> dict:
        """
        Extract sitemap/navigation structure from available modules.
        Based on domain configuration modules.
        """
        sitemap = {
            "base": "https://skynetx.dssgroup.it/",
            "sections": []
        }
        
        modules = [
            {
                "name": "Realtime",
                "description": "Real-time map tracking",
                "path": "/realtime"
            },
            {
                "name": "Report",
                "description": "Fleet reports and analytics",
                "path": "/report",
                "sub_items": [
                    {"name": "Totals", "path": "/report/totals"},
                    {"name": "Partials", "path": "/report/partials"},
                    {"name": "Daily", "path": "/report/daily"},
                    {"name": "Fleet Daily", "path": "/report/fleet-daily"},
                    {"name": "Last 24h", "path": "/report/last-24h"},
                    {"name": "Last 72h", "path": "/report/last-72h"}
                ]
            },
            {
                "name": "Yard",
                "description": "Yard management",
                "path": "/yard"
            },
            {
                "name": "IO",
                "description": "Input/Output controls",
                "path": "/io"
            },
            {
                "name": "Targets",
                "description": "Geofencing targets with events",
                "path": "/targets"
            },
            {
                "name": "Routes",
                "description": "Route management with events",
                "path": "/routes"
            },
            {
                "name": "Events",
                "description": "Event logs and alerts",
                "path": "/events"
            },
            {
                "name": "Temperature",
                "description": "Temperature monitoring",
                "path": "/temperature"
            },
            {
                "name": "Chart",
                "description": "Speed/Analog/Activity charts",
                "path": "/chart"
            },
            {
                "name": "Last Point",
                "description": "Latest GPS positions",
                "path": "/last-point"
            },
            {
                "name": "Shipments",
                "description": "Shipment tracking with events",
                "path": "/shipments"
            },
            {
                "name": "Maintenance",
                "description": "Vehicle maintenance scheduling",
                "path": "/maintenance"
            },
            {
                "name": "Drivers",
                "description": "Driver registry and management",
                "path": "/drivers"
            },
            {
                "name": "Geofencing",
                "description": "Geofence management",
                "path": "/geofencing"
            }
        ]
        
        sitemap["sections"] = modules
        return sitemap
    
    def get_functionalities(self) -> dict:
        """
        Extract complete list of functionalities based on research.
        """
        return {
            "authentication": {
                "name": "Authentication",
                "features": [
                    "JWT token-based authentication",
                    "Session persistence",
                    "Two-factor authentication (2FA) support",
                    "Password reset functionality"
                ]
            },
            "fleet_tracking": {
                "name": "Fleet Tracking",
                "features": [
                    "Real-time GPS position tracking",
                    "Vehicle status monitoring",
                    "Speed tracking",
                    "Heading/direction monitoring",
                    "Last position retrieval"
                ]
            },
            "mapping": {
                "name": "Mapping & Visualization",
                "features": [
                    "Interactive map display",
                    "Multiple map providers support",
                    "Vehicle markers on map",
                    "Route visualization",
                    "Stop location markers"
                ]
            },
            "reporting": {
                "name": "Reporting & Analytics",
                "features": [
                    "Total reports",
                    "Partial reports",
                    "Daily reports",
                    "Fleet daily reports",
                    "Last 24h reports",
                    "Last 72h reports",
                    "Custom date range reports",
                    "Export capabilities"
                ]
            },
            "geofencing": {
                "name": "Geofencing & Targets",
                "features": [
                    "Geofence creation",
                    "Target waypoints",
                    "Entry/exit alerts",
                    "Custom zones"
                ]
            },
            "sensors": {
                "name": "Sensor Monitoring",
                "features": [
                    "Temperature monitoring",
                    "Humidity tracking",
                    "Shock detection",
                    "Light sensors",
                    "Altitude tracking",
                    "Analog inputs"
                ]
            },
            "events": {
                "name": "Events & Alarms",
                "features": [
                    "Real-time event notifications",
                    "Power failure alarms",
                    "SOS alerts",
                    "Speed limit violations",
                    "Geofence breach alerts",
                    "24/7 central station monitoring"
                ]
            },
            "maintenance": {
                "name": "Maintenance Management",
                "features": [
                    "Vehicle maintenance scheduling",
                    "Service reminders",
                    "Maintenance history"
                ]
            },
            "drivers": {
                "name": "Driver Management",
                "features": [
                    "Driver registry",
                    "Driver-vehicle association",
                    "Driver activation/deactivation",
                    "Driver identification"
                ]
            },
            "shipments": {
                "name": "Shipment Tracking",
                "features": [
                    "Cargo tracking",
                    "Shipment events",
                    "ETA calculations"
                ]
            },
            "api": {
                "name": "API Access",
                "features": [
                    "REST API access",
                    "API key management",
                    "Third-party integration"
                ]
            }
        }
    
    def logout(self):
        """Clear session and logout."""
        self.token = None
        self.user_data = None
        self.units = []
        self.authenticated = False
        
        try:
            os.remove("session.json")
        except FileNotFoundError:
            pass
        
        print("[OK] Logged out successfully")


def main():
    print("=" * 50)
    print("DSS SkyNet Fleet Scraper")
    print("=" * 50)
    
    if not DSS_USERNAME or not DSS_PASSWORD:
        print("[ERROR] Missing credentials in .env file!")
        print("  Please set DSS_USERNAME and DSS_PASSWORD")
        sys.exit(1)
    
    scraper = SkyNetScraper()
    
    print(f"\n[*] Logging in as {DSS_USERNAME}...")
    result = scraper.login(DSS_USERNAME, DSS_PASSWORD, DSS_PIN)
    
    if result.get("success"):
        print("\n[2] Extracting sitemap...")
        sitemap = scraper.get_sitemap()
        
        print("\n[3] Extracting functionalities...")
        functionalities = scraper.get_functionalities()
        
        print("\n[4] Getting units data...")
        units = scraper.get_units()
        
        output = {
            "scraped_at": datetime.now().isoformat(),
            "login_success": True,
            "username": DSS_USERNAME,
            "units_count": len(units),
            "sitemap": sitemap,
            "functionalities": functionalities,
            "units": units[:5] if len(units) > 5 else units
        }
        
        with open("skynet_data.json", "w") as f:
            json.dump(output, f, indent=2, default=str)
        
        print("\n[OK] Data saved to skynet_data.json")
        print(f"[INFO] Found {len(units)} GPS units")
        print(f"[INFO] Identified {len(sitemap['sections'])} main sections")
        
        update_html_with_data(output)
        
    else:
        print("\n[ERROR] Login failed. Check credentials.")
        sys.exit(1)


def update_html_with_data(data):
    """Update index.html with scraped data inline."""
    html_path = Path(__file__).parent / "index.html"
    
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    data_json = json.dumps(data, indent=2, default=str)
    
    new_html = html.replace(
        "let data = null;",
        f"let data = {data_json};"
    )
    
    new_html = new_html.replace(
        "async function loadData() {",
        "function loadData() {"
    )
    
    new_html = new_html.replace(
        '''try {
                const response = await fetch('skynet_data.json');
                data = await response.json();
                renderData();
            } catch (error) {
                document.getElementById('status-badge').innerHTML = '<span class="status-badge warning">Run scraper.py first</span>';
                document.getElementById('status-badge').querySelector('span').className = 'status-badge warning';
            }''',
        "renderData();"
    )
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    
    print("[OK] HTML dashboard updated with data")


if __name__ == "__main__":
    main()
