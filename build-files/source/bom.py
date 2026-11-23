"""Bill of materials for the Rev E1/E2 boat, written for a hobbyist builder.

Writes ../BOM.csv (everything to buy) and ../Print_Guide.csv (every printed part).
Prices: "web" = seen on the linked page in November 2026; "est" = estimate, check before ordering.
Links were checked by search in November 2026; shops change, so search the part number if one breaks.
Run: python3 bom.py
"""
import csv, json, os
import parts as Pm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..")

# (section, item, specification, qty, unit, unit_usd, basis, supplier, link, used_in, notes)
B = []
def add(sec, item, spec, qty, unit, usd, basis, supplier="", link="", used="", notes=""):
    B.append(dict(section=sec, item=item, spec=spec, qty=qty, unit=unit, unit_usd=usd, basis=basis,
                  supplier=supplier, link=link, used_in=used, notes=notes))

# ------------------------------------------------------------------ A. Autopilot, comms, sensors
S = "A Electronics: autopilot, comms, sensors"
add(S, "Autopilot", "Holybro Pixhawk 6C Mini, Model A (SKU 20235)", 1, "ea", 176.99, "web", "Holybro",
    "https://holybro.com/products/pixhawk-6c-mini", "Main box (D03, D30)", "ArduPilot Rover, sailboat frame")
add(S, "Autopilot power module", "Holybro PM02 V3 (12S), 5.2 V 3 A out, voltage + current sense", 1, "ea", 25, "est", "GetFPV",
    "https://www.getfpv.com/holybro-pixhawk-pm02-v3-12s-power-module.html", "Main box (D30)", "Replace the XT60s with soldered, heat-shrunk joints")
add(S, "GPS + compass", "Holybro Micro M10 GPS with case, IST8310 compass (SKU 12044)", 2, "ea", 27.99, "web", "Holybro",
    "https://holybro.com/products/micro-m10-gps/", "P05 (main), P21 (limp-home)", "Pot in soft silicone after the shakedown")
add(S, "Companion + limp-home MCU", "Adafruit Feather ESP32-S3, 4 MB flash / 2 MB PSRAM (#5477)", 2, "ea", 17.50, "est", "Adafruit",
    "https://www.adafruit.com/product/5477", "Main box, P21", "Buy a third as a programmed spare (row S)")
add(S, "Satellite modem", "Ground Control RockBLOCK Plus, 3 m cable (FP-GC-RB-PLUS-3M)", 1, "ea", 419.00, "web", "Ground Control",
    "https://store.groundcontrol.com/products/rockblock-plus", "P23 in the hatch lid", "Airtime is extra (line rental + credits)")
add(S, "RS-232 level shifter", "SparkFun MAX3232 transceiver breakout (BOB-11189)", 1, "ea", 7.26, "web", "SparkFun",
    "https://www.sparkfun.com/products/11189", "Main box", "RockBLOCK Plus talks RS-232 at 19200 baud")
add(S, "Wind-vane angle sensor", "AS5600 magnetic angle board, must fit a 26 x 26 mm recess", 1, "ea", 6, "est", "Adafruit (#6357) or generic",
    "https://learn.adafruit.com/adafruit-as5600-magnetic-angle-sensor", "P03 recess", "Measure the board before printing P03")
add(S, "Vane magnet", "Diametric NdFeB disc 6 x 2.5 mm, N35SH (Radial Magnets 9049)", 2, "ea", 0.75, "web", "DigiKey",
    "https://www.digikey.com/en/products/detail/radial-magnets-inc/9049/6030786", "P04", "One spare")
add(S, "Humidity/pressure sensor", "Adafruit BME280 (#2652)", 1, "ea", 14.95, "web", "Adafruit",
    "https://www.adafruit.com/products/2652", "Bulkhead x 300 (D03)", "")
add(S, "Leak sensor", "Blue Robotics SOS Leak Sensor with probes", 1, "ea", 35.00, "web", "Blue Robotics",
    "https://bluerobotics.com/product-category/sensors-cameras/leak-sensor/", "Sump + box (D03)", "")
add(S, "Servo current sensors", "Adafruit INA260 (#4226)", 2, "ea", 9.95, "web", "Adafruit",
    "https://www.adafruit.com/product/4226", "Rudder servo feeds (D30)", "docs/Rudder_Health_Spec.md")
add(S, "Limp-home orientation sensor", "Adafruit BNO085 9-DOF (#4754)", 1, "ea", 29.50, "web", "Adafruit",
    "https://www.adafruit.com/products/4754", "P21", "")
