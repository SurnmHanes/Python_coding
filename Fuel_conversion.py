def liters_100km_to_miles_gallon(liters):
    liters_per_km = liters / 100
    gallons_per_km = liters_per_km / 3.785411784
    km_per_gallon = 1 / gallons_per_km
    miles_per_gallon = km_per_gallon / 1.609344
    return miles_per_gallon
    

def miles_gallon_to_liters_100km(miles):
    km_per_gallon = miles * 1.609344
    gallons_per_km = 1 / km_per_gallon
    liters_per_km = 3.785411784 * gallons_per_km
    liters_per_100km = liters_per_km * 100
    return liters_per_100km 