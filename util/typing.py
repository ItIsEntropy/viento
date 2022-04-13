# type aliases
WeatherData = dict[str, dict] # TODO: fill dict with correct type after parsing json response
TimeStamp = float
LocationData = dict[str, WeatherData | TimeStamp] 
DataCache = dict[str, LocationData]