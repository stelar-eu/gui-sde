import numpy as np

class StationRecord:
    def __init__(self, STAID, STANAME, CN, LAT, LON, HGHT):
        self.STAID = STAID
        self.STANAME = STANAME
        self.CN = CN
        self.LAT = self.convert_lat_lon_string(LAT)
        self.LON = self.convert_lat_lon_string(LON)
        self.HGHT = HGHT

    def get_latitude(self):
        return self.LAT

    def get_longitude(self):
        return self.LON

    def convert_lat_lon_string(self, latlon):
        parts = latlon.split(":")
        sign = 1
        degrees = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        if "-" in latlon:
            sign = -1
        decDegrees = np.floor(degrees + sign * (minutes / 60) + sign * (seconds / 3600) * 10000)
        return decDegrees

    def getSTAID(self):
        return self.STAID

    def __str__(self):
        return f"Station {self.STAID}: {self.STANAME} in {self.CN} at {self.LAT}, {self.LON} with height {self.HGHT}"