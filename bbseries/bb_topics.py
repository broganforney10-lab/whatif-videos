# "Baseball What Ifs" scripts. Each topic: hook + 7 scenes. Scene = (kicker, headline, sub, narration, act).
# Acts drive the 3D shots (see make_bb.py). Figures are widely cited; keep narration ~12 words per 4.5 s scene.
T = []


def add(slug, title, hook, scenes, tags, set_="park"):
    assert len(scenes) == 7, slug
    T.append(dict(slug=slug, title=title, hook=hook, scenes=scenes, tags=tags, set=set_))


add("moon", "What if you hit a baseball on the Moon?",
    ("WHAT IF", "MOON BALL", "you hit a home run on the Moon?", "What if you hit a baseball on the Moon?", "moonstand"),
    [("GRAVITY ON THE MOON", "1/6", "of Earth's pull.", "Gravity on the Moon is only one sixth of Earth's.", "moonstand2"),
     ("NO AIR MEANS", "NO DRAG", "Nothing slows the ball down.", "And there's no air, so nothing slows the ball down.", "moonswing"),
     ("A NORMAL HOME RUN SWING GOES", "3,700 FT", "Over half a mile.", "A normal home run swing sends it over half a mile.", "moonflight"),
     ("HANG TIME", "~30 SEC", "Fielders could jog to it.", "It hangs in the air for almost thirty seconds.", "moonflight2"),
     ("CURVEBALLS", "DON'T CURVE", "Spin needs air to bend a pitch.", "Curveballs stop curving. Spin needs air to bend a pitch.", "moonpitch"),
     ("IT'S SORT OF BEEN DONE", "1971", "Alan Shepard hit golf balls up there.", "It's sort of been done. In 1971, Alan Shepard hit golf balls up there.", "moonstand"),
     ("THE BALLPARK YOU'D NEED", "MILES WIDE", "", "The ballpark you'd need? Miles wide.", "moonwide")],
    "#baseball #moon #space #physics", set_="moon")

add("120mph", "What if a pitcher threw 120 mph?",
    ("WHAT IF", "120 MPH", "a pitcher threw this fast?", "What if a pitcher threw a hundred and twenty miles per hour?", "pitch"),
    [("FASTEST PITCH EVER RECORDED", "105.8 MPH", "Aroldis Chapman, 2010.", "The fastest pitch ever recorded was a hundred and five point eight.", "stat"),
     ("AT 120 MPH IT ARRIVES IN", "0.3 SEC", "Faster than a blink.", "At one twenty, it reaches the plate in three tenths of a second.", "pitch"),
     ("HITTERS", "JUST GUESS", "There's no time to read the spin.", "Hitters can't react anymore. They just guess and swing.", "swingmiss"),
     ("STRIKEOUTS", "EXPLODE", "Most at-bats end in three pitches.", "Strikeouts explode. Most at-bats are over in three pitches.", "crowdsad"),
     ("THE PITCHER'S ELBOW", "BREAKS", "Arms already tear near 100 mph.", "But his elbow probably breaks. Arms already tear near a hundred.", "hurt"),
     ("IF YOU DO MAKE CONTACT", "IT FLIES", "Faster pitch, faster exit speed.", "And if you do make contact, the ball flies even farther.", "homer"),
     ("COULD A HUMAN DO IT?", "NOT YET.", "", "Could a human ever do it? Not yet.", "think")],
    "#baseball #mlb #pitching #physics")

add("mound", "What if they moved the pitcher's mound back?",
    ("WHAT IF", "MOUND BACK", "they moved the pitcher's mound back?", "What if they moved the pitcher's mound back?", "pitch"),
    [("BEFORE 1893, PITCHERS THREW FROM", "50 FEET", "Much closer than today.", "Before 1893, pitchers threw from just fifty feet away.", "pitch"),
     ("THEN THEY MOVED IT TO", "60 FT 6 IN", "Where it still is today.", "Then baseball moved it to sixty feet, six inches. It's still there.", "stat"),
     ("LEAGUE BATTING AVERAGE BY 1894", ".309", "Up from .245 in 1892.", "Batting averages exploded, to over three hundred by 1894.", "swing"),
     ("1894 PHILLIES OUTFIELD", "4 HIT .400", "All four, in one season.", "That year, four Phillies outfielders all hit over four hundred.", "crowd"),
     ("IN 2021, A LEAGUE TESTED", "61 FT 6 IN", "One more foot back.", "In 2021, the Atlantic League tested moving it back one more foot.", "pitch"),
     ("MOVE IT BACK 5 MORE FEET?", "OFFENSE BOOMS", "Breaking balls hang longer.", "Move it back five more feet, and offense booms all over again.", "homer"),
     ("WOULD FANS LOVE IT?", "PROBABLY.", "", "Would fans love it? Probably.", "crowd")],
    "#baseball #mlb #history #pitching")

add("nogloves", "What if baseball banned gloves?",
    ("WHAT IF", "NO GLOVES", "baseball banned them?", "What if baseball banned gloves?", "glove"),
    [("EARLY PLAYERS CAUGHT WITH", "BARE HANDS", "Gloves caught on in the 1870s and 80s.", "Early players caught barehanded. Gloves only caught on in the 1870s.", "glove2"),
     ("A LINE DRIVE CAN LEAVE THE BAT AT", "100+ MPH", "Straight at your palm.", "A line drive can leave the bat at over a hundred miles per hour.", "swing"),
     ("ERRORS", "EVERYWHERE", "Dropped balls on almost every play.", "Errors everywhere. Dropped balls on almost every play.", "glove"),
     ("CATCHERS", "CAN'T CATCH", "Nobody barehands 95 mph.", "Catchers can't catch. Nobody barehands a ninety five mile per hour fastball.", "pitch"),
     ("SO PITCHERS", "SLOW DOWN", "", "So pitchers have to slow way down.", "think"),
     ("SCORES GO", "DOUBLE DIGITS", "Like the 1800s.", "Scores go double digits, like baseball in the eighteen hundreds.", "stat"),
     ("BROKEN FINGERS?", "EVERY GAME.", "", "Broken fingers? Every game.", "hurt")],
    "#baseball #mlb #history #sports")

OUTRO = ("FOLLOW FOR MORE", "WHAT'S NEXT?", "Comment below", "What should we test next? Comment below, and follow for more.", "wave")
