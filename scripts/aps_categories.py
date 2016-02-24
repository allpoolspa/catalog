# All Pool Spa's categorical information for shopify, manufacturers, and distributors.
# This should be kept up to date with shopify.

###############################SHOPIFY##################################
# Each Manufacturer gets a collection
MANUFACTURERS = [
    'Oreq',
    'Aquachek',
    'GAME',
    'Unicel',
    'Val-Pak',
    'U.S. SEAL',
    'Aladddin',
    'Waterway',
    'Zodiac',
    'Pentair',
    'Hayward',
]

# All the collections for the shopify allpoolspa.com
COLLECTIONS = [
    'Popular in Filters',
    'Popular in Pumps',
    'Popular in O-Rings',
    'Popular in Baskets',
    'On Sale',
    'O-Rings & Gaskets',
    'Maintenance',
    'White Goods',
    'Valves',
    'Pool Cleaners',
    'Skimmers',
    'Filters',
    'Pumps',
    'Best Sellers',
    'Spa',
    'Floats & Toys',
    'Accessories',
    'Equipment',
    'Covers',
    'Automation',
    'Sanitization',
    'Lighting',
    'Heaters',
    'Heat Pumps',
    MANUFACTURERS
]

# All The Types (keys) and Tags (values) for shopify allpoolspa.com
POOL_TYPES = ['pool', 'spa', 'commercial', 'residential']
COMMON = ['part', 'accessory', 'miscellaneous', 'maintenance']
TYPES_N_TAGS = {
    'Filters' : [
        'sand',
        'DE',
        'cartridge',
        'valve',
        'separation tank',
        'filter system',
        'replacement',
        POOL_TYPES,
        COMMON,
    ],
    'Pumps' : [
        'variable speed',
        'multiple speed',
        'single speed',
        'motor',
        POOL_TYPES,
        COMMON,
    ],
    'Heaters' : [
        'gas',
        'propane',
        'electric',
        POOL_TYPES,
        COMMON,
    ],
    'Heat Pumps' : [
        POOL_TYPES,
        COMMON,
    ],
    'White Goods' : [
        'skimmer',
        'cover',
        'weir',
        'drain',
        'grate',
        'basket',
        'pvc',
        'plumbing',
        'skimmer',
        'cover',
        'weir',
        'valve',
        'jet',
        'junction box',
        'flow fitting',
        'strainer',
        'anti-entrapment',
        'return',
        'inlet',
        POOL_TYPES,
        COMMON,
    ],
    'Skimmers' : [
        'skimmer',
        'cover',
        'weir',
        'basket',
        POOL_TYPES,
        COMMON,
    ],
    'Lighting' : [
        'fiber optic',
        'LED',
        'floating',
        'fountain',
        'halogen',
        'incandescent',
        'landscape',
        'light',
        'lighting',
        'auto controller',
        'niches',
        'bulb',
        POOL_TYPES,
        COMMON,
    ],
    'Automation' : [
        'control',
        'controller',
        POOL_TYPES,
        COMMON,
    ],
    'O-Rings & Gaskets' : [
        'pump',
        'skimmer',
        'filter',
        'heater',
        'lighting',
        'valve',
        'lubricant',
        'accessory',
        'miscellaneous',
        POOL_TYPES,
        COMMON,
    ],
    'Sanitization' : [
        'salt system',
        'salt',
        'ozone',
        'UV',
        'chlorine'
        'feeder',
        POOL_TYPES,
        COMMON,
    ],
    'Maintenance' : [
        'test kit',
        'leaf rake',
        'vacuum',
        'brush',
        'thermometer',
        'basket',
        'miscellaneous',
        'reagent',
        'test strip',
        'testing',
        'vacuum head',
        'hose',
        POOL_TYPES,
        COMMON,
    ],
    'Deck Accessories' : [
        'rail',
        'water feature',
        'slide',
        'pool access',
        'ladder',
        'diving',
        'lifeguard',
        'game',
        POOL_TYPES,
        COMMON,
    ],
    'Covers' : [
        'winter',
        'solar',
        'heater',
        POOL_TYPES,
        COMMON,
    ],
    'Accessories': [
        'float',
        'toy',
        'thermometers',
        'safety',
        'sign',
        'water feature',
        'maintenance',
        'cover',
        'fountain',
        POOL_TYPES,
        COMMON,
    ],
    'Cleaners': [
        'suction',
        'pressure',
        'robotic',
        'manual',
        'pump',
        POOL_TYPES,
        COMMON,
    ],
    'O-Rings & Gaskets' : [
        'o-ring',
        'gasket',
        POOL_TYPES,
        COMMON,
    ],
    'Valves' : [
        'valve',
        'backwash',
        'filter',
        'multiport',
        'ball',
        'check',
        'diverter',
        'filter control valve',
        POOL_TYPES,
        COMMON,
    ]
}