add(S, "Optocouplers", "6N137 (DIP-8) high-speed optocoupler", 2, "ea", 1.50, "est", "DigiKey / Mouser", "", "P21 (heartbeat in, takeover flag out)", "")
add(S, "Supervisor / external watchdog", "3.3 V supervisor with watchdog (e.g. TI TPS3823-33)", 1, "ea", 3, "est", "DigiKey / Mouser", "", "P21", "")

S = "B Electronics: power"
add(S, "Battery", "Bioenno BLF-1215A, 12.8 V 15 Ah LiFePO4, PVC pack", 1, "ea", 149.99, "web", "Bioenno Power",
    "https://www.bioennopower.com/products/12v-15ah-lifepo4-battery-pvc", "Battery box (D09)", "Charger for the bench: Bioenno 4 A LiFePO4 (optional)")
add(S, "Solar charge controller", "Genasun GV-5-Li-14.2V MPPT, 5 A", 1, "ea", 85.00, "web", "eMarine",
    "https://emarineinc.com/Genasun-MPPT-Solar-Controller-5A-Input-12V-Output", "Main box", "Pick the Li 14.2 V option. Datasheet says IP40: it lives in the sealed box")
add(S, "Solar panels", "PV Logic / Solar Technology STPVF010 10 W Flexi, ETFE, 380 x 250 x 4 mm, IP69, one per deck bay (20 W total)", 2, "ea", 64, "web", "Cactus Navigation (UK) or any PV Logic dealer",
    "https://www.cactusnav.com/flexible-solar-panel-p-19876.html", "Deck (D08)", "Rev E3: stock panel that fits the 280 mm bays. Run 027: 20 W costs no measurable success; about 1 boat in 20 dips to SAFE once. Custom-size 17-20 W panels remain an upgrade")
add(S, "Servo supply regulators", "Pololu D36V50F6, 6 V 5.5 A step-down (#4092)", 2, "ea", 39.95, "web", "Pololu",
    "https://www.pololu.com/product/4092", "Main box + P21", "Limp_Home_Spec asks for about 5.8 V; this one is a fixed 6.0 V, fine with ideal diodes")
add(S, "Servo multiplexer", "Pololu 4-channel RC servo multiplexer, assembled (#2806)", 1, "ea", 17.95, "web", "Pololu",
    "https://www.pololu.com/product/2806", "P22", "FAILMODE jumper set so a lost select gives the master (Pixhawk)")
add(S, "Ideal diodes", "Pololu power ORing ideal diode pair, 4-60 V 6 A (#5398)", 2, "ea", 7.95, "web", "Pololu",
    "https://www.pololu.com/product/5398", "P22", "One per muxed servo (starboard rudder, tail)")
add(S, "Logic supplies", "Pololu D36V6F5, 5 V 600 mA step-down (#3792)", 2, "ea", 5.95, "web", "Pololu",
    "https://www.pololu.com/product/3792", "Main box (companion ESP32) + P21 (limp-home ESP32)", "E2: neither ESP32 had a stated 5 V supply (D30)")
add(S, "Load switches", "Logic-level MOSFET switch boards, 12 V 3 A (pump, nav light, solar cut-off, Pixhawk power-cycle)", 4, "ea", 5, "est", "SparkFun / Pololu", "", "Main box (D30)", "")
add(S, "Fuses and holders", "Waterproof inline ATC blade fuse holders, 16 AWG, + ATC fuse assortment", 1, "set", 20, "est", "Marine store", "", "D30 fuse table", "")
add(S, "Battery connector", "Anderson Powerpole 15/45 housings + contacts, 10 sets", 1, "set", 12, "est", "Powerwerx", "", "Battery box", "The BLF-1215A has a Powerpole lead")

S = "C Electronics: actuators and pump"
add(S, "Rudder servo enclosures", "Blue Trail Engineering SER-2000 sealed servo kit, 6 mm Ti D-shaft", 2, "ea", 215.00, "web", "Blue Trail Engineering",
    "https://www.bluetrailengineering.com/product-page/underwater-servo-ser-200x", "P12 cradles (D05)", "Measure the unit and set SER in design.py, rebuild P12")
add(S, "Servos", "DFRobot SER0066, 25 kg magnetic-encoder servo, IP54", 3, "ea", 21.90, "web", "DFRobot",
    "https://www.dfrobot.com/product-2789.html", "2 in SER-2000s, 1 tail (P09)", "Includes a metal 25T arm: use it as the tail-fin horn")
