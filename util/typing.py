# type aliases
APIResponse = dict[str, str | int | list | dict]
WeatherData = dict[str, APIResponse] # TODO: fill dict with correct type after parsing json response
TimeStamp = float
LocationData = dict[str, WeatherData | TimeStamp] 
DataCache = dict[str, LocationData]
VientoResponse = list[dict[str, float]]