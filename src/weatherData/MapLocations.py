import streamlit as st

from src.weatherData.StationRecord import StationRecord


class MapLocations:
    def __init__(self):
        self.minLat = 90000000
        self.maxLat = -90000000
        self.minLon = 180000000
        self.maxLon = -180000000
        self.stations = []
        self.map = {}

    def read_stations(self, lines):
        for line in lines[25:]:
            parts = line.split(",")
            if len(parts) < 12:
                continue
            STAID = int(parts[0].replace(" ", ""))

            STANAME = parts[2].replace(" ", "")
            CN = parts[3].replace(" ", "")
            LAT = parts[4].replace(" ", "")
            LON = parts[5].replace(" ", "")
            HGHT = int(parts[6].replace(" ", ""))
            sr = StationRecord(str(STAID), STANAME, CN, LAT, LON, HGHT)
            self.stations.append(sr)
            self.minLat = min(self.minLat, sr.get_latitude())
            self.maxLat = max(self.maxLat, sr.get_latitude())
            self.minLon = min(self.minLon, sr.get_longitude())
            self.maxLon = max(self.maxLon, sr.get_longitude())
            self.map[STAID] = [sr.get_longitude(), sr.get_latitude(), STANAME, CN]

    def get_domain(self, staid):
        if staid not in self.map:
            print(f"Station {staid} not found")
            return None, None
        return self.map[staid][0], self.map[staid][1]

    def print_stats(self):
        st.write(f"Latitude: {self.minLat} to {self.maxLat}")
        st.write(f"Longitude: {self.minLon} to {self.maxLon}")
        st.write(f"Number of stations: {len(self.stations)}")
        distinct_lat = len(set([sr.get_latitude() for sr in self.stations]))
        distinct_lon = len(set([sr.get_longitude() for sr in self.stations]))
        st.write(f"Distinct lat: {distinct_lat}")
        st.write(f"Distinct lon: {distinct_lon}")