add(S, "Bilge pump", "12 V R385 self-priming diaphragm pump, 6 mm barbs", 1, "ea", 12, "est", "RobotShop",
    "https://www.robotshop.com/en/6-12v-r385-dc-diaphragm-pump.html", "P24 on the mast tube (D03)", "Motor is about 28 mm diameter, as P24 expects")
add(S, "Pump plumbing", "Strainer, 6 mm silicone hose 2 m, 6 mm inline check valve, 1/4 in nylon through-deck fitting", 1, "set", 20, "est", "Marine / aquarium store", "", "D03", "")
add(S, "Membrane vents", "Amphenol LTW VENT-MS1NME-O8001, M12 stainless, IP68", 2, "ea", 4.15, "web", "Zoro",
    "https://www.zoro.com/amphenol-m12-vent-ss-1760mlmin-sr-vent-ms1nme-o8001/i/G111364227", "Hatch lid + box lid", "Sold in pairs")
add(S, "Test valve", "Schrader valve, bolt-in (tubeless rim valve) with sealing cap", 1, "ea", 5, "est", "Bike shop", "", "Hatch lid", "")
add(S, "Navigation light", "12 V all-round white LED puck, about 30 mm, potted", 1, "ea", 15, "est", "Marine store", "", "P20", "")
add(S, "Slip ring", "6-wire capsule slip ring, 12 mm diameter (Adafruit #775)", 1, "ea", 15, "est", "Adafruit",
    "https://www.adafruit.com/category/223", "Spar foot (D07)", "")

S = "D Electronics: enclosure, cable, penetrations"
add(S, "Electronics box", "Hammond 1554V2GYCL, 239 x 160 x 89 mm, IP68 polycarbonate, clear lid", 1, "ea", 50, "est", "Hammond (distributors)",
    "https://www.hammfg.com/part/1554V2GYCL", "Shelf at x 980-1220 (D03)", "")
add(S, "Cable penetrators", "Blue Robotics WetLink Penetrator M10, LC, seal size to suit each cable OD", 8, "ea", 15, "est", "Blue Robotics / RobotShop",
    "https://www.robotshop.com/products/bluerobotics-wetlink-penetrator-lc-1-pack-m10-65-mm", "D30 penetration table (W1-W8)", "E2: 8, not 6: two more for the battery-box exits. Order the seal size for your cable")
add(S, "Penetrator blanks", "WetLink Penetrator Blank (no hole) M10", 2, "ea", 6.00, "web", "RobotShop",
    "https://www.robotshop.com/products/wetlink-penetrator-blank-no-hole-m10", "Spares", "")
add(S, "RockBLOCK gland", "M20 x 1.5 IP68 nylon cable gland", 1, "ea", 4, "est", "Any", "", "P23", "")
add(S, "Main feed wire", "Tinned marine duplex 14 AWG", 2, "m", 4, "est", "Marine store", "", "Battery to box (D30)", "")
add(S, "Power wire", "Tinned marine duplex 16-18 AWG (Ancor or similar)", 10, "m", 2.5, "est", "Marine store", "", "D30", "")
add(S, "Signal wire", "Tinned 22 AWG hook-up wire, 4 colours", 1, "set", 20, "est", "Any", "", "D30", "")
add(S, "Signal cable", "4-core shielded cable, about 6 mm OD (match the WetLink seal)", 6, "m", 2, "est", "Any", "", "Limp-home links, sensors", "")
add(S, "Connectors", "Locking connectors: JST-GH pre-crimped cable kit + Molex Micro-Fit 3.0 kit", 1, "set", 40, "est", "Any", "", "Main box", "No push-on headers in the box (Electronics_Review)")
add(S, "Heat-shrink", "Adhesive-lined heat-shrink assortment", 1, "set", 15, "est", "Any", "", "All joints", "")
add(S, "Mounting", "3M Dual Lock 25 mm, UV-rated zip ties", 1, "set", 15, "est", "Any", "", "P15 tray", "")
add(S, "Conformal coating", "Acrylic or urethane conformal coat, spray", 1, "can", 20, "est", "MG Chemicals / DigiKey", "", "All boards", "docs/Potting_Spec.md")
add(S, "Urethane potting", "Two-part urethane potting compound, about 375 ml (e.g. MG 8810)", 2, "ea", 45, "est", "MG Chemicals",
    "https://www.mgchemicals.com/category/potting-compounds/urethane-potting-compounds/", "P21, P22, joints", "")
add(S, "Silicone potting", "Soft two-part silicone potting/RTV, about 200 ml", 1, "ea", 25, "est", "MG Chemicals / DigiKey", "", "GPS, BNO085, AS5600", "")