# All the menus/linklists for the shopify allpoolspa.com navigation
MENUS = {
    "Main Menu": [
        'Manufacturers',
        'Parts',
        'Equipment',
        'Maintenance',
        'Accessories',
        'Spa',
        'Floats & Toys',
    ],
    'Accessories': [
        'Floating Lights'
        'Floats & Toys',
        'Thermometers',
        'Safety',
        'Signs',
        'Water Features',
        'Maintenance',
        'Covers',
    ],
    'Cleaners': [
        'All Pool Cleaners',
        'Suction Cleaners',
        'Robotic Cleaners',
        'Pressure Cleaners',
        'Manual Vacuums',
        'Cleaner Parts',
        'Cleaner Accessories',
    ],
    'Covers': [
        'All Covers',
        'Winter Covers',
        'Solar Covers',
    ],
    'Deck Equipment': [
        'Rails',
        'Water Features',
        'Slides',
        'Pool Access Equipment',
        'Ladders',
        'Diving',
        'Pool Access',
        'Lifeguard',
        'Games',
    ],
    'Equipment': [
        'Filters',
        'Pumps',
        'Heaters',
        'Pool Cleaners',
        'Sanitization',
        'Automation',
        'Skimmers',
        'Lighting',
    ],
    'Spa': [
        'Filters',
        'Heaters',
        'Pumps',
        'Baskets',
        'Jets',
        'Accessories',
    ],
    'Filters': [
        'All Filters',
        'Sand Filters',
        'DE Filters',
        'Cartridge Filters',
        'Filter Parts',
        'Filter Accessories',
    ],
    'Lighting':[
        'All Lights',
        'Pool Lights',
        'Spa Lights',
        'LED Lights',
        'Fiber Optic Lights',
        'Floating Lights',
        'Fountain Lights',
        'Halogen Lights',
        'Incandescent Lights',
        'Landscape Lights',
        'Light Parts',
        'Light Accessories',
    ],
    'Pumps': [
        'All Pumps',
        'Single Speed Pumps',
        'Multiple Speed Pumps',
        'Variable Speed Pumps',
        'Motors',
        'Pump Parts',
        'Pump Accessories',
    ],
    'About All Pool Spa': [
        'About Us',
        'FAQs',
        'Refund & Exchange Policies',
        'Contact Us',
        'Manufacturer Rebates',
        'Privacy & Security Policies',
        'Terms and Conditions',
        'Vendor Relations',
    ],
    'Heaters': [
        'All Heaters'
        'Gas Heaters'
        'Propane Heater'
        'Electric Heaters'
        'Heat Pumps'
        'Heater Parts'
        'Heater Accessories'
    ],
    'White Goods': [
        'skimmers',
        'skimmer covers',
        'skimmer baskets',
        'skimmer weirs'
        'main drains',
        'deck drains',
        'valves',
        'plumbing',
        'jets'
    ],
    'Maintenance' : [
        'Test Kits',
        'Test Strips',
        'Leaf Rakes',
        'Vacuums',
        'Brushes',
        'Thermometers',
        'Baskets',
    ],
    'O-Rings & Gaskets': [
        'Filter O-Rings/Gaskets',
        'Pump O-Rings/Gaskets',
        'Heater O-Rings/Gaskets',
        'Valve O-Rings/Gaskets',
        'Pool Cleaner O-Rings/Gaskets',
        'White Good O-Rings/Gaskets',
        'Light O-Rings/Gaskets',
    ],
    'Parts': [
        'O-Rings & Gaskets',
        'Filter Parts',
        'Pump Parts',
        'Heater Parts',
        'Pool Cleaner Parts',
        'Lighting Parts',
        'Valve Parts',
        'Automation Parts',
        'Skimmer Parts',
        'Plumbing',
        'White Goods',
    ],
    'Pumps': [
        'All Pumps',
        'Single Speed Pumps',
        'Multiple Speed Pumps',
        'Variable Speed Pumps',
        'Motors',
        'Pump Parts',
        'Pump Accessories',
    ],
    'Sanitization' : [
        'All Sanitization',
        'Chlorine',
        'Salt Systems',
        'Ozone',
        'UV',
        'Tablet Feeders',
        'Sanitizatizer Parts    ',
    ],
    'Skimmers': [
        'All Skimmers',
        'Skimmer Units',
        'Skimmer Covers',
        'Skimmer Baskets',
        'Skimmer Weirs',
    ],
}
########################END SHOPIFY#####################################


