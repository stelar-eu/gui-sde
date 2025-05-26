from weatherData.StationRecord import StationRecord


class MapLocations:
    def __init__(self):
        self.minLat = 90000000
        self.maxLat = -90000000
        self.minLon = 180000000
        self.maxLon = -180000000
        self.stations = []
        self.map = {}

    def read_stations(self, lines):
        for line in lines[19:]:
            parts = line.split(",")
            if len(parts) < 6:
                continue
            STAID = int(parts[0].replace(" ", ""))

            STANAME = parts[1].replace(" ", "")
            CN = parts[2].replace(" ", "")
            LAT = parts[3].replace(" ", "")
            LON = parts[4].replace(" ", "")
            HGHT = int(parts[5].replace(" ", ""))
            sr = StationRecord(str(STAID), STANAME, CN, LAT, LON, HGHT)
            self.stations.append(sr)
            self.minLat = min(self.minLat, sr.get_latitude())
            self.maxLat = max(self.maxLat, sr.get_latitude())
            self.minLon = min(self.minLon, sr.get_longitude())
            self.maxLon = max(self.maxLon, sr.get_longitude())
            self.map[STAID] = [sr.get_latitude(), sr.get_longitude(), STANAME, CN]

    def get_domain(self, staid):
        if staid not in self.map:
            print(f"Station {staid} not found")
            return None, None
        return self.map[staid][0], self.map[staid][1]

    def print_stats(self):
        print(f"Latitude: {self.minLat} to {self.maxLat}")
        print(f"Longitude: {self.minLon} to {self.maxLon}")
        print(f"Number of stations: {len(self.stations)}")
        distinct_lat = len(set([sr.get_latitude() for sr in self.stations]))
        distinct_lon = len(set([sr.get_longitude() for sr in self.stations]))
        print(f"Distinct lat: {distinct_lat}")
        print(f"Distinct lon: {distinct_lon}")