# ------------------------------------------------------------------ E. tracker and safety
S = "E Backup tracker and safety"
add(S, "Backup tracker", "YB Tracking YB3 handheld tracker (GBP 449 + tax)", 1, "ea", 600, "web", "YB Tracking",
    "https://www.ybtracking.com/product-page/yb3-professional", "P19 in the foredeck well", "Price converted from GBP; airtime extra")
add(S, "Radar reflector", "Davis Emergency Radar Reflector 151", 1, "ea", 39.99, "web", "Davis Instruments",
    "https://davisinstruments.com/product/emergency-radar-reflector/", "Stern stub (D07)", "")

# ------------------------------------------------------------------ F. rig, steering, mechanical
S = "F Rig, steering and mechanical"
add(S, "Wing spar, outer tube", "Carbon tube 30 OD x 26 ID, roll-wrapped, 1000 long (cut to 995)", 1, "ea", 35, "est", "Katana Carbon / Wh-shop (eBay)",
    "https://www.ebay.de/itm/294026974744", "D06, D07", "Rev E3: stock outer half of the sleeved 30 x 22 spar")
add(S, "Wing spar, inner sleeve", "R&G CFRP tube wound 3k-PW 26 OD x 22 ID x 1000 (cut to 995), bonded full length inside the outer tube", 1, "ea", 40, "est", "R&G",
    "https://www.r-g.de/en/art/740908SOPO", "D06, D07", "Rev E3. Sand to a sliding fit, bond with thickened laminating epoxy, cure vertical. Same section as 30 x 22. A one-piece special-order 30 x 22 is fine instead")
add(S, "Tail boom", "Carbon tube 16 x 14, 600 long (buy 1 m), roll-wrapped", 1, "ea", 25, "est", "R&G / Easy Composites",
    "https://www.easycomposites.eu/16mm-woven-finish-carbon-fibre-tube", "P08, P09 (D06)", "Rev E1 size")
add(S, "Counterweight arm", "Solid pultruded fibreglass rod, 12.0 mm metric, 246 long (buy 0.5-1 m)", 1, "ea", 12, "est", "Metric composite supplier",
    "", "P08, P18 (D06)", "US 1/2 in (12.7) rod will NOT fit the 12.2 sockets")
add(S, "Stern post", "Pultruded fibreglass tube 20 OD x 16 ID, 500 long", 1, "ea", 15, "est", "Metric composite supplier", "", "P05, P06, P20 (D07)", "")
add(S, "Tail pivot rod", "Carbon rod 6 mm, 200 long", 1, "ea", 6, "est", "Any hobby shop", "", "P10", "")
add(S, "Tail joint rod", "Carbon rod 3 mm, 200 long", 1, "ea", 3, "est", "Any hobby shop", "", "P10", "")
add(S, "Mast tube", "2 in. schedule 40 PVC pipe, 300 mm", 1, "ea", 8, "est", "Hardware store", "", "D07", "")
add(S, "Mast bearings", "6806 acetal (POM) ball bearing, glass balls, 30 x 42 x 7", 3, "ea", 25, "est", "VXB / Bearings Canada",
    "https://bearingscanada.com/products/plastic-bearing-pom-6806-glass-balls-30", "P07", "Third is a spare")
add(S, "Bearing O-rings", "O-ring 42 ID x 1.5 CS, EPDM or NBR", 4, "ea", 1, "est", "Any O-ring supplier", "", "P07 grooves", "")
add(S, "Spar seal", "V-ring VA-30 (NBR)", 1, "ea", 5, "est", "Bearing shop", "", "Spar above P07 (D07)", "")
add(S, "Thrust collar", "Acetal (Delrin) rod 50 mm dia, 25 mm slice, bored 30 (or print in PETG)", 1, "ea", 10, "est", "Any plastics supplier", "", "Spar on P07 (D07)", "")
add(S, "Vane bearings", "S608-2RS stainless 8 x 22 x 7", 3, "ea", 6.79, "web", "Zoro",
    "https://www.zoro.com/tritan-bearings-sealed-8mm-bore-dia-700mm-w-ss608-2rs-fm222/i/G4576419", "P01", "Third is a spare")
add(S, "Vane shaft", "316 stainless round bar 8 mm, 300 long", 1, "ea", 10, "est", "Metals supplier", "", "P01-P04", "Cut to about 80")
add(S, "Rudder stocks", "316 stainless round bar 12 mm, 1 m (two at 360)", 1, "ea", 35, "est", "Metals supplier", "", "D05", "Metric: 1/2 in bar will not fit the 12 mm bushings")
add(S, "Rudder bushings", "igus iglide J flanged bushing JFM-1214-12 (12 bore, 14 OD)", 4, "ea", 1.5, "est", "RS / igus",
    "https://uk.rs-online.com/web/p/plain-bearings/2692785", "Trunks (D05)", "Press into the 14 ID trunk")
