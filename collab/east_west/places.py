"""Launch points and destinations for the east-to-west study (docs/East_West_Study.md)."""
# drop point: about 40-45 km offshore on the downwind (south-west) side, clear of island wind shadows
LAUNCH = {
    "gran_canaria": dict(name="Gran Canaria (Las Palmas), 45 km SW of Maspalomas", port=(28.14, -15.41), drop=(27.45, -15.95)),
    "el_hierro":    dict(name="El Hierro (La Restinga), 40 km SW", port=(27.64, -17.98), drop=(27.35, -18.30)),
    "mindelo":      dict(name="Cape Verde (Mindelo, Sao Vicente), 45 km SW, south of Santo Antao", port=(16.89, -24.99), drop=(16.55, -25.35)),
    "madeira":      dict(name="Madeira (Funchal), 45 km SW", port=(32.65, -16.91), drop=(32.35, -17.25)),
    "cadiz":        dict(name="Cadiz, Spain, 45 km W in the Gulf of Cadiz", port=(36.53, -6.30), drop=(36.40, -6.85)),
    "lisbon":       dict(name="Lisbon (Cascais), Portugal, 45 km W", port=(38.69, -9.42), drop=(38.55, -9.95)),
    "cornwall":     dict(name="Cornwall (Falmouth), 45 km SW of the Isles of Scilly", port=(50.15, -5.07), drop=(49.65, -6.85)),
}
# target: a few km off the windward (east) coast; any landfall in the Americas also counts
DEST = {
    "barbados":    dict(name="Barbados (east coast)", target=(13.17, -59.40), port="Bridgetown / Port St Charles"),
    "st_lucia":    dict(name="St Lucia (windward coast)", target=(13.95, -60.85), port="Rodney Bay"),
    "martinique":  dict(name="Martinique, France (windward coast)", target=(14.65, -60.80), port="Le Marin / Fort-de-France"),
    "guadeloupe":  dict(name="Guadeloupe, France (windward coast)", target=(16.25, -61.15), port="Pointe-a-Pitre"),
    "antigua":     dict(name="Antigua (windward coast)", target=(17.05, -61.65), port="English Harbour / Jolly Harbour"),
    "puerto_rico": dict(name="Puerto Rico, US (off Fajardo)", target=(18.45, -65.55), port="Fajardo / San Juan"),
    "new_england": dict(name="Nantucket Shoals, US", target=(41.0, -69.5), port="Newport, RI"),
}
