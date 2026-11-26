# 50 "What if every ___ vanished overnight?" scripts.
# Each topic: slug, on-screen subject, spoken subject, emoji, hashtags, 7 scenes.
# Scene = (kicker, headline, subline, narration). Figures are rounded, widely cited estimates.

T = []
def add(slug, subject, spoken, emoji, tags, scenes):
    assert len(scenes) == 7, slug
    T.append(dict(slug=slug, subject=subject, spoken=spoken, emoji=emoji, tags=tags, scenes=scenes))

add("moon", "THE MOON", "the Moon", "🌕", "#moon #space #science", [
 ("TIDES SHRINK BY ABOUT", "2/3", "Only the Sun's weaker pull is left.", "Tides shrink by about two thirds. Only the Sun's pull is left."),
 ("TONIGHT", "PITCH BLACK", "No moonlight. Ever again.", "Tonight is pitch black. No moonlight, ever again."),
 ("CORAL REEFS", "CONFUSED", "Many corals spawn by the full moon.", "Coral reefs get confused. Many spawn by the full moon."),
 ("NIGHT HUNTERS", "STRUGGLE", "Owls and lions lose their hunting light.", "Night hunters struggle. Owls and lions lose their hunting light."),
 ("OVER MILLIONS OF YEARS", "EARTH WOBBLES", "The Moon steadies our tilt and seasons.", "Over millions of years, Earth wobbles. The Moon steadies our seasons."),
 ("THE MOST VALUABLE THING NOW", "TIDE CHARTS", "Every one of them is wrong.", "The most valuable thing now? New tide charts. Every old one is wrong."),
 ("GETTING IT BACK?", "NEVER.", "", "Getting it back? Never."),
])
add("bees", "BEE", "bee", "🐝", "#bees #nature #food", [
 ("ANIMAL POLLINATORS HELP", "75%", "of the world's leading food crops.", "Pollinators help about three quarters of the world's leading food crops."),
 ("CALIFORNIA GROWS", "80%", "of the world's almonds. All bee-pollinated.", "California grows eighty percent of the world's almonds. All need bees."),
 ("SUPERMARKETS LOSE", "HALF", "the produce aisle within a few years.", "Supermarkets lose about half the produce aisle within a few years."),
 ("COFFEE, APPLES, AVOCADOS", "SHRINK", "Yields drop. Prices explode.", "Coffee, apples and avocados shrink. Yields drop and prices explode."),
 ("WILDFLOWERS", "FADE", "Birds and animals that eat seeds and fruit follow.", "Wildflowers fade, and the animals that eat their seeds follow."),
 ("THE MOST VALUABLE JOB NOW", "HAND POLLINATOR", "Some pear farms in China already do it by brush.", "The most valuable job now? Hand pollinator. Some farms already do it."),
 ("WHAT KEEPS US FED?", "WIND CROPS", "Wheat, rice and corn don't need bees.", "What keeps us fed? Wheat, rice and corn. They don't need bees."),
])
add("internet", "THE INTERNET", "the internet", "🌐", "#internet #tech #whatif", [
 ("PEOPLE OFFLINE", "5.5 BILLION", "Two thirds of humanity, cut off.", "Five and a half billion people go offline at once."),
 ("CARD PAYMENTS", "FAIL", "Most card readers need a connection.", "Card payments fail. Most card readers need a connection."),
 ("STOCK MARKETS", "FROZEN", "Every exchange trades electronically.", "Stock markets freeze. Every exchange trades electronically."),
 ("DAY 2", "SUPPLY CHAINS JAM", "Orders, shipping and stock all run online.", "Day two. Supply chains jam. Orders and shipping all run online."),
 ("AIRLINES", "GROUNDED", "Booking and flight planning go dark.", "Airlines are grounded. Booking and flight planning go dark."),
 ("THE MOST VALUABLE THING NOW", "CASH", "And anyone who still owns a landline.", "The most valuable thing now? Cash. And anyone with a landline."),
 ("REBUILDING IT?", "YEARS.", "", "Rebuilding all of it? Years."),
])
add("gps", "NAVIGATION SATELLITE", "navigation satellite", "🛰️", "#gps #space #tech", [
 ("GPS ALONE HAS", "31", "satellites. All gone by morning.", "GPS alone has thirty-one satellites. All gone by morning."),
 ("YOUR MAPS APP", "LOST", "The blue dot stops moving.", "Your maps app is lost. The blue dot stops moving."),
 ("CELL NETWORKS & BANKS", "OUT OF SYNC", "They use satellite time to stay in step.", "Cell networks and banks drift out of sync. They use satellite time."),
 ("PILOTS & SHIP CAPTAINS", "OLD SCHOOL", "Radio beacons, radar and charts.", "Pilots and ship captains go old school. Radio beacons and charts."),
 ("DELIVERY & TAXIS", "CRAWL", "Every route is planned by satellite.", "Deliveries and taxis crawl. Every route was planned by satellite."),
 ("THE MOST VALUABLE THING NOW", "PAPER MAPS", "And people who can read them.", "The most valuable thing now? Paper maps, and people who can read them."),
 ("REPLACING THEM?", "YEARS.", "Dozens of rocket launches.", "Replacing them? Years, and dozens of rocket launches."),
])
add("mosquitoes", "MOSQUITO", "mosquito", "🦟", "#mosquito #nature #science", [
 ("MALARIA KILLS ABOUT", "600,000", "people a year. That stops.", "Malaria kills about six hundred thousand people a year. That stops."),
 ("ALSO GONE", "DENGUE & ZIKA", "Spread almost entirely by mosquitoes.", "Dengue and Zika disappear too. Mosquitoes spread them."),
 ("SPECIES LOST", "3,500+", "Only the females of some bite us.", "Over three thousand five hundred species vanish. Only some females bite us."),
 ("ARCTIC BIRDS", "HUNGRY", "Huge summer swarms feed migrating birds.", "Arctic birds go hungry. Summer swarms feed migrating flocks."),
 ("FISH & FROGS", "ADAPT", "Larvae are a snack, not the whole menu.", "Fish and frogs adapt. Larvae were a snack, not the whole menu."),
 ("THE BIGGEST WINNER", "HUMANS", "Mosquitoes are the deadliest animal on Earth.", "The biggest winner? Humans. Mosquitoes are the deadliest animal alive."),
 ("WOULD NATURE MISS THEM?", "BARELY.", "Scientists still argue about it.", "Would nature miss them? Barely. Scientists still argue about it."),
])
add("trees", "TREE", "tree", "🌳", "#trees #nature #earth", [
 ("EARTH HAS ABOUT", "3 TRILLION", "trees. All gone by morning.", "Earth has about three trillion trees. All gone by morning."),
 ("DON'T PANIC", "WE CAN BREATHE", "Ocean plankton makes half our oxygen.", "Don't panic. We can still breathe. Ocean plankton makes half our oxygen."),
 ("FIRST RAIN", "LANDSLIDES", "Roots were holding the hills together.", "With the first rain come landslides. Roots held the hills together."),
 ("THE AMAZON", "DRIES OUT", "That forest makes much of its own rain.", "The Amazon dries out. That forest makes much of its own rain."),
 ("CITIES", "BAKE", "Shade-less streets get much hotter.", "Cities bake. Streets without shade get much hotter."),
 ("THE MOST VALUABLE THING NOW", "WOOD", "Every plank and chair is irreplaceable.", "The most valuable thing now? Wood. Every plank is irreplaceable."),
 ("REGROWING FORESTS?", "CENTURIES.", "", "Regrowing the forests? Centuries."),
])
add("plastic", "PIECE OF PLASTIC", "piece of plastic", "🧴", "#plastic #science #whatif", [
 ("WE MAKE ABOUT", "400M TONS", "of plastic a year. All gone.", "We make about four hundred million tons of plastic a year. All gone."),
 ("HOSPITALS", "CRISIS", "IV bags, syringes and gloves vanish.", "Hospitals are in crisis. IV bags, syringes and gloves vanish."),
 ("YOUR CLOTHES", "FALL APART", "Most fabric now is polyester or nylon.", "Your clothes fall apart. Most fabric now is polyester or nylon."),
 ("CARS", "GUTTED", "Dashboards, bumpers, seats and wiring.", "Cars are gutted. Dashboards, bumpers, seats and wire coatings."),
 ("FOOD", "SPOILS", "No wrappers, bottles or bags.", "Food spoils fast. No wrappers, bottles or bags."),
 ("THE MOST VALUABLE THING NOW", "GLASS JARS", "Grandma was right.", "The most valuable thing now? Glass jars. Grandma was right."),
 ("REPLACING IT ALL?", "DECADES.", "", "Replacing it all? Decades."),
])
add("powergrid", "POWER GRID", "power grid", "⚡", "#electricity #whatif #science", [
 ("FRIDGES WARM UP IN", "4 HOURS", "Then the food starts to spoil.", "Fridges warm up in about four hours. Then food starts to spoil."),
 ("CITY TAPS", "RUN DRY", "Water is pushed by electric pumps.", "City taps run dry. Water is pushed by electric pumps."),
 ("PHONES", "DIE BY NIGHT", "And cell towers go quiet soon after.", "Phones die by night, and cell towers go quiet soon after."),
 ("HOSPITALS", "ON DIESEL", "Backup generators last days, not weeks.", "Hospitals run on diesel. Backup generators last days, not weeks."),
 ("GAS STATIONS", "USELESS", "The pumps need power too.", "Gas stations are useless. The pumps need power too."),
 ("THE MOST VALUABLE THING NOW", "DIESEL", "And anyone with solar panels.", "The most valuable thing now? Diesel, and anyone with solar panels."),
 ("REBUILDING IT?", "YEARS.", "", "Rebuilding the grid? Years."),
])
add("cash", "BANKNOTE AND COIN", "banknote and coin", "💵", "#money #finance #whatif", [
 ("U.S. CASH IN CIRCULATION", "$2 TRILLION+", "Gone by morning.", "Over two trillion dollars of US cash, gone by morning."),
 ("ADULTS WITH NO BANK ACCOUNT", "1.4 BILLION", "Their savings vanish completely.", "One point four billion adults have no bank account. Their savings vanish."),
 ("STREET VENDORS", "STUCK", "Cash-only businesses can't sell.", "Street vendors are stuck. Cash-only businesses can't sell."),
 ("PIGGY BANKS", "EMPTY", "Coin jars and tip jars too.", "Piggy banks are empty. Coin jars and tip jars too."),
 ("CARDS & APPS", "OVERLOADED", "Everyone tries to pay digitally at once.", "Cards and payment apps overload as everyone pays digitally at once."),
 ("THE MOST VALUABLE THING NOW", "BARTER", "Eggs, fuel and favors.", "The most valuable thing now? Barter. Eggs, fuel and favors."),
 ("PRINTING NEW MONEY?", "MONTHS.", "", "Printing new money? Months."),
])
add("smartphones", "SMARTPHONE", "smartphone", "📱", "#phones #tech #whatif", [
 ("PHONES GONE", "4 BILLION+", "From every pocket at once.", "Over four billion phones vanish from every pocket at once."),
 ("LOGINS", "LOCKED", "Two-factor codes go to your phone.", "Logins lock up. Your two-factor codes went to your phone."),
 ("BOARDING PASSES", "GONE", "Tickets, wallets and keys lived on it.", "Boarding passes vanish. Tickets and wallets lived on it."),
 ("NOBODY KNOWS", "ANY NUMBERS", "Can you name five by heart?", "Nobody knows any phone numbers. Can you name five by heart?"),
 ("PHOTOS", "LOST", "Unless they were backed up.", "Years of photos are lost, unless they were backed up."),
 ("THE MOST VALUABLE THING NOW", "LANDLINES", "And paper phone books.", "The most valuable thing now? Landlines and paper phone books."),
 ("BUILDING 4 BILLION MORE?", "YEARS.", "", "Building four billion more? Years."),
])
add("copper", "PIECE OF COPPER", "piece of copper", "🟠", "#copper #science #whatif", [
 ("A U.S. HOME HAS", "400+ LBS", "of copper in its wiring and pipes.", "A typical US home has over four hundred pounds of copper inside."),
 ("POWER GRIDS", "DEAD", "Nearly all wiring is copper.", "Power grids die. Nearly all wiring is copper."),
 ("PIPES", "BURST", "Water floods through the walls.", "Pipes burst. Water floods through the walls."),
 ("ELECTRIC MOTORS", "STOP", "Fans, pumps and EVs all wind copper coils.", "Electric motors stop. Fans, pumps and cars use copper coils."),
 ("PHONES & COMPUTERS", "DEAD", "Copper connects every chip.", "Phones and computers die. Copper connects every chip."),
 ("THE MOST VALUABLE THING NOW", "ALUMINUM", "The next-best conductor we have.", "The most valuable thing now? Aluminum, the next-best conductor."),
 ("REWIRING THE WORLD?", "DECADES.", "", "Rewiring the world? Decades."),
])
add("sand", "GRAIN OF SAND", "grain of sand", "🏖️", "#sand #construction #science", [
 ("WE USE ABOUT", "50B TONS", "of sand and gravel every year.", "We use about fifty billion tons of sand and gravel a year."),
 ("NO SAND, NO", "CONCRETE", "Every building site stops.", "No sand means no concrete. Every building site stops."),
 ("NO SAND, NO", "GLASS", "Windows and screens start from sand.", "No sand means no glass. Windows and screens start from sand."),
 ("CHIPS", "AT RISK", "Silicon is refined from quartz sand.", "Computer chips are at risk. Silicon comes from quartz sand."),
 ("BEACHES", "GONE", "Waves hit the cliffs directly.", "Beaches are gone. Waves hit the cliffs directly."),
 ("WEIRD BUT TRUE", "DESERT SAND", "is too smooth to make good concrete.", "Weird but true: desert sand is too smooth to make good concrete."),
 ("THE MOST VALUABLE THING NOW", "CRUSHED ROCK", "Grind mountains into new sand.", "The most valuable thing now? Crushed rock, ground into new sand."),
])
add("rubber", "PIECE OF RUBBER", "piece of rubber", "🛞", "#rubber #cars #whatif", [
 ("TIRES MADE EACH YEAR", "2 BILLION+", "Every one flat by morning.", "Over two billion tires are made a year. All gone by morning."),
 ("CARS & TRUCKS", "ON RIMS", "Traffic grinds to a halt.", "Cars and trucks sit on bare rims. Traffic grinds to a halt."),
 ("PLANES", "CAN'T LAND", "Landing gear tires are rubber.", "Planes can't land safely. Their tires are rubber."),
 ("ENGINES", "LEAK", "Seals and hoses all fail.", "Engines leak everywhere. Seals and hoses fail."),
 ("HOSPITALS", "NO GLOVES", "Medical gloves are latex or nitrile.", "Hospitals run out of gloves. They're latex or nitrile."),
 ("THE MOST VALUABLE THING NOW", "RUBBER TREES", "Most grow in Southeast Asia.", "The most valuable thing now? Rubber trees. Most grow in Southeast Asia."),
 ("REPLACING IT ALL?", "YEARS.", "", "Replacing it all? Years."),
])
add("glass", "PIECE OF GLASS", "piece of glass", "🪟", "#glass #science #whatif", [
 ("EVERY WINDOW", "OPEN AIR", "Wind and rain pour into homes.", "Every window becomes open air. Wind and rain pour inside."),
 ("INTERNET CABLES", "CUT", "Fiber optic lines are made of glass.", "Internet cables are cut. Fiber optic lines are glass."),
 ("EYEGLASSES", "BILLIONS", "of people suddenly can't see clearly.", "Billions of people suddenly lose their glasses."),
 ("PHONE SCREENS", "GONE", "Touchscreens are a sheet of glass.", "Phone screens vanish. Touchscreens are a sheet of glass."),
 ("LABS", "BLIND", "Microscope lenses and test tubes.", "Labs go blind. Microscope lenses and test tubes are glass."),
 ("THE MOST VALUABLE THING NOW", "SAND & FURNACES", "Glassblowers become rock stars.", "The most valuable thing now? Sand and furnaces. Glassblowers are stars."),
 ("REGLAZING THE WORLD?", "YEARS.", "", "Reglazing the world? Years."),
])
add("oil", "DROP OF OIL", "drop of oil", "🛢️", "#oil #energy #whatif", [
 ("WE USE ABOUT", "100M", "barrels of oil every day.", "We use about one hundred million barrels of oil every day."),
 ("PLANES & SHIPS", "STRANDED", "Almost all run on oil fuels.", "Planes and ships are stranded. Almost all run on oil."),
 ("TRUCKS", "STOP", "Groceries stop arriving.", "Trucks stop, and groceries stop arriving."),
 ("ROADS", "CRUMBLE", "Asphalt is made with oil.", "Roads slowly crumble. Asphalt is made with oil."),
 ("PLASTIC & MEDICINE", "SHORTAGES", "Both start as oil.", "Plastics and many medicines run short. They start as oil."),
 ("THE MOST VALUABLE THING NOW", "BICYCLES", "And electric cars.", "The most valuable thing now? Bicycles, and electric cars."),
 ("SWITCHING OVER?", "DECADES.", "", "Switching the world over? Decades."),
])
add("fertilizer", "BAG OF FERTILIZER", "bag of fertilizer", "🌾", "#farming #food #science", [
 ("SYNTHETIC FERTILIZER FEEDS", "~HALF", "of everyone alive today.", "Synthetic fertilizer helps feed about half of everyone alive."),
 ("NEXT HARVEST", "SHRINKS", "Yields fall dramatically.", "The next harvest shrinks. Yields fall dramatically."),
 ("FOOD PRICES", "SOAR", "Bread, rice, meat. Everything.", "Food prices soar. Bread, rice, meat, everything."),
 ("MEAT", "DISAPPEARS", "Animal feed needs fertilized crops.", "Meat disappears. Animal feed needs fertilized crops."),
 ("FARMERS", "SCRAMBLE", "Back to 1900s farming methods.", "Farmers scramble back to old farming methods."),
 ("THE MOST VALUABLE THING NOW", "MANURE", "Seriously.", "The most valuable thing now? Manure. Seriously."),
 ("RECOVERY?", "YEARS.", "", "Recovery? Years."),
])
add("antibiotics", "ANTIBIOTIC", "antibiotic", "💊", "#medicine #health #science", [
 ("WE'VE HAD THEM SINCE", "1928", "Penicillin changed everything.", "We've had them since nineteen twenty-eight. Penicillin changed everything."),
 ("A SMALL CUT", "DANGEROUS", "Infections can't be stopped.", "A small cut becomes dangerous. Infections can't be stopped."),
 ("SURGERY", "RISKY", "Infection risk soars after every operation.", "Surgery gets risky. Infection risk soars after every operation."),
 ("CANCER TREATMENT", "HARDER", "Chemo patients rely on antibiotics.", "Cancer treatment gets harder. Chemo patients rely on antibiotics."),
 ("FARMS", "STRUGGLE", "Many livestock get antibiotics too.", "Farms struggle. Many livestock get antibiotics too."),
 ("THE MOST VALUABLE THING NOW", "SOAP", "And clean water.", "The most valuable thing now? Soap, and clean water."),
 ("NEW ONES?", "A DECADE+", "Drugs take years to develop.", "New ones? Over a decade. Drugs take years to develop."),
])
add("antarctic-ice", "ANTARCTICA'S ICE", "Antarctica's ice", "🧊", "#antarctica #climate #science", [
 ("SEA LEVEL RISES ABOUT", "58 METERS", "That's a 19-story building.", "Sea level rises about fifty-eight meters. A nineteen story building."),
 ("FLORIDA", "MOSTLY GONE", "Miami is deep underwater.", "Florida is mostly gone. Miami is deep underwater."),
 ("LONDON & SHANGHAI", "FLOODED", "Coastal megacities disappear.", "London and Shanghai flood. Coastal megacities disappear."),
 ("FRESH WATER", "LOST", "Most of Earth's ice is in Antarctica.", "Fresh water is lost. Most of Earth's ice is in Antarctica."),
 ("PENGUINS", "HOMELESS", "Their whole world is ice.", "Penguins are homeless. Their whole world is ice."),
 ("THE MOST VALUABLE THING NOW", "HIGH GROUND", "Mountain towns boom.", "The most valuable thing now? High ground. Mountain towns boom."),
 ("GETTING IT BACK?", "100,000 YRS", "", "Getting it back? A hundred thousand years."),
])
add("ozone", "THE OZONE LAYER", "the ozone layer", "☀️", "#ozone #space #science", [
 ("SQUEEZED TO SEA LEVEL IT'S", "3 MM", "thick. And it shields everything.", "Squeezed to sea level, it's three millimeters thick. It shields everything."),
 ("SUNBURN", "IN MINUTES", "Ultraviolet light floods in.", "Sunburn in minutes. Ultraviolet light floods in."),
 ("SKIN CANCER", "SOARS", "And eye damage, too.", "Skin cancer soars, and eye damage too."),
 ("CROPS", "DAMAGED", "Strong UV harms plant growth.", "Crops are damaged. Strong UV harms plant growth."),
 ("OCEAN PLANKTON", "HIT HARD", "The base of the sea's food web.", "Ocean plankton gets hit hard. It's the base of the food web."),
 ("THE MOST VALUABLE THING NOW", "SHADE", "Life moves indoors and to nighttime.", "The most valuable thing now? Shade. Life moves to nighttime."),
 ("REPAIRING IT?", "CENTURIES?", "We fixed one hole. Not a whole layer.", "Repairing it? Maybe centuries. We fixed one hole, not a whole layer."),
])
add("magnetic-field", "EARTH'S MAGNETIC FIELD", "Earth's magnetic field", "🧲", "#space #earth #science", [
 ("EVERY COMPASS", "SPINS", "North means nothing.", "Every compass just spins. North means nothing."),
 ("SATELLITES", "EXPOSED", "Solar storms hit them head-on.", "Satellites are exposed. Solar storms hit them head on."),
 ("POWER GRIDS", "AT RISK", "Big solar storms can fry transformers.", "Power grids are at risk. Big solar storms can fry transformers."),
 ("BIRDS & TURTLES", "LOST", "Many navigate by magnetism.", "Birds and turtles get lost. Many navigate by magnetism."),
 ("OVER MILLIONS OF YEARS", "AIR LEAKS", "Solar wind strips the atmosphere.", "Over millions of years, solar wind strips away our air."),
 ("THAT HAPPENED TO", "MARS", "It lost its field, then most of its air.", "That happened to Mars. It lost its field, then most of its air."),
 ("GETTING IT BACK?", "NEVER.", "", "Getting it back? Never."),
])
add("cars", "CAR", "car", "🚗", "#cars #cities #whatif", [
 ("CARS ON EARTH", "1.4 BILLION", "All gone by morning.", "There are about one point four billion cars. All gone by morning."),
 ("SUBURBS", "STRANDED", "The nearest store is miles away.", "Suburbs are stranded. The nearest store is miles away."),
 ("BUSES & TRAINS", "PACKED", "Every seat taken for months.", "Buses and trains are packed for months."),
 ("CITY AIR", "CLEANER", "Traffic noise disappears too.", "City air gets cleaner, and traffic noise disappears."),
 ("PARKING LOTS", "EMPTY", "Cities find tons of free space.", "Parking lots sit empty. Cities find tons of free space."),
 ("THE MOST VALUABLE THING NOW", "BICYCLES", "Sold out everywhere.", "The most valuable thing now? Bicycles. Sold out everywhere."),
 ("REPLACING THEM?", "DECADES.", "", "Replacing them all? Decades."),
])
add("planes", "PLANE", "plane", "✈️", "#aviation #travel #whatif", [
 ("FLIGHTS PER DAY", "100,000", "All cancelled by morning.", "About a hundred thousand flights a day, all cancelled."),
 ("AIR CARGO CARRIES ABOUT", "1/3", "of world trade by value.", "Air cargo carries about a third of world trade by value."),
 ("TRAVELERS", "STRANDED", "Overseas with no way home.", "Travelers are stranded overseas with no way home."),
 ("ISLANDS", "CUT OFF", "Ferries become the only link.", "Islands are cut off. Ferries become the only link."),
 ("FRESH FLOWERS & FISH", "VANISH", "They fly in daily.", "Fresh flowers and sushi fish vanish. They fly in daily."),
 ("THE MOST VALUABLE THING NOW", "SHIPS", "Crossing oceans takes a week again.", "The most valuable thing now? Ships. Crossing oceans takes a week again."),
 ("REBUILDING FLEETS?", "DECADES.", "", "Rebuilding the fleets? Decades."),
])
add("container-ships", "CARGO SHIP", "cargo ship", "🚢", "#shipping #trade #whatif", [
 ("SHIPS CARRY ABOUT", "80%", "of world trade by volume.", "Ships carry about eighty percent of world trade by volume."),
 ("PORTS", "EMPTY", "Cranes stand still.", "Ports go empty. The giant cranes stand still."),
 ("HAWAII IMPORTS ABOUT", "85%", "of its food.", "Hawaii imports about eighty-five percent of its food."),
 ("ELECTRONICS & CLOTHES", "SOLD OUT", "Most are shipped from Asia.", "Electronics and clothes sell out. Most ship from Asia."),
 ("OIL TANKERS", "GONE TOO", "Gas prices explode.", "Oil tankers are gone too, so gas prices explode."),
 ("THE MOST VALUABLE THING NOW", "SHIPYARDS", "Every one works around the clock.", "The most valuable thing now? Shipyards, working around the clock."),
 ("REBUILDING?", "DECADES.", "", "Rebuilding the fleet? Decades."),
])
add("undersea-cables", "UNDERSEA CABLE", "undersea internet cable", "🌊", "#internet #ocean #tech", [
 ("THEY CARRY ABOUT", "99%", "of data between continents.", "They carry about ninety-nine percent of data between continents."),
 ("THERE ARE ABOUT", "500+", "of them on the ocean floor.", "There are over five hundred of them on the ocean floor."),
 ("CONTINENTS", "DISCONNECTED", "Your local internet still works.", "Continents disconnect, though your local internet still works."),
 ("FOREIGN WEBSITES", "UNREACHABLE", "Many apps break mid-scroll.", "Foreign websites become unreachable. Many apps break."),
 ("GLOBAL MARKETS", "SPLIT", "New York can't trade with London.", "Global markets split. New York can't trade with London."),
 ("THE MOST VALUABLE THING NOW", "SATELLITE LINKS", "Slow, expensive and overloaded.", "The most valuable thing now? Satellite links. Slow and overloaded."),
 ("RELAYING CABLES?", "YEARS.", "", "Laying new cables? Years."),
])
add("dams", "DAM", "dam", "🌊", "#dams #water #energy", [
 ("HYDROPOWER MAKES ABOUT", "15%", "of the world's electricity.", "Hydropower makes about fifteen percent of the world's electricity."),
 ("RIVERS", "SURGE", "Reservoirs rush downstream.", "Rivers surge as reservoirs rush downstream."),
 ("CHINA'S THREE GORGES", "GONE", "The world's biggest power plant.", "China's Three Gorges Dam, the world's biggest power plant, is gone."),
 ("DRINKING WATER", "LOST", "Many cities store it behind dams.", "Drinking water is lost. Many cities store it behind dams."),
 ("FARMS", "DRY UP", "Irrigation depends on stored water.", "Farms dry up. Irrigation depends on stored water."),
 ("THE MOST VALUABLE THING NOW", "WATER TANKS", "Every drop gets saved.", "The most valuable thing now? Water tanks. Every drop gets saved."),
 ("REBUILDING THEM?", "DECADES.", "", "Rebuilding them? Decades."),
])
add("coffee", "COFFEE BEAN", "coffee bean", "☕", "#coffee #food #whatif", [
 ("CUPS DRUNK EVERY DAY", "2 BILLION+", "None tomorrow.", "Over two billion cups a day. None tomorrow."),
 ("WITHIN A DAY", "HEADACHES", "Caffeine withdrawal kicks in.", "Within a day come the headaches. Caffeine withdrawal kicks in."),
 ("BRAZIL GROWS ABOUT", "1/3", "of the world's coffee.", "Brazil grows about a third of the world's coffee."),
 ("COFFEE FARMERS", "MILLIONS", "lose their income overnight.", "Millions of coffee farmers lose their income overnight."),
 ("CAFES", "CLOSE", "Or become very fancy tea shops.", "Cafes close, or become very fancy tea shops."),
 ("THE MOST VALUABLE THING NOW", "TEA", "And energy drinks.", "The most valuable thing now? Tea, and energy drinks."),
 ("REGROWING IT?", "YEARS.", "Coffee plants take years to fruit.", "Regrowing it? Years. Coffee plants take years to fruit."),
])
add("cacao", "CACAO TREE", "cacao tree", "🍫", "#chocolate #food #whatif", [
 ("NO CACAO MEANS NO", "CHOCOLATE", "Not one bar.", "No cacao means no chocolate. Not one bar."),
 ("IVORY COAST & GHANA GROW", "~60%", "of the world's cocoa.", "Ivory Coast and Ghana grow about sixty percent of the world's cocoa."),
 ("FARM FAMILIES", "MILLIONS", "lose their main crop.", "Millions of farm families lose their main crop."),
 ("CANDY AISLES", "HALF EMPTY", "Cookies, cakes, ice cream too.", "Candy aisles go half empty. Cookies and ice cream too."),
 ("COCOA BUTTER", "GONE", "It's in lip balm and lotion too.", "Cocoa butter is gone. It's in lip balm and lotion too."),
 ("THE MOST VALUABLE THING NOW", "CAROB", "The chocolate stand-in.", "The most valuable thing now? Carob, the chocolate stand-in."),
 ("REGROWING IT?", "5 YEARS", "Cacao trees take years to bear pods.", "Regrowing it? About five years before trees bear pods."),
])
add("bananas", "BANANA", "banana", "🍌", "#bananas #food #science", [
 ("THE WORLD GROWS ABOUT", "135M TONS", "of bananas every year.", "The world grows about a hundred thirty-five million tons of bananas a year."),
 ("THE CAVENDISH IS ABOUT", "HALF", "of all bananas grown.", "The Cavendish is about half of all bananas grown."),
 ("IT HAPPENED BEFORE", "1950s", "A fungus wiped out the Gros Michel.", "It happened before. In the nineteen fifties a fungus wiped out the Gros Michel."),
 ("BANANA FARMS", "COLLAPSE", "Whole economies depend on them.", "Banana farms collapse. Whole economies depend on them."),
 ("BABY FOOD & SMOOTHIES", "CHANGE", "A breakfast staple, gone.", "Baby food and smoothies change. A breakfast staple is gone."),
 ("THE MOST VALUABLE THING NOW", "PLANTAINS", "Wait, those count too.", "The most valuable thing now? Plantains. Wait, those are bananas too."),
 ("BRINGING THEM BACK?", "SEED BANKS", "Wild banana seeds are stored.", "Bringing them back? Seed banks store wild banana varieties."),
])
add("rice", "GRAIN OF RICE", "grain of rice", "🍚", "#rice #food #whatif", [
 ("RICE IS A STAPLE FOR", "3.5 BILLION", "people.", "Rice is a staple for three and a half billion people."),
 ("ASIA GROWS ABOUT", "90%", "of the world's rice.", "Asia grows about ninety percent of the world's rice."),
 ("FOOD PRICES", "SPIKE", "Every other grain gets bought up.", "Food prices spike as every other grain gets bought up."),
 ("SUSHI", "GONE", "Along with risotto and paella.", "Sushi is gone, along with risotto and paella."),
 ("RICE PADDIES", "EMPTY", "Millions of farmers start over.", "Rice paddies sit empty. Millions of farmers start over."),
 ("THE MOST VALUABLE THING NOW", "WHEAT & CORN", "Fields switch overnight.", "The most valuable thing now? Wheat and corn."),
 ("RECOVERY?", "SEED BANKS", "Over 100,000 rice varieties are stored.", "Recovery? Seed banks store over a hundred thousand rice varieties."),
])
add("wheat", "WHEAT PLANT", "wheat plant", "🍞", "#wheat #food #whatif", [
 ("WHEAT GIVES US ABOUT", "20%", "of all the calories humans eat.", "Wheat gives us about twenty percent of all the calories we eat."),
 ("BREAD & PASTA", "GONE", "Pizza, cereal and cake too.", "Bread and pasta are gone. Pizza, cereal and cake too."),
 ("RUSSIA & UKRAINE SUPPLY ABOUT", "~30%", "of wheat exports.", "Russia and Ukraine supply about thirty percent of wheat exports."),
 ("IMPORTING COUNTRIES", "IN TROUBLE", "Egypt is the world's top buyer.", "Importing countries are in trouble. Egypt is a top buyer."),
 ("ANIMAL FEED", "SHORTAGE", "Meat prices rise next.", "Animal feed runs short, so meat prices rise next."),
 ("THE MOST VALUABLE THING NOW", "RICE & POTATOES", "The new bread.", "The most valuable thing now? Rice and potatoes. The new bread."),
 ("RECOVERY?", "SEED BANKS", "Svalbard holds backup seeds.", "Recovery? The Svalbard seed vault holds backups."),
])
add("cows", "COW", "cow", "🐄", "#cows #farming #food", [
 ("CATTLE ON EARTH", "1 BILLION+", "All gone by morning.", "Over a billion cattle, all gone by morning."),
 ("MILK & CHEESE", "GONE", "Butter, yogurt and ice cream too.", "Milk and cheese are gone. Butter and ice cream too."),
 ("BURGERS", "EXTINCT", "Steak becomes a memory.", "Burgers are extinct. Steak becomes a memory."),
 ("LEATHER", "GONE", "Shoes, belts, car seats.", "Leather is gone. Shoes, belts and car seats."),
 ("METHANE", "DROPS", "Cattle are a big source of it.", "Methane drops. Cattle are a big source of it."),
 ("THE MOST VALUABLE THING NOW", "GOATS", "Milk still has a source.", "The most valuable thing now? Goats. Milk still has a source."),
 ("FARMLAND", "FREED UP", "Huge pastures go wild.", "Huge pastures go wild again."),
])
add("chickens", "CHICKEN", "chicken", "🐔", "#chickens #food #whatif", [
 ("CHICKENS ALIVE RIGHT NOW", "25 BILLION+", "More than three per person.", "Over twenty-five billion chickens. More than three per person."),
 ("EGGS", "GONE", "Over a trillion laid each year.", "Eggs are gone. Over a trillion are laid each year."),
 ("BAKERIES", "STRUGGLE", "Cakes and pastries need eggs.", "Bakeries struggle. Cakes and pastries need eggs."),
 ("FAST FOOD", "PANIC", "Nuggets and wings vanish.", "Fast food panics. Nuggets and wings vanish."),
 ("VACCINE MAKERS", "HIT", "Many flu shots are grown in eggs.", "Vaccine makers get hit. Many flu shots are grown in eggs."),
 ("THE MOST VALUABLE THING NOW", "DUCKS", "Duck eggs, anyone?", "The most valuable thing now? Ducks. Duck eggs, anyone?"),
 ("RECOVERY?", "NEVER.", "", "Getting them back? Never."),
])
add("ants", "ANT", "ant", "🐜", "#ants #nature #science", [
 ("ANTS ON EARTH", "20 QUADRILLION", "That's 20,000,000,000,000,000.", "There are about twenty quadrillion ants on Earth."),
 ("THEY OUTWEIGH", "ALL WILD BIRDS", "and wild mammals combined.", "They outweigh all wild birds and mammals combined."),
 ("SOIL", "HARDENS", "Ants tunnel and mix the dirt.", "Soil hardens. Ants tunnel and mix the dirt."),
 ("SEEDS", "STRANDED", "Many plants rely on ants to spread.", "Seeds are stranded. Many plants rely on ants to spread them."),
 ("DEAD BUGS", "PILE UP", "Ants are nature's cleanup crew.", "Dead bugs pile up. Ants are nature's cleanup crew."),
 ("THE BIGGEST LOSER", "ANTEATERS", "Their whole menu, gone.", "The biggest loser? Anteaters. Their whole menu is gone."),
 ("PICNICS", "SAVED", "At least there's that.", "But picnics are saved. At least there's that."),
])
add("earthworms", "EARTHWORM", "earthworm", "🪱", "#worms #soil #nature", [
 ("A FIELD CAN HOLD", "MILLIONS", "of worms per acre.", "A single field can hold millions of worms per acre."),
 ("SOIL", "COMPACTS", "No more tunnels for air and water.", "Soil compacts. No more tunnels for air and water."),
 ("DEAD LEAVES", "PILE UP", "Worms recycle them into soil.", "Dead leaves pile up. Worms recycle them into soil."),
 ("RAIN", "RUNS OFF", "Instead of soaking into the ground.", "Rain runs off instead of soaking into the ground."),
 ("ROBINS & MOLES", "HUNGRY", "Worms are their main meal.", "Robins and moles go hungry. Worms are their main meal."),
 ("DARWIN WROTE", "A WHOLE BOOK", "about why worms matter.", "Darwin wrote a whole book about why worms matter."),
 ("THE MOST VALUABLE THING NOW", "COMPOST", "Farmers fight for it.", "The most valuable thing now? Compost. Farmers fight for it."),
])
add("plankton", "PLANKTON CELL", "plankton cell", "🦠", "#ocean #science #nature", [
 ("THEY MAKE ABOUT", "HALF", "of the oxygen on Earth.", "They make about half the oxygen on Earth."),
 ("KRILL", "STARVE", "They eat phytoplankton.", "Krill starve. They eat phytoplankton."),
 ("WHALES", "STARVE NEXT", "Blue whales eat tons of krill a day.", "Whales starve next. Blue whales eat tons of krill a day."),
 ("FISHERIES", "COLLAPSE", "The whole ocean food web unravels.", "Fisheries collapse. The ocean food web unravels."),
 ("CO2", "RISES", "Plankton soak up carbon.", "Carbon dioxide rises. Plankton soak up carbon."),
 ("THE MOST VALUABLE THING NOW", "LAND FARMS", "The sea stops feeding us.", "The most valuable thing now? Land farms. The sea stops feeding us."),
 ("RECOVERY?", "UNCLEAR.", "", "Recovery? Nobody knows."),
])
add("sharks", "SHARK", "shark", "🦈", "#sharks #ocean #nature", [
 ("SHARKS ARE OLDER THAN", "TREES", "They've survived five mass extinctions.", "Sharks are older than trees. They survived five mass extinctions."),
 ("SPECIES LOST", "500+", "From tiny lanternsharks to whale sharks.", "Over five hundred species vanish."),
 ("MID-SIZE FISH", "BOOM", "No one is keeping them in check.", "Mid-size fish boom. No one keeps them in check."),
 ("SEAGRASS", "OVERGRAZED", "Turtles and rays eat it all.", "Seagrass gets overgrazed. Turtles and rays eat it freely."),
 ("SICK FISH", "SPREAD", "Sharks pick off the weak.", "Sick fish spread disease. Sharks picked off the weak."),
 ("WHO KILLS WHO?", "WE KILL MORE", "Humans kill tens of millions a year.", "Who kills who? Humans kill tens of millions of sharks a year."),
 ("REPLACING THEM?", "NEVER.", "", "Replacing them? Never."),
])
add("clouds", "CLOUD", "cloud", "☁️", "#weather #science #earth", [
 ("CLOUDS COVER ABOUT", "2/3", "of Earth at any moment.", "Clouds cover about two thirds of Earth at any moment."),
 ("NO CLOUDS", "NO RAIN", "Rivers start shrinking.", "No clouds means no rain. Rivers start shrinking."),
 ("DAYS", "SCORCHING", "Clouds reflect sunlight back to space.", "Days get scorching. Clouds reflect sunlight to space."),
 ("NIGHTS", "FREEZING", "Clouds act like a blanket.", "Nights get freezing. Clouds act like a blanket."),
 ("FARMS", "DRY UP", "Rain-fed crops fail first.", "Farms dry up. Rain-fed crops fail first."),
 ("THE MOST VALUABLE THING NOW", "DESALINATION", "Turning seawater into drinking water.", "The most valuable thing now? Desalination plants."),
 ("SKY", "ALWAYS BLUE", "Sunsets get boring.", "The sky is always blue. Sunsets get boring."),
])
add("lithium", "BIT OF LITHIUM", "bit of lithium", "🔋", "#batteries #tech #energy", [
 ("EVERY", "BATTERY", "in phones, laptops and EVs.", "Every lithium battery in phones, laptops and EVs, gone."),
 ("ELECTRIC CARS", "STOPPED", "Millions of them, dead in the driveway.", "Electric cars stop. Millions, dead in the driveway."),
 ("PHONES", "DEAD", "Plug them in, or nothing.", "Phones die. Plug them in, or nothing."),
 ("MEDICINE", "TOO", "Lithium treats bipolar disorder.", "Medicine too. Lithium treats bipolar disorder."),
 ("GRID BATTERIES", "GONE", "Solar power stops at sunset.", "Grid batteries vanish, so solar power stops at sunset."),
 ("THE MOST VALUABLE THING NOW", "LEAD-ACID", "Grandpa's car battery is back.", "The most valuable thing now? Lead acid batteries. Grandpa's back."),
 ("REPLACING IT?", "YEARS.", "Sodium batteries are coming.", "Replacing it? Years. Sodium batteries are coming."),
])
add("microchips", "MICROCHIP", "microchip", "🖥️", "#chips #tech #whatif", [
 ("CHIPS MADE EACH YEAR", "1 TRILLION+", "All gone by morning.", "Over a trillion chips are made a year. All gone."),
 ("A MODERN CAR HAS", "1,000+", "chips inside.", "A modern car has over a thousand chips inside."),
 ("PHONES & LAPTOPS", "DEAD", "Bricks of glass and metal.", "Phones and laptops become bricks."),
 ("MICROWAVES & WASHERS", "DEAD", "Even toasters have chips now.", "Microwaves and washers die. Even toasters have chips."),
 ("TAIWAN'S TSMC MAKES", "~90%", "of the most advanced chips.", "Taiwan's TSMC makes about ninety percent of the most advanced chips."),
 ("THE MOST VALUABLE THING NOW", "OLD TECH", "Analog radios and wind-up clocks.", "The most valuable thing now? Old tech. Analog radios and clocks."),
 ("REBUILDING?", "YEARS.", "A chip factory takes years to build.", "Rebuilding? Years. A chip factory takes years to build."),
])
add("satellites", "SATELLITE", "satellite", "🛰️", "#space #satellites #tech", [
 ("ACTIVE SATELLITES", "10,000+", "All gone by morning.", "Over ten thousand active satellites. All gone by morning."),
 ("WEATHER FORECASTS", "BLIND", "No more hurricane tracking from space.", "Weather forecasts go blind. No hurricane tracking from space."),
 ("GPS", "GONE", "Maps, flights and ships lose their way.", "GPS is gone. Maps, flights and ships lose their way."),
 ("SATELLITE TV & INTERNET", "OFF", "Remote towns go dark.", "Satellite TV and internet switch off. Remote towns go dark."),
 ("SPACE STATION", "GONE TOO", "It's a satellite, technically.", "The space station is gone too. It's technically a satellite."),
 ("THE MOST VALUABLE THING NOW", "ROCKETS", "Every launch is booked.", "The most valuable thing now? Rockets. Every launch is booked."),
 ("REPLACING THEM?", "DECADES.", "", "Replacing them all? Decades."),
])
add("roads", "ROAD", "road", "🛣️", "#roads #cities #whatif", [
 ("THE U.S. ALONE HAS ABOUT", "4M MILES", "of public roads.", "The US alone has about four million miles of public road."),
 ("CARS", "STRANDED", "In driveways, on bare dirt.", "Cars are stranded in driveways, on bare dirt."),
 ("AMBULANCES", "CAN'T REACH", "Fire trucks too.", "Ambulances can't reach anyone. Fire trucks too."),
 ("FIRST RAIN", "MUD", "Everything turns into a swamp.", "With the first rain, everything turns to mud."),
 ("GROCERIES", "STOP", "Trucks can't drive on mud.", "Groceries stop. Trucks can't drive on mud."),
 ("THE MOST VALUABLE THING NOW", "HORSES", "And trains.", "The most valuable thing now? Horses, and trains."),
 ("REPAVING?", "DECADES.", "", "Repaving it all? Decades."),
])
add("aluminum", "PIECE OF ALUMINUM", "piece of aluminum", "🥫", "#aluminum #science #whatif", [
 ("PLANES ARE MOSTLY", "ALUMINUM", "Fleets vanish from runways.", "Planes are mostly aluminum. Fleets vanish from runways."),
 ("CANS", "BILLIONS", "Every soda and beer can, gone.", "Billions of soda cans, gone."),
 ("POWER LINES", "DOWN", "Big transmission lines use aluminum.", "Power lines fall. Big transmission lines use aluminum."),
 ("WINDOWS & DOORS", "FRAMELESS", "Many frames are aluminum.", "Windows and doors lose their frames."),
 ("YOUR KITCHEN", "FOIL-FREE", "And half your pans.", "Your kitchen is foil free, and missing half its pans."),
 ("THE MOST VALUABLE THING NOW", "STEEL", "Heavier, but it works.", "The most valuable thing now? Steel. Heavier, but it works."),
 ("REPLACING IT?", "DECADES.", "", "Replacing it all? Decades."),
])
add("steel", "PIECE OF STEEL", "piece of steel", "🏗️", "#steel #construction #whatif", [
 ("WE MAKE ABOUT", "1.9B TONS", "of steel every year.", "We make about one point nine billion tons of steel a year."),
 ("SKYSCRAPERS", "COLLAPSE", "Steel frames hold them up.", "Skyscrapers collapse. Steel frames hold them up."),
 ("CONCRETE", "CRACKS", "Steel rebar keeps it from breaking.", "Concrete cracks. Steel rebar kept it together."),
 ("CARS & TRAINS", "GONE", "Rails, engines, bodies.", "Cars and trains vanish. Rails, engines, bodies."),
 ("SURGERY TOOLS", "GONE", "Scalpels and implants too.", "Surgery tools are gone, scalpels and implants too."),
 ("THE MOST VALUABLE THING NOW", "IRON ORE", "Back to the furnaces.", "The most valuable thing now? Iron ore. Back to the furnaces."),
 ("REBUILDING?", "DECADES.", "", "Rebuilding everything? Decades."),
])
add("paper", "SHEET OF PAPER", "sheet of paper", "📄", "#paper #whatif #facts", [
 ("BOOKS", "BLANK", "Every library, empty shelves.", "Books vanish. Every library becomes empty shelves."),
 ("CARDBOARD BOXES", "GONE", "Online shopping collapses.", "Cardboard boxes are gone. Online shopping collapses."),
 ("TOILET PAPER", "GONE", "Bidets sell out in minutes.", "Toilet paper is gone. Bidets sell out in minutes."),
 ("RECEIPTS & FORMS", "GONE", "Some offices still run on paper.", "Receipts and forms vanish. Some offices still run on paper."),
 ("WEIRD BUT TRUE", "DOLLARS SURVIVE", "U.S. bills are cotton and linen.", "Weird but true: dollar bills survive. They're cotton and linen."),
 ("THE MOST VALUABLE THING NOW", "WOOD PULP", "Paper mills run nonstop.", "The most valuable thing now? Wood pulp. Paper mills run nonstop."),
 ("RECOVERY?", "MONTHS.", "", "Recovery? Months."),
])
add("salt", "GRAIN OF SALT", "grain of salt", "🧂", "#salt #food #science", [
 ("YOUR BODY", "NEEDS IT", "Sodium keeps nerves and muscles working.", "Your body needs it. Sodium keeps nerves and muscles working."),
 ("FOOD", "BLAND", "And harder to preserve.", "Food gets bland, and harder to preserve."),
 ("WINTER ROADS", "ICY", "No salt for snowy highways.", "Winter roads turn icy. No salt for the highways."),
 ("CHLORINE", "SHORTAGE", "Made from salt. Cleans drinking water.", "Chlorine runs short. It's made from salt and cleans our water."),
 ("PVC PIPES", "TOO", "They're made with chlorine.", "PVC pipes too. They're made with chlorine."),
 ("THE MOST VALUABLE THING NOW", "SEAWATER", "Evaporate it for new salt.", "The most valuable thing now? Seawater. Evaporate it for new salt."),
 ("RECOVERY?", "WEEKS.", "The oceans are full of it.", "Recovery? Weeks. The oceans are full of it."),
])
add("amazon-rainforest", "TREE IN THE AMAZON", "tree in the Amazon", "🌴", "#amazon #rainforest #nature", [
 ("THE AMAZON HOLDS ABOUT", "10%", "of all known species.", "The Amazon holds about ten percent of all known species."),
 ("IT MAKES", "ITS OWN RAIN", "Trees breathe out water vapor.", "It makes its own rain. Trees breathe out water vapor."),
 ("FLYING RIVERS", "STOP", "Moist air that waters Brazil's farms.", "Flying rivers stop. That moist air waters Brazil's farms."),
 ("CARBON", "RELEASED", "Billions of tons stored in its trees.", "Billions of tons of stored carbon get released."),
 ("MEDICINES", "LOST", "Many drugs started as rainforest plants.", "Medicines are lost. Many drugs started as rainforest plants."),
 ("THE MOST VALUABLE THING NOW", "SEEDS", "From botanical gardens worldwide.", "The most valuable thing now? Seeds from botanical gardens."),
 ("REGROWING IT?", "CENTURIES.", "", "Regrowing it? Centuries."),
])
add("glaciers", "GLACIER", "glacier", "🏔️", "#glaciers #water #climate", [
 ("HIMALAYAN ICE FEEDS RIVERS FOR", "~2 BILLION", "people.", "Himalayan ice feeds rivers for nearly two billion people."),
 ("FIRST", "FLOODS", "Meltwater rushes downhill.", "First come floods as meltwater rushes downhill."),
 ("THEN", "DRY SUMMERS", "Rivers lose their summer melt.", "Then dry summers. Rivers lose their summer melt."),
 ("HYDROPOWER", "DROPS", "Less water spins fewer turbines.", "Hydropower drops. Less water spins fewer turbines."),
 ("SKI RESORTS", "CLOSE", "Alpine glaciers gone.", "Ski resorts close. Alpine glaciers are gone."),
 ("THE MOST VALUABLE THING NOW", "RESERVOIRS", "Every drop of snowmelt saved.", "The most valuable thing now? Reservoirs. Every drop gets saved."),
 ("REGROWING THEM?", "THOUSANDS OF YRS", "", "Regrowing them? Thousands of years."),
])
add("elevators", "ELEVATOR", "elevator", "🛗", "#elevators #cities #whatif", [
 ("BURJ KHALIFA", "163 FLOORS", "Take the stairs.", "The Burj Khalifa has a hundred sixty-three floors. Take the stairs."),
 ("ELEVATORS MOVE THE WORLD'S POPULATION EVERY", "3 DAYS", "That's one maker's estimate.", "Elevators move the world's population about every three days."),
 ("TOP FLOORS", "WORTHLESS", "Penthouses become punishments.", "Top floors become worthless. Penthouses become punishments."),
 ("HOSPITALS", "STUCK", "Moving patients between floors.", "Hospitals get stuck moving patients between floors."),
 ("SKYSCRAPERS", "PAUSED", "No new tall buildings.", "Skyscrapers pause. No more tall buildings."),
 ("THE MOST VALUABLE THING NOW", "GROUND FLOORS", "Rent flips upside down.", "The most valuable thing now? Ground floors. Rent flips upside down."),
 ("FITNESS", "UP", "Everyone's legs get stronger.", "On the bright side, everyone's legs get stronger."),
])
add("refrigerators", "FRIDGE", "fridge", "🧊", "#food #history #whatif", [
 ("FRIDGE FOOD STAYS SAFE ABOUT", "4 HOURS", "after it warms up.", "Fridge food stays safe about four hours after it warms up."),
 ("MILK & MEAT", "SPOIL", "Shopping becomes a daily task.", "Milk and meat spoil. Shopping becomes a daily task."),
 ("VACCINES & INSULIN", "AT RISK", "They need cold storage.", "Vaccines and insulin are at risk. They need cold storage."),
 ("SUPERMARKETS", "EMPTY", "Frozen aisles melt.", "Supermarkets empty. Frozen aisles melt."),
 ("IN THE 1800s", "ICE WAS SHIPPED", "from New England around the world.", "In the eighteen hundreds, ice was shipped from New England worldwide."),
 ("THE MOST VALUABLE THING NOW", "ICE", "Ice delivery is back.", "The most valuable thing now? Ice. Ice delivery is back."),
 ("REPLACING THEM?", "YEARS.", "", "Replacing them? Years."),
])
add("air-conditioners", "AIR CONDITIONER", "air conditioner", "❄️", "#heat #climate #whatif", [
 ("AC UNITS WORLDWIDE", "2 BILLION+", "All gone by morning.", "Over two billion AC units, gone by morning."),
 ("PHOENIX & DUBAI", "UNLIVABLE", "Summer can pass 45°C / 113°F.", "Phoenix and Dubai become unlivable in summer."),
 ("DATA CENTERS", "OVERHEAT", "The internet slows down.", "Data centers overheat, and the internet slows down."),
 ("HEAT WAVES", "DEADLIER", "Older people are at most risk.", "Heat waves get deadlier. Older people are at most risk."),
 ("OFFICES", "SIESTA", "Work moves to early mornings.", "Offices adopt the siesta. Work moves to early mornings."),
 ("THE MOST VALUABLE THING NOW", "FANS", "And thick-walled houses.", "The most valuable thing now? Fans, and thick-walled houses."),
 ("REPLACING THEM?", "YEARS.", "", "Replacing them? Years."),
])

assert len(T) == 50, len(T)
import os as _os
exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "topics2.py")).read())
assert len(T) == 100, len(T)
assert len({t["slug"] for t in T}) == 100
exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "topics3.py")).read())
assert len(T) == 130, len(T)
assert len({t["slug"] for t in T}) == 130