add(S, "Rudder trunks", "316 stainless tube 16 OD x 1 wall, 400 long (two at about 150)", 1, "ea", 20, "est", "Metals supplier", "", "D05", "Or GRP tube 14 ID")
add(S, "Trunk seals", "Lip seal 12 x 22 x 5 + rubber boot", 2, "set", 6, "est", "Bearing shop", "", "Trunk tops (D05)", "")
add(S, "G10 plate", "G10/FR4 sheet 10 mm, 150 x 75 (keel-box plate) + 6 mm, 100 x 100 (stops)", 1, "set", 25, "est", "Plastics supplier", "", "D04, D05", "")
add(S, "Fin rods", "316 (A4) threaded rod M10, 1 m (two at about 580)", 1, "ea", 20, "est", "Fastener supplier", "", "D04", "")
add(S, "Pushrods", "M2 316 threaded rod 300 mm + 4 stainless M2 clevises + lock nuts", 1, "set", 15, "est", "RC hobby shop", "", "D32 linkage", "")
add(S, "Overload springs", "316 compression springs, 6 OD x 0.8 wire x 20 long (see D32)", 4, "ea", 2, "est", "Spring supplier", "", "D32 spring link", "Two spare")
add(S, "Spring link tube", "Brass or 316 tube 7 x 0.5, 100 mm", 1, "ea", 4, "est", "Hobby shop (K&S)", "", "D32 spring link", "")
add(S, "Detent magnets", "NdFeB disc 6 x 3 mm, N52", 4, "ea", 0.5, "est", "Any magnet supplier", "", "P25", "Two spare")
add(S, "Detent striker", "Mild steel disc 6 x 1 mm (or a cut washer)", 1, "ea", 0.5, "est", "Any", "", "P10a pocket", "")
add(S, "Clamps", "316 worm-drive hose clamps 20-32 mm", 8, "ea", 2, "est", "Marine store", "", "P12 (4), P19 (2), P24 (2)", "")
add(S, "Battery straps", "25 mm polyester webbing 2 m + 2 cam buckles", 1, "set", 15, "est", "Any", "", "P16", "")
add(S, "Hatch / battery-box seal", "EPDM O-ring cord 4 mm, 3 m", 1, "ea", 10, "est", "O-ring supplier", "", "Hatch (D08), battery box (D09)", "")

# ------------------------------------------------------------------ G. fasteners (all 316 / A4)
S = "G Fasteners (all 316 / A4 stainless)"
add(S, "Set screw M3 x 4", "Cup point, A4", 2, "ea", 0.3, "est", "Fastener supplier", "", "P02", "")
add(S, "Socket cap M3 x 20 + nyloc", "A4", 4, "ea", 0.4, "est", "Fastener supplier", "", "P26 (2), P02 split (1), spare", "")
add(S, "Set screw M4 x 6", "Cup point, A4", 4, "ea", 0.3, "est", "Fastener supplier", "", "P03 (1), P06 (2), spare", "")
add(S, "Socket cap M4 x 30 + nyloc + 2 washers", "A4", 10, "ea", 0.5, "est", "Fastener supplier", "", "P05, P08 (2), P09, P11 (2), P18, P20, spares", "D32 table")
add(S, "Socket cap M5 x 16", "A4, 50-pack covers all M5 x 16", 1, "pk", 7, "est", "Zoro",
    "https://www.zoro.com/zoro-select-m5-080-socket-head-cap-screw-socket-plain-316-stainless-steel-16-mm-length-50-pk-m550500500016/i/G5321845/",
    "Hatch (12), battery-box lid (8), RockBLOCK (4)", "")
add(S, "Socket cap M5 x 30 + nyloc + washers", "A4", 8, "ea", 0.6, "est", "Fastener supplier", "", "P08 ears (2), P06 transom (4), P19 (2)", "")
add(S, "M5 bonded inserts", "316 flanged threaded inserts for bonding in composite (e.g. Bigheads) or nuts glassed to a doubler", 20, "ea", 1.5, "est", "Composite supplier", "", "Hatch (12), battery-box lid (8)", "")
add(S, "M10 nyloc + large washers", "A4", 4, "ea", 1, "est", "Fastener supplier", "", "Fin rods (D04)", "")
add(S, "Pins 4 mm", "316 rod 4 mm, 200 long (cut 4 pins)", 1, "ea", 4, "est", "Metals supplier", "", "P13 (4)", "")
add(S, "Pins 3 mm", "316 rod 3 mm, 200 long (cut 2 pins)", 1, "ea", 3, "est", "Metals supplier", "", "Tiller cross-pins (2)", "")
add(S, "Backing washers", "Fender washers M5, A4", 10, "ea", 0.3, "est", "Fastener supplier", "", "Transom, P19", "")

