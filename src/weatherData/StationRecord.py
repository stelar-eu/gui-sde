import numpy as np

class StationRecord:
    def __init__(self, STAID, STANAME, CN, LAT, LON, HGHT):
        self.STAID = STAID
        self.STANAME = STANAME
        self.CN = CN
        self.LAT = self.convert_lat_lon_string(LAT)
        self.LON = self.convert_lat_lon_string(LON)
        self.HGHT = HGHT

    def normalize_longitude(self, lon):
        """Wrap longitude to range [-180, 180]."""
        while lon > 180:
            lon -= 360
        while lon < -180:
            lon += 360
        return lon

    def get_latitude(self):
        return self.LAT

    def get_longitude(self):
        return self.LON

    def convert_lat_lon_string(self, latlon):
        """Convert '+56:52:00' or '-014:48:00' to decimal degrees."""
        latlon = latlon.strip()
        sign = -1 if "-" in latlon else 1
        latlon = latlon.replace("+", "").replace("-", "")
        parts = latlon.split(":")
        degrees = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        decDegrees = sign * (degrees + minutes / 60 + seconds / 3600)
        decDegrees = decDegrees
        return decDegrees


    # def convert_lat_lon_string(self, latlon):
    #     parts = latlon.split(":")
    #     sign = 1
    #     degrees = int(parts[0])
    #     minutes = int(parts[1])
    #     seconds = int(parts[2])
    #     if "-" in latlon:
    #         sign = -1
    #     decDegrees = np.floor(degrees + sign * (minutes / 60) + sign * (seconds / 3600) * 10000)
    #     return decDegrees

    def getSTAID(self):
        return self.STAID

    def __str__(self):
        return f"Station {self.STAID}: {self.STANAME} in {self.CN} at {self.LAT}, {self.LON} with height {self.HGHT}"

