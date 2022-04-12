# type aliases
WeatherData = dict[str, dict] # TODO: fill dict with correct type after parsing json response
LocationData = dict[str, WeatherData | float] 
URLData = dict[str, LocationData]
DataCache = dict[str, URLData]