# ------------------------------------------------------------------ H. composites and hull materials (quantities from the laminate schedule on D31)
S = "H Composites, wood and foam"
add(S, "Hull core", "Divinycell H80 10 mm (3/8 in) PVC foam, about 2 m2 (strips, bulkheads, battery box)", 3, "sheet 1220x610", 45, "est", "R&G / Fibre Glast / Jamestown",
    "https://www.r-g.de/en/art/5800H80", "Hull, bulkheads T17/T18", "US: sold as 4 x 8 ft sheets too")
add(S, "Glass cloth", "6 oz (200 g/m2) E-glass plain weave, 50 in wide", 12, "yd", 9, "est", "TotalBoat / Jamestown / CLC",
    "https://www.totalboat.com/products/6-oz-fiberglass-cloth", "All laminates (D31)", "About 10 m2 needed incl. 15% waste")
add(S, "Glass tape", "6 oz glass tape 3 in (75 mm), 25 yd", 1, "roll", 25, "est", "Marine store", "", "Bulkheads, hull-deck joint, floors (D31)", "")
add(S, "Carbon unidirectional", "Carbon uni tape about 300 g/m2, 50-60 mm wide, 5 m", 1, "roll", 40, "est", "Composite supplier", "", "Fin strips (D04)", "5 layers each side = 1.5 mm")
add(S, "Epoxy", "West System 105-B resin + 205-B fast (or 206-B slow) hardener, 1.2 gal kit", 1, "kit", 198.64, "web", "Fiberglass Supply",
    "https://fiberglasssupply.com/epoxy/west-system/west-system-105-epoxy-resin/west-system-kits-105-epoxy-with-205-fast-hardener/", "All laminates", "About 3.5 L mixed is needed (D31)")
add(S, "Epoxy (top-up)", "West System 105-A + 205-A, 1.2 qt kit", 1, "kit", 92.02, "web", "Fiberglass Supply",
    "https://fiberglasssupply.com/epoxy/west-system/west-system-105-epoxy-resin/west-system-kits-105-epoxy-with-205-fast-hardener/", "Fairing, bonding", "")
add(S, "Metering pumps", "West System 300 mini pumps (B size)", 1, "set", 20, "est", "Marine store", "", "", "")
add(S, "Fillers", "West 406 colloidal silica, 410 Microlight, 404 high-density", 1, "set", 60, "est", "Marine store", "", "Bonding, fillets, fairing", "")
add(S, "Layup consumables", "Peel ply 2 m, mixing cups, stir sticks, chip brushes, foam rollers, squeegees, nitrile gloves", 1, "set", 60, "est", "Any", "", "", "")
add(S, "XPS foam (fill)", "Extruded polystyrene board 2 in (50 mm), 4 x 8 ft", 1, "sheet", 45, "est", "Hardware store", "", "Hull fill (D09), fairing T21", "")
add(S, "XPS foam (wing)", "Extruded polystyrene board 3 in (75 mm), 2 x 8 ft", 1, "sheet", 35, "est", "Hardware store", "", "Wing cores T15 (D06)", "2 in board is too thin: the wing is 56 mm thick")
add(S, "Fin core", "Hardwood (white oak or ash), 25 x 100 x 600, two boards", 2, "ea", 15, "est", "Lumber yard", "", "D04, T12/T13", "")
add(S, "Marine plywood", "9 mm (floors T19/T20) and 3 mm (wing caps), 600 x 600 each", 1, "set", 40, "est", "Lumber yard", "", "D04, D06", "")
add(S, "Building frames", "12 mm MDF or ply, 1220 x 610 (frames T01-T11) + 2 x 6 lumber 2 m (strongback)", 1, "set", 45, "est", "Hardware store", "", "D31 build setup", "Not part of the boat")
add(S, "Lead (bulb)", "Scrap or ingot lead, 10 kg", 10, "kg", 5, "est", "Scrap dealer / fishing supply", "", "D04 bulb (cast)", "Cast outdoors, mask, dry mould")
add(S, "Lead shot", "Lead shot, 2 kg", 2, "kg", 10, "est", "Fishing / reloading supply", "", "P18 (0.91 kg), P02 vane", "")
add(S, "Casting plaster", "Plaster of Paris 10 lb + casting sand", 1, "set", 15, "est", "Hardware store", "", "Bulb mould around P14", "")
add(S, "Sealants", "3M 4200 marine sealant, silicone grease, waterproof trunk grease", 1, "set", 30, "est", "Marine store", "", "", "")
add(S, "Paint", "Epoxy primer, hi-vis orange topside paint, white", 1, "set", 90, "est", "Marine store", "", "D09 labels", "")
add(S, "Antifouling", "Copper ablative antifouling, 1 qt", 1, "ea", 70, "est", "Marine store", "", "Bottom, fin, bulb, rudders", "Three coats (C4)")

# ------------------------------------------------------------------ I. printing filament (from the print guide)
S = "I 3D-printing filament"

# ------------------------------------------------------------------ S. spares recommended
S2 = "S Recommended spares"
add(S2, "Spare MCU", "Adafruit Feather ESP32-S3 (#5477), programmed", 1, "ea", 17.50, "est", "Adafruit", "https://www.adafruit.com/product/5477", "Potted P21 cannot be repaired", "")
add(S2, "Spare servo", "DFRobot SER0066", 1, "ea", 21.90, "web", "DFRobot", "https://www.dfrobot.com/product-2789.html", "", "")

# ------------------------------------------------------------------ print guide
DENS = {"PETG": 1.27, "ASA": 1.07, "PLA": 1.24}
GUIDE = {  # stem: (material, walls, infill, orientation, supports, notes)
 "P00a_fit_test_bores": ("PETG", 3, "100%", "Flat", "None", "Print first, with the filament and settings you will use"),
 "P00b_fit_test_sockets": ("PETG", 3, "100%", "As modelled (holes horizontal)", "None", "Checks the teardrop sockets"),
 "P01_vane_housing": ("ASA", 4, "100%", "As modelled (cavity down)", "None (32 mm bridge at z 34: bridge settings on)", ""),
 "P02_vane_arm": ("ASA", 4, "40%", "As modelled (hub top on the bed)", "None", "275 long: needs a 230 x 230 bed diagonally; brim for the fin"),
 "P02A_vane_arm_hub_split": ("ASA", 4, "40%", "As modelled", "None", "Use P02A + P02B instead of P02 on a small bed"),
 "P02B_vane_arm_fin_split": ("ASA", 4, "40%", "As modelled (fin standing)", "None", "Brim; fin is 3 mm thick"),
 "P03_sensor_cap": ("ASA", 4, "100%", "As modelled (socket down)", "None (E2 chamfer)", ""),
 "P04_magnet_holder": ("PETG", 4, "100%", "As modelled", "None", ""),
 "P05_antenna_platform": ("ASA", 4, "40%", "As modelled", "Build plate only: the D42 GPS pocket under the plate", ""),
 "P06_transom_bracket": ("ASA", 6, "40%", "As modelled", "None", ""),
 "P07_mast_bearing_housing": ("PETG", 4, "100%", "Flange down", "None (E2 chamfer)", "Tallest part (137)"),
 "P08_spar_clamp_two_sockets": ("ASA", 4, "100%", "As modelled", "None", ""),
 "P09_tail_servo_housing": ("ASA", 4, "40%", "As modelled", "None", "Check servo tab spacing first"),
 "P10a_tail_fin_lower": ("PETG", 3, "15%", "Standing on the root", "None", "Brim 5 mm"),
 "P10b_tail_fin_upper": ("PETG", 3, "15%", "Standing", "None", "Brim 5 mm"),
 "P11_tiller_arm": ("PETG", 4, "100%", "Flat", "None", "Print 2"),
 "P12_rudder_servo_cradle": ("PETG", 5, "40%", "Base down", "None", "Print 2; rebuild for your SER-2000 size first"),
 "P13a_rudder_core_upper": ("PETG", 3, "15% gyroid", "Standing", "None", "Print 2; brim"),
 "P13b_rudder_core_lower": ("PETG", 3, "15% gyroid", "Standing", "None", "Print 2; brim"),
 "P14a_bulb_pattern_fwd": ("PLA", 3, "15%", "Split face down", "None", "Pattern only"),
 "P14b_bulb_pattern_aft": ("PLA", 3, "15%", "Split face down", "None", "Pattern only"),
 "P15_electronics_tray": ("PETG", 3, "30%", "Flat", "None", "Trim to the box"),
 "P16_battery_strap_anchor_x4": ("PETG", 4, "40%", "Flat", "None (28 mm slot bridge)", "Print 4"),
 "P17_penetrator_pad_x4": ("PETG", 4, "100%", "Flat", "None", "Print 4 (6 if every WetLink gets one)"),
 "P18_counterweight_pod": ("ASA", 4, "40%", "As modelled", "None", ""),
 "P19_yb3_platform": ("ASA", 5, "40%", "Flat", "None", "Check YB3 size first"),
 "P20_nav_light_clamp": ("ASA", 4, "40%", "As modelled", "None", ""),
 "P21_limp_home_case": ("PETG", 4, "100% back", "Back down", "None", ""),
 "P22_switchover_pod": ("PETG", 4, "40%", "As modelled", "None", ""),
 "P23_rockblock_plus_bowl": ("ASA", 5, "40%", "Floor down", "None (chamfered flange)", ""),
 "P24_bilge_pump_spacer": ("PETG", 5, "40%", "Standing on end", "None", ""),
 "P25_tail_detent": ("PETG", 4, "100%", "Flat", "None", ""),
 "P26_rudder_servo_arm": ("PETG", 4, "100%", "Flat", "None", "Print 2"),
 "P27_vane_bearing_spacer": ("PETG", 4, "100%", "Flat", "None", "E2: new part"),
}

def fill_factor(walls, infill):
    """Rough share of the solid volume a slicer lays down, for small hobby parts."""
    if infill.startswith("100"):
        return 1.0
    pct = float(infill.split("%")[0]) / 100
    return min(1.0, 0.35 + 0.05 * walls + 0.5 * pct)

def print_guide():
    rep = json.load(open(os.path.join(OUT, "stl_report.json")))
    rows = []
    for stem, pid, kw in Pm.BUILD:
        if stem not in rep:
            continue
        r = rep[stem]; P = Pm.PARTS[pid]
        mat, walls, infill, orient, sup, note = GUIDE[stem]
        qty = 4 if stem.endswith("_x4") else (2 if pid in ("P11", "P12", "P13", "P26") else 1)
        if stem.startswith("P02A") or stem.startswith("P02B"):
            qty = 0   # alternative to P02
        g = r["volume_cm3"] * DENS[mat] * fill_factor(walls, infill)
        ext = sorted(r["extent"][:2])
        bed = "230 x 230 (diagonal)" if max(ext) > 220 else "220 x 220"
        rows.append(dict(file=f"stl/{stem}.stl", part=pid, name=P["name"], qty=qty, material=mat,
                         walls=walls, infill=infill, orientation=orient, supports=sup,
                         size_mm=" x ".join(f"{v:.0f}" for v in r["extent"]), min_bed=bed,
                         grams_each=round(g), hours_each=round(g / 12 + 0.3, 1), notes=note))
    return rows

def main():
    pg = print_guide()
    with open(os.path.join(OUT, "Print_Guide.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(pg[0].keys())); w.writeheader(); w.writerows(pg)
    grams = {}
    for r in pg:
        n = r["qty"] if r["qty"] else 0
        grams[r["material"]] = grams.get(r["material"], 0) + r["grams_each"] * max(n, 0)
    # P00 coupons count once; add 30% for failed prints and the split vane option
    for mat, g in grams.items():
        spools = max(1, -(-g * 1.3 // 1000))
        add("I 3D-printing filament", f"{mat} filament", f"1.75 mm, 1 kg spool (parts need about {g/1000:.1f} kg)",
            int(spools), "spool", 25 if mat != "ASA" else 30, "est", "Any", "", "Print_Guide.csv", "Includes 30% for reprints")
    rows = []; count = {}
    for b in sorted(B, key=lambda b: b["section"]):
        line = round(b["qty"] * b["unit_usd"], 2)
        k = b["section"][0]; count[k] = count.get(k, 0) + 1
        rows.append(dict(id=f"{k}{count[k]:02d}", section=b["section"][2:], item=b["item"], specification=b["spec"],
                         qty=b["qty"], unit=b["unit"], unit_usd=b["unit_usd"], line_usd=line, price_basis=b["basis"],
                         supplier=b["supplier"], link=b["link"], used_in=b["used_in"], notes=b["notes"]))
    with open(os.path.join(OUT, "BOM.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    tot = {}
    for r in rows:
        tot[r["section"]] = tot.get(r["section"], 0) + r["line_usd"]
    for k, v in tot.items():
        print(f"{k:45s} {v:9.0f}")
    print(f"{'TOTAL':45s} {sum(tot.values()):9.0f}   ({len(rows)} lines, {sum(1 for r in rows if r['link'])} with links)")
    print("filament g:", {k: round(v) for k, v in grams.items()})

if __name__ == "__main__":
    main()