# Manufacturers and distributor categories
_CATEGORIES = {
    # Optimus
    "Cleaners, Robotic" : "Cleaners, Robotic",
    "Chemical Feeders" : "Chemical Feeders, Sanitization",
    "Cleaners, Suction" : "Cleaners, Suction",
    "DE Filter Modules" : "DE Filter Modules, Filters",
    "Deck and Gutter Drains" : "Deck and Gutter Drains, White Goods",
    "Filter Cartridges" : "Filter Cartridges, Filters",
    "Filters, Cartridge Type" : "Filters, Cartridge Type",
    "Filters, DE, Grid Type" : "Filters, DE, Grid Type",
    "Filters, DE, Module Type" : "Filters, DE, Module Type",
    "Filters, DE, Perflex Type" : "Filters, DE, Perflex Type",
    "Heat Pumps" : "Heat Pumps",
    "Gas Heaters" : "Gas Heaters, Heaters",
    "Filters, Sand, Top Mount" : "Filters, Sand, Top Mount, Valves",
    "Filters, Sand, Side Mount" : "Filters, Sand, Side Mount, Valves",
    "Filter Valves, Top Mount" : "Filter Valves, Top Mount, Valves",
    "Filter Valves, Side Mount" : "Filter Valves, Side Mount, Valves",
    "Filter Valves, Push Pull" : "Filter Valves, Push Pull, Valves",
    "Inlet Fittings" : "Inlet Fittings, White Goods",
    "Light Niches" : "Light Niches, Lighting",
    "Lights, AG Thru Wall" : "Lights, AG Thru Wall, Lighting",
    "Lights, Niche type" : "Lights, Niche type, Lighting",
    "Main Drains" : "Main Drains, White Goods",
    "PH and ORP Controllers" : "PH and ORP Controllers, Automation",
    "Plumbing Unions" : "Plumbing Unions, White Goods",
    "Plumbing Valves" : "Plumbing Valves, White Goods",
    "Pumps" : "Pumps",
    "Seperation Tanks" : "Seperation Tanks, Filters",
    "Skimmers" : "Skimmers",
    "Vacuum Heads" : "Vacuum Heads, Maintenance",
    "Vacuum Release Systems" : "Vacuum Release Systems, White Goods",
    "Valve Actuators" : "Valve Actuators, Automation",
    # SCP
    "Main Drains, Commercial" : "White Goods",
    "Heat Pumps" : "Heat Pumps",
    "Filters, DE" : "Filters, DE",
    "Filter Control Valves" : "Filter Control Valves, Valves",
    "Parts, Whitegoods Flow Fittings, Commercail" : "Parts, White Goods, Flow Fittings, Commercail",
    "Parts, Plumbing" : "Parts, Plumbing, White Goods",
    "Motors, Residential" : "Motors, Residential, Pumps",
    "Parts, Lights Auto Controllers" : "Parts, Lights Auto Controllers, Lighting",
    "Miscellaneous, Maintenance" : "Miscellaneous, Maintenance",
    "Parts, Feeders Chlorinators Sanitizers" : "Sanitization, Parts, Feeders Chlorinators Sanitizers",
    "Heaters, Electric" : "Heaters, Electric",
    "Controls" : "Controls, Automation",
    "Strainers, Commercial" : "Strainers, Commercial, White Goods",
    "Anti-Entrapment Main Drains, Commercial" : "Anti-Entrapment Main Drains, Commercial, White Goods",
    "Service Repair Install" : "Service Repair Install, Maintenance",
    "Chem Feeders" : "Chem Feeders, Sanitization",
    "Miscellaneous, Deck Equipment" : "Miscellaneous, Deck Accessories",
    "Filter Systems, DE" : "Filter Systems, DE, Filters",
    "Motors, Comm" : "Motors, Comm, Pumps",
    "Miscellaneous, Lights Auto Controllers" : "Miscellaneous, Lights Auto Controllers, Lighting",
    "Pool Saftey Devices" : "Pool Saftey Devices, Safety, Accessories",
    "Cleaners, Electric Robotic" : "Cleaners, Robotic",
    "Plumbing Valves Unions" : "Plumbing Valves Unions, Valves",
    "Miscellaneous, Whitegoods Flow Fittings, Comm" : "Miscellaneous, White Goods, Flow Fittings, Comm",
    "Filters, Cartridge, Commercial" : "Filters, Cartridge, Commercial",
    "Junction Box" : "Junction Box, White Goods",
    "Covers, Winter" : "Covers, Winter",
    "Parts, Automatic Cleaners" : "Parts, Automatic Cleaners, Cleaners",
    "Main Drains" : "Main Drains, White Goods",
    "Spa Accessories Hardware" : "Spa Accessories Hardware, Accessories",
    "Test Plugs" : "Test Plugs, White Goods",
    "Parts, Heaters" : "Parts, Heaters",
    "Lubes" : "Lubes, Maintenance",
    "Parts, Filter" : "Parts, Filters",
    "Filters, Sand, Commercial" : "Filters, Sand, Commercial",
    "Designer Fountains" : "Designer Fountains, Accessories",
    "Miscellaneous, Plumbing" : "Miscellaneous, Plumbing, White Goods",
    "Deck Drains Deck Joints Deck Grates" : "Deck Drains Deck Joints Deck Grates, White Goods",
    "Miscellaneous, White Goods Flow Fittings" : "Miscellaneous, White Goods, Flow Fittings",
    "Miscellaneous, White Goods Flow Fittings, Comm" : "Miscellaneous, White Goods, Flow Fittings, Commercial",
    "Return Inlet Fittings" : "Return Inlet Fittings, White Goods",
    "Heater Venting" : "Heater Venting, Heaters",
    "Parts, Pumps" : "Parts, Pumps",
    "Niches" : "Niches, Lighting",
    "Replacement, Cartridges" : "Replacement, Cartridges, Filters, Cartridge",
    "Pool Spa Lights" : "Pool Spa Lights, Lighting",
    "Heaters" : "Heaters",
    "Parts, Whitegoods Flow Fittings" : "Parts, White Goods, Flow Fittings",
    "Separation Tanks" : "Separation Tank, Filters",
    "Alarms, Pool Entry" : "Alarm, Pool Entry, Safety, Accessories",
    "Replacement, DE Grids" : "Replacement, DE, Grid, Filters",
    "Pumps, Commercial" : "Pumps, Commercial",
    "Replacement Bulbs" : "Replacement Bulb, bulb, Lighting",
    "Skimmers" : "Skimmers",
    "Test Meters Labs" : "Test Meters Labs, Maintenance, testing",
    "Parts, Miscellaneous Deck Equipment" : "Parts, Miscellaneous, Deck Accessories",
    "Cleaners, Suction" : "Cleaners, Suction",
    "Parts, Pumps, Commercial" : "Parts, Pumps, Commercial",
    "Pumps, Residential" : "Pumps, Residential",
    "PVC Fittings" : "PVC Fittings, White Goods",
    "Spa, Jets" : "Spa, Jets, White Goods",
    "Chem Feeders, Commercial" : "Chem Feeders, Commercial, Sanitization",
    "Filters, Sand" : "Filters, Sand",
    "Filters, Cartridge" : "Filters, Cartridge",
    "Chlorinators Floating Dispensers" : "Chlorinators Floating Dispensers, Sanitization",
    "Salt Generators, Commercial" : "Salt Generators, Commercial, Sanitization",
    "Plumbing Valves Unions, Commercial" : "Plumbing Valves Unions, Commercial, Valves",
    "Parts, Spa" : "Parts, Spa, White Goods",
    "Miscellaneous, Feeders Chlorinators Santizers" : "Sanitization, Feeders Chlorinators Santizers",
    "Fiber Optics" : "Fiber Optics, Lighting",
    "O-Rings" : "Rings, O-Rings & Gaskets",
    "Filter Systems, Sand" : "Filter Systems, Sand, Filters",
    "Vacuums, All" : "Vacuums, All, Maintenance",
    "Tools, Hand" : "Tools, Hand, Maintenance",
    "Filter Systems, Cartridge" : "Filter Systems, Cartridge, Filters",
    "Cleaners, Pressure" : "Cleaners, Pressure",
    "Salt Generators" : "Salt Generators, Sanitization",
    "Test Kits Reagents" : "Test Kits, Reagents, Maintenance",
    "Cleaners, Commercial" : "Cleaners, Commercial",
    "Filter Control Valves, Commercial" : "Filter Control Valves, Commercial, Valves",
    "Parts, Maintenance" : "Parts, Maintenance",
    "Heaters Gas, Commercial" : "Heaters Gas, Commercial, Heaters",
    "Parts, Filter Accessories" : "Parts, Filter Accessories, Filters",
    # SCP product lines
    "AUTOMATIC CLEANERS" : "Cleaners",
    "HEATERS" : "Heaters",
    "PLUMBING, ALL" : "White Goods",
    "WHITEGOODS FLOW FITTINGS" : "White Goods",
    "POOL SERVICE" : "Maintenance",
    "FEEDERS CHLORINATORS SANTIZERS" : "Sanitization",
    "COVERS" : "Covers",
    "ELECTRICAL" : "Electrical",
    "MAINTENANCE EQUIP" : "Maintenance",
    "DECK EQUIPMENT" : "Deck Accessories",
    "DECK CONSTRUCTION" : "Deck Accessories",
    "PUMPS" : "Pumps",
    "FILTERS" : "Filters",
    "POOL SPA LIGHTING, AUTO CONTROLLERS" : "Lighting, Auto Controllers",
    "WATER FEATURES" : "Accessories, water features",
    "SAFETY" : "Safety",
    "FILTER ACCESSORIES" : "Filters, Accessories",
    "TOOLS" : "Maintenance, Tool",
    "SPA MISC" : "White Goods, Spa",
    "TESTING EQUIPMENT" : "Maintenance, testing",
    # Pentair Optimus
    "Compool / Pentair Pool Control System Circuit Boards": "Pool Controls, Automation",
    "Compool / Pentair Pool Control System Parts": "Pool Controls, Automation",
    "Compool / Pentair Pool Control System Spa Side Remotes": "Pool Controls, Automation",
    "Compool / Pentair Pool Control System Valve Actuators": "Valve Actuators, Automation",
    "Hayward and Pentair Deck & Gutter Drains": "Deck and Gutter Drains, White Goods",
    "Hayward and Pentair Safety Vac Locks": "Cleaners, Accessory",
    "Leaf Vacs, Various Models": "Leaf Vacs, Vacuum, Maintenance",
    "Letro / Pentair Booster Pump, Older version": "Cleaners, Pressure, Pump",
    "Miscellaneous Vacuum Head Parts": "Vacuum Heads, Maintenance",
    "Ortega /Pentair T-Style Diverter Valves": "Plumbing Valves, Valves",
    "Pentair - A.O. Smith Commercial Pump Motors": "Pump Motors, Pumps",
    "Pentair / American Complete Amerlite Pool Lights": "Lights, Lighting, Niche type",
    "Pentair / American Complete Aqualight Spa and Pool Lights": "Lights, Lighting, Niche type",
    "Pentair / American Complete Aqualumin III Pool Lights": "Lights, Lighting, Niche type",
    "Pentair / American Complete Aqualuminator Above Ground Pool Light and Return": "Lights, Lighting, Combo AG",
    "Pentair / American Complete Full Size Stainless Steel Niches": "Light Niches, Lighting",
    "Pentair / American Complete Small Stainless Steel Niches": "Light Niches, Lighting",
    "Pentair / American Complete Spa Brite Spa Lights": "Lights, Lighting, Niche type",
    "Pentair / American Complete Spectrum Amerlite Pool Lights": "Lights, Lighting, Niche type",
    "Pentair / American Complete Spectrum Aqualight Pool and Spa Lights": "Lights, Lighting, Niche type",
    "Pentair / American Products 5 and 8 Position Top Mount": "Filter Valves, Valves, Top Mount",
    "Pentair / American Products 6 Position Top Mount": "Filter Valves, Valves, Top Mount",
    "Pentair / American Products Americana Pump": "Pumps",
    "Pentair / American Products Aqualuminator,Quasar, Quasar 500": "Lights, Lighting, Combo AG",
    "Pentair / American Products Commander Cartridge": "Filters, Cartridge Type",
    "Pentair / American Products Diverter Valve Parts": "Plumbing Valves, Valves",
    "Pentair / American Products Eagle Pump": "Pumps",
    "Pentair / American Products Eclipse & Meteor Top Mount": "Filters, Sand, Top Mount",
    "Pentair / American Products Eclipse Side Mount": "Filters, Sand, Side Mount",
    "Pentair / American Products In Ground Admiral Skimmers": "Skimmers",
    "Pentair / American Products Maxim Pump": "Pumps",
    "Pentair / American Products Predator Cartridge": "Filters, Cartridge Type",
    "Pentair / American Products Push Pull Valve": "Filter Valves, Valves, Push Pull",
    "Pentair / American Products Quantum, CM Series, Cartridge": "Filters, Cartridge Type",
    "Pentair / American Products Quantum, RPM Cartridge": "Filters, Cartridge Type",
    "Pentair / American Products Quantum, Stainless Steel Cartridge": "Filters, Cartridge Type",
    "Pentair / American Products Sandpiper Filter Side Mount": "Filters, Sand, Side Mount",
    "Pentair / American Products Separation Tanks": "Seperation Tanks, Filters",
    "Pentair / American Products Side Mount 1-1/2\"": "Filter Valves, Valves, Side Mount",
    "Pentair / American Products Side Mount 2\"": "Filter Valves, Valves, Side Mount",
    "Pentair / American Products Small Skimmers, FAS 100": "Skimmers",
    "Pentair / American Products Titan, CM DE Filter": "Filters, DE, Grid Type",
    "Pentair / American Products Titan, RPM DE Filter": "Filters, DE, Grid Type",
    "Pentair / American Products Titan, SS DE Filter": "Filters, DE, Grid Type",
    "Pentair / American Products Ultra Flo Pump": "Pumps",
    "Pentair / Compool Complete Diverter Valves": "Plumbing Valves, Valves",
    "Pentair / Compool Diverter Valve Parts": "Plumbing Valves, Valves",
    "Pentair / Hydrel Complete Halogen Spa and Pool Lights": "Lights, Lighting, Niche type",
    "Pentair / Hydrel Sunlite Niche": "Light Niches, Lighting",
    "Pentair / Kreepy E-Z Vac & Kadet Accessories": "Cleaners, Suction",
    "Pentair / Kreepy Krauly 1993 and Prior Accessories": "Cleaners, Suction",
    "Pentair / Kreepy Krauly 1994 - 1999": "Cleaners, Suction",
    "Pentair / Kreepy Krauly 1994 and Prior": "Cleaners, Suction",
    "Pentair / Kreepy Krauly 1994 to Current Accessories": "Cleaners, Suction",
    "Pentair / Kreepy Krauly 2000 to Current": "Cleaners, Suction",
    "Pentair / Kreepy Krauly E-Z Vac": "Cleaners, Suction",
    "Pentair / Kreepy Krauly Kadet": "Cleaners, Suction",
    "Pentair / Kreepy Krauly Legend, Model LL505G": "Cleaners, Pressure",
    "Pentair / Kreepy Krauly Thruster": "Cleaners, Suction",
    "Pentair / Letro - A.O. Smith / Magnetek Cleaner Pump Motors": "Pump Motors, Pumps",
    "Pentair / Letro - Emerson Cleaner Pump Replacement Motors": "Pump Motors, Pumps",
    "Pentair / Letro Autofills, T40 & T40FN": "Autofills, White Goods",
    "Pentair / Letro Inline Thermometers": "Thermometers, Accessories",
    "Pentair / Pac Fab 2\" Slide Valve": "Filter Valves, Valves, Push Pull",
    "Pentair / Pac Fab Hi-Flow 2\"": "Filter Valves, Valves, Side Mount",
    "Pentair / Pac Fab Hydropump, 590 & 700 Series": "Pumps",
    "Pentair / Pac Fab In Ground Bermuda Skimmers": "Skimmers",
    "Pentair / Pac Fab In Ground Skim-Clean Skimmers": "Skimmers",
    "Pentair / Pac Fab Pinnacle Pump": "Pumps",
    "Pentair / Pac Fab Top Mount Valve 1-1/2\"": "Filter Valves, Valves, Top Mount",
    "Pentair / Pac Fac Dynamo Pump": "Pumps",
    "Pentair / Pac-Fab Hatteras Pool Niche": "Light Niches, Lighting",
    "Pentair / Praher Complete Valves": "Filter Valves, Valves, Side Mount",
    "Pentair / Praher Valves, 1-1/2\"": "Filter Valves, Valves, Top Mount",
    "Pentair / Praher Valves, 2\" ": "Filter Valves, Valves, Top Mount",
    "Pentair / Purex 2000 Series Backwash Valve": "Filter Valves, Valves, Bottom Mount",
    "Pentair / Purex C Series Commericial Pump": "Pumps",
    "Pentair / Purex CFW Cartridge, CFW-120, 180, 315, 405": "Filters, Cartridge Type",
    "Pentair / Purex CMF Cartridge, CFM-120, 180, 315": "Filters, Cartridge Type",
    "Pentair / Purex Quietflo & Aquatron": "Pumps",
    "Pentair / Purex SM, SMBW 4000 Series DE": "Filters, DE, Grid Type",
    "Pentair / Purex SMBW 1000 & 2000 Series DE, Stainless": "Filters, DE, Grid Type",
    "Pentair / Purex Stainless DE Separation Tank, SEP-48, 72, 96, 144": "Seperation Tanks, Filters",
    "Pentair / Purex Tahitian Top Mount, HR-21, 25, 31": "Filters, Sand, Top Mount",
    "Pentair / Purex Tahitian Valve": "Filter Valves, Valves, Top Mount",
    "Pentair / Purex Tropic Isle Heaters, 120 - 300": "Gas Heaters, Heaters",
    "Pentair / Purex Whisperflo Pump, Models WF & WFE": "Pumps",
    "Pentair / Rainbow Bromine Feeder": "Chemical Feeders, Sanitization",
    "Pentair / Rainbow Complete DSF Series Skim Filters": "Skimmers",
    "Pentair / Rainbow Complete High Capacity Feeders": "Chemical Feeders, Sanitization",
    "Pentair / Rainbow Complete In Line Feeders": "Chemical Feeders, Sanitization",
    "Pentair / Rainbow Complete Off Line Feeders": "Chemical Feeders, Sanitization",
    "Pentair / Rainbow DSF Skim Filter": "Skimmers",
    "Pentair / Rainbow Flex Vac Heads": "Vacuum Heads, Maintenance",
    "Pentair / Rainbow Floating Feeders": "Floating Chemical Feeders, Sanitization",
    "Pentair / Rainbow Free Standing Feeders": "Chemical Feeders, Sanitization",
    "Pentair / Rainbow In Line Feeders": "Chemical Feeders, Sanitization",
    "Pentair / Rainbow Leaf Trap Model 180": "Leaf Traps, Accessories, Cleaner",
    "Pentair / Rainbow Leaf Trap, Model 179, 179C": "Leaf Traps, Accessories, Cleaner",
    "Pentair / Rainbow Leaf Trap, Model 186": "Leaf Traps, Accessories, Cleaner",
    "Pentair / Rainbow Pro Vac": "Vacuum Heads, Maintenance",
    "Pentair / Rainbow Super Pro Vac, Model 241": "Vacuum Heads, Maintenance",
    "Pentair / Rainbow Swivel Wheel Flex Vac": "Vacuum Heads, Maintenance",
    "Pentair / Rainbow Vinyl Vac": "Vacuum Heads, Maintenance",
    "Pentair / Sta-Rite / Swimquip Inlet Fitting": "Inlet Fittings, White Goods",
    "Pentair / Sta-Rite 4\" Suction Trap, Package 142 & 175": "Pumps",
    "Pentair / Sta-Rite ABG Series Pump": "Pumps",
    "Pentair / Sta-Rite Above Ground Skimmers, 09655-6403, 09655-7403": "Skimmers",
    "Pentair / Sta-Rite Calypso, Model GW7000": "Cleaners, Suction",
    "Pentair / Sta-Rite Complete Swimquip Style Pool Lights": "Lights, Lighting, Niche type",
    "Pentair / Sta-Rite Complete U-3 Gunite Skimmers": "Skimmers",
    "Pentair / Sta-Rite Complete U-3 Standard Mouth Vinyl Liner Skimmers": "Skimmers",
    "Pentair / Sta-Rite Crystal-Flo II Top Mount Sand Filter System": "Filters, Sand, Top Mount",
    "Pentair / Sta-Rite Crystal-Flo Side Mount Sand": "Filters, Sand, Side Mount",
    "Pentair / Sta-Rite Crystal-Flo Top Mount Sand": "Filters, Sand, Top Mount",
    "Pentair / Sta-Rite Crystal-Flo Top Mount Sand, 30\", T-300BP-2": "Filters, Sand, Top Mount",
    "Pentair / Sta-Rite DEP & DEP-01B DE Filter": "Filters, DE, Grid Type",
    "Pentair / Sta-Rite DEP & DEP-01B DE Filter Grid Assembly": "Filters, DE, Grid Type",
    "Pentair / Sta-Rite DEPB DE Filter": "Filters, DE, Grid Type",
    "Pentair / Sta-Rite DEPB DE Filter Grid Assembly": "Filters, DE, Grid Type",
    "Pentair / Sta-Rite DES DE Filter": "Filters, DE, Grid Type",
    "Pentair / Sta-Rite DES DE Filter Grid Assembly": "Filters, DE, Grid Type",
    "Pentair / Sta-Rite GW9500, Inground": "Cleaners, Suction",
    "Pentair / Sta-Rite Great White, Model GW9000": "Cleaners, Suction",
    "Pentair / Sta-Rite HRP Series Sand, HRP-20, 24, 30": "Filters, Sand, Side Mount",
    "Pentair / Sta-Rite HRP-01B Series Sand, HRP20-01B, 24-01B, 30-01B": "Filters, Sand, Side Mount",
    "Pentair / Sta-Rite HRPB Series Sand, HRPB-20, 24, 30": "Filters, Sand, Side Mount",
    "Pentair / Sta-Rite In Ground Skimmers, U-3": "Skimmers",
    "Pentair / Sta-Rite Light, 5082, 5086": "Lights, Lighting, Niche type",
    "Pentair / Sta-Rite Lil Shark, Model GW8000": "Cleaners, Suction",
    "Pentair / Sta-Rite Max-E-Therm Heaters, SR200, 333, 400": "Gas Heaters, Heaters",
    "Pentair / Sta-Rite Modular DE, S7MD60, S7MD72": "Filters, DE, Module Type",
    "Pentair / Sta-Rite Multiport, 1-1/2\" WC112 Series": "Filter Valves, Valves, Top Mount",
    "Pentair / Sta-Rite PRC, PRD, Cartridge and DE Filters": "Filters, DE, Module Type",
    "Pentair / Sta-Rite Plastic Slide Valve": "Filter Valves, Valves, Push Pull",
    "Pentair / Sta-Rite Pool Shark, Models GW7500, GW7700": "Cleaners, Suction",
    "Pentair / Sta-Rite Posi-Clear Cartridge System, PXC75, 95, 125, 150": "Filters, Cartridge Type",
    "Pentair / Sta-Rite Posi-Flo II Cartridge, PTM-135": "Filters, Cartridge Type",
    "Pentair / Sta-Rite Posi-Flo II Cartridge, PTM-50, 70, 100": "Filters, Cartridge Type",
    "Pentair / Sta-Rite Posi-Flo SS Cartridge, 1 Piece Tank, TX Models": "Filters, Cartridge Type",
    "Pentair / Sta-Rite Posi-Flo SS Cartridge, 2 Piece Tank, TX, TXR Models": "Filters, Cartridge Type",
    "Pentair / Sta-Rite Sidemount": "Filter Valves, Valves, Side Mount",
    "Pentair / Sta-Rite Sidemount Valves": "Filter Valves, Valves, Side Mount",
    "Pentair / Sta-Rite Sunbrite Halogen Light": "Lights, Lighting, Niche type",
    "Pentair / Sta-Rite Sunbrite LTC Light": "Lights, Lighting, Niche type",
    "Pentair / Sta-Rite Sunburst Halogen Light": "Lights, Lighting, Niche type",
    "Pentair / Sta-Rite Sunglow Light": "Lights, Lighting, Niche type",
    "Pentair / Sta-Rite Sunstar AG Halogen Light": "Lights, Lighting, AG Thru Wall",
    "Pentair / Sta-Rite Swimquip Bronze Slide Valve": "Filter Valves, Valves, Push Pull",
    "Pentair / Sta-Rite Swimquip Multiport, 1-1/2\"": "Filter Valves, Valves, Top Mount",
    "Pentair / Sta-Rite System 2, Mod Media and Mod DE System, PLM & PLD Models": "Filters, DE, Module Type",
    "Pentair / Sta-Rite System 2, Modular DE, PLDE36, PLDE48": "Filters, DE, Module Type",
    "Pentair / Sta-Rite System 3 Cartridge, S7M120, S8M150, S7M400, S8M500": "Filters, Cartridge Type",
    "Pentair / Sta-Rite System 3 DE Filter": "Filters, DE, Grid Type",
    "Pentair / Sta-Rite System 3 Sand, S7S50, S8S70": "Filters, Sand, Side Mount",
    "Pentair / Sta-Rite Thermoplastic DE Separation Tank, 60SEP": "Seperation Tanks, Filters",
    "Pentair / Sta-Rite Top Mount 2\" ": "Filter Valves, Valves, Top Mount",
    "Pentair / Sta-Rite Unions": "Plumbing Unions, White Goods",
    "Pentair / Sta-Rite Vinyl Niche, 0568-0121 & 0568-0171": "Light Niches, Lighting",
    "Pentair Above Ground Hydro-Skim Skimmers": "Skimmers",
    "Pentair Aerators": "Aerators",
    "Pentair Amerlite Pool Light": "Lights, Lighting, Niche type",
    "Pentair Amerquartz Light": "Lights, Lighting, Niche type",
    "Pentair Aqualight Halogen": "Lights, Lighting, Niche type",
    "Pentair Aqualumin II, Aqualumin II Light": "Lights, Lighting, Aqualumin",
    "Pentair Aqualumin, Aqualumin II Mounting Bracket": "Lights, Lighting, Aqualumin",
    "Pentair Booster Pump, Current version, Model LAO1N": "Cleaners, Pressure",
    "Pentair CF Cartridge, CF-40, 60, 80": "Filters, Cartridge Type",
    "Pentair Cartridges, 13 Inch and over Diameter": "Filter Cartridges, Filters",
    "Pentair Challenger Pump": "Pumps",
    "Pentair Clean and Clear / Predator Cartridge System": "Filters, Cartridge Type",
    "Pentair Clean and Clear Plus Cartridge": "Filters, Cartridge Type",
    "Pentair Commercial Pool Control Parts, LX80, LX820": "Pool Controls, Automation",
    "Pentair Complete AQL Aqualuminator Above Ground Light and Return": "Lights, Lighting, Combo AG",
    "Pentair Complete Aqualumin III Vinyl Liner Mounting Brackets": "Lights, Lighting, Aqualumin",
    "Pentair Complete Intellibrite 5G White Pool Lights": "Lights, Lighting, Niche type",
    "Pentair Complete Intellibrite 5G White Spa Lights": "Lights, Lighting, Niche type",
    "Pentair Complete Plastic Niches": "Light Niches, Lighting",
    "Pentair Complete Quasar 500 Above Ground Pool Light": "Lights, Lighting, AG Thru Wall",
    "Pentair DE Filter Modules": "DE Filter Modules, Filters",
    "Pentair DM Cartridge, DM-75, 90, 120, 180, 240": "Filters, Cartridge Type",
    "Pentair Deck Jet I": "Deck Jets, White Goods",
    "Pentair Deck Jet II": "Deck Jets, White Goods",
    "Pentair EQ Commercial Pump": "Pumps",
    "Pentair Easytouch Pool Control Parts": "Pool Controls, Automation",
    "Pentair Fiberworks Lenses": "Lights, Lighting, Fiber Optic",
    "Pentair Fiberworks PG2000 Photon Generator": "Lights, Lighting, Fiber Optic",
    "Pentair Fiberworks Photon Generator": "Lights, Lighting, Fiber Optic",
    "Pentair Full Flow Valve": "Filter Valves, Valves, Push Pull",
    "Pentair Full Size SS Niches": "Light Niches, Lighting",
    "Pentair Hi-Lite Pool Light": "Lights, Lighting, Niche type",
    "Pentair Intellibrite 5G Color LED Pool Light - After 2009": "Lights, Lighting, Niche type",
    "Pentair Intellibrite 5G Color LED Spa Light - After 2009": "Lights, Lighting, Niche type",
    "Pentair Intellibrite White LED Pool Light - After 2009": "Lights, Lighting, Niche type",
    "Pentair Intellibrite, Colored LED Light": "Lights, Lighting, Niche type",
    "Pentair Intellibrite, White LED Light": "Lights, Lighting, Niche type",
    "Pentair Intellichlor": "Salt Chlorine Generators, Sanitization",
    "Pentair Intelliflo Pump, Models VS3050 and VF": "Pumps",
    "Pentair Intellipro Pump, Model VS 3050": "Pumps",
    "Pentair Intellitouch Pool Control Parts": "Pool Controls, Automation",
    "Pentair Jet Vac": "Cleaners, Pressure",
    "Pentair Junction Box": "Junction Boxes, White Goods",
    "Pentair Kreepy Krauly Sandshark": "Cleaners, Suction",
    "Pentair Kreepy Kruiser": "Cleaners, Suction",
    "Pentair Kreepy Legend II, LX5000G, Head Parts": "Cleaners, Pressure",
    "Pentair Legend II, LX-2000, Head Parts & Tune Up Kit": "Cleaners, Pressure",
    "Pentair Legend Platinum": "Cleaners, Pressure",
    "Pentair Legend, 3 Wheel Version, Parts & Tune Up Kits ": "Cleaners, Pressure",
    "Pentair Legend, 4 Wheel Version, Head Parts": "Cleaners, Pressure",
    "Pentair Legend, Hose and Back Up Valves": "Cleaners, Pressure",
    "Pentair Magic Stream Laminars": "Deck Jets, White Goods",
    "Pentair Mastertemp Heaters, 175 - 400": "Gas Heaters, Heaters",
    "Pentair Mastertemp Heaters, Electrical System": "Gas Heaters, Heaters",
    "Pentair Mastertemp Heaters, Water System": "Gas Heaters, Heaters",
    "Pentair Mini Max Heaters (1991 - 1997)": "Gas Heaters, Heaters",
    "Pentair Mini Max Heaters, Heat Exchangers, (1991 - 1997)": "Gas Heaters, Heaters",
    "Pentair Minimax AG Heaters, 75, 100, 100SC": "Gas Heaters, Heaters",
    "Pentair Minimax CH Heaters, 150 - 400": "Gas Heaters, Heaters",
    "Pentair Minimax Heaters, Burner Trays (1991 - 1997)": "Gas Heaters, Heaters",
    "Pentair Minimax NT Heaters, NT TSI, NT LN, NT STD, 200 - 400": "Gas Heaters, Heaters",
    "Pentair Minimax Plus Heaters, 150 - 400": "Gas Heaters, Heaters",
    "Pentair Mitra Stainless Cartridge, MA-60, 80, 100, 160": "Filters, Cartridge Type",
    "Pentair Mytilus B Fiberglass Cartridge, MY-60B, 80B, 100B": "Filters, Cartridge Type",
    "Pentair Mytilus FG Cartridge, MY-60, 80, 100": "Filters, Cartridge Type",
    "Pentair Mytilus Fiberglass Cartridge FMY-80, 100, 150": "Filters, Cartridge Type",
    "Pentair Nautilus FNS DE, FNS-24, 36, 48, 60": "Filters, DE, Grid Type",
    "Pentair Nautilus FNS Plus DE, 180006, 180007, 180008, 180009": "Filters, DE, Grid Type",
    "Pentair Nautilus Plus DE Stainless, NSP-36, 48, 60, 72": "Filters, DE, Grid Type",
    "Pentair Nautilus Stainless DE, NS-24, 36, 48, 60, 72": "Filters, DE, Grid Type",
    "Pentair Optiflo Pump, 3/4 to 1-1/2 HP": "Pumps",
    "Pentair PF Stainless Steel, Side Mount Sand PF-35, 50": "Filters, Sand, Side Mount",
    "Pentair Plastic Full Size and Small Niches": "Light Niches, Lighting",
    "Pentair Plastic Slide Valves": "Filter Valves, Valves, Push Pull",
    "Pentair Prowler 710": "Cleaners, Robotic",
    "Pentair Prowler 720, 730": "Cleaners, Robotic",
    "Pentair Quad DE, Models 60, 80, 100": "Filters, DE, Module Type",
    "Pentair Quick Niche": "Light Niches, Lighting",
    "Pentair R Series Commercial Pump, 5 to 15 HP": "Pumps",
    "Pentair Replacement Skimmer Lids with Thermometers": "Skimmers",
    "Pentair Return Line Eyeball Check Valves": "Inlet Fittings, Valves",
    "Pentair Round Starguard 8\" Mains Drains, Frame & Covers": "Main Drains, White Goods",
    "Pentair Sand Dollar Top Mount Sand System, SD-30 Thru SD-80": "Filters, Sand, Top Mount",
    "Pentair Sea Horse FG Cartridge, FSH-300, 400, 500": "Filters, Cartridge Type",
    "Pentair Sea Horse Stainless Cartridge SH-300, 400, 500": "Filters, Cartridge Type",
    "Pentair Separation Tank, S-20, S-30": "Seperation Tanks, Filters",
    "Pentair Small SS Niches": "Light Niches, Lighting",
    "Pentair Spectrum Amerlight, SAM": "Lights, Lighting, Niche type",
    "Pentair Spectrum Aqualight (SAL) Multicolor Spa Light": "Lights, Lighting, Niche type",
    "Pentair Star DE, ST-35, 40, 50, 80": "Filters, DE, Grid Type",
    "Pentair Suntouch Pool Control Parts": "Pool Controls, Automation",
    "Pentair Superflo Pump": "Pumps",
    "Pentair Tagelus Top Mount Sand, TA-35D thru TA-100D, TA30 Thur TA-60": "Filters, Sand, Top Mount",
    "Pentair Triton C-3 Side Mount Sand, TR100C-3, TR140C-3": "Filters, Sand, Side Mount",
    "Pentair Triton Commercial Side Mount Sand, TR100C, TR140C": "Filters, Sand, Side Mount",
    "Pentair Triton II Side Mount Sand, TR-40, 50, 60, 100, 100HD, 140": "Filters, Sand, Side Mount",
    "Pentair Valve Actuators": "Valve Actuators, Automation",
    "Pentair Warrior FG DE, 44, 66, 88 GPM": "Filters, DE, Grid Type",
    "Pentair and Hayward Insider Inlet Fittings": "Inlet Fittings, White Goods",
    "Replacement Skimmer Baskets": "Skimmers",
    "Vacuum Pole Parts": "Vacuum Poles, Maintenance",
    "Pentair / Rainbow Feeder Accessories" : "Chemical Feeders, Sanitization",
    "Pentar / American Products Autofills" : "Autofills, White Goods",
    "Pentair CPVC Check Valves" : "Check Valves, Valves",
    "Pentair / Rainbow Complete Dynamic Series Top Load Cartridge Filters" : "Cartridge Filters, Filters",
    "Pentair / Rainbow Complete Dynamic Series In Line Cartridge Filters" : "Cartridge Filters, Filters",
    "Pentair / Rainbow Dynamic Series I Inline Cartridge Filter" : "Cartridge Filters, Filters",
    "Pentair / Rainbow Series IV Cartridge Filter, DFM & DFML" : "Cartridge Filters, Filters",
    "Pentair / Rainbow Dynamic Series II & III Top Load Cartridge Filters" : "Cartridge Filters, Filters",
    "Pentair / Rainbow Module Cartridge Filter" : "Cartridge Filters, Filters",
    "Pentair / Rainbow High Capacity Automatic Feeders" : "Feeders, Sanitization",
    "Pentair / Sta-Rite Sunsaver Halogen Light": "Lighting",
    "Pentair / Pac-Fab Hatteras Pool Light" : "Lighting"
}