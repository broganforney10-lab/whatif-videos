"""Auto-build a 3D story shot list for every video from its narration data.

  python3 gen_story.py            # all public/data/*.json -> public/story/*.json (skips hand-made ones)
  python3 gen_story.py 05-mosquitoes --force

Each narration scene becomes two shots (~2.25 s each). Every shot gets a set, a character
action, a camera move and emoji props picked from the scene's words.
"""
import glob, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
HAND = {"02-bees": "bees"}  # hand-written shot lists in stories/<slug>.py

CATS = {
    "ocean": (["beach", "beach", "town", "store", "beach", "home"],
              "ocean fish whale shark coral seaweed plankton gulf ship cable suez panama nile tides moon"),
    "space": (["night", "meadow", "town", "night", "home", "snow"],
              "sun satellite gps ozone magnetic moon space streetlight cloud wind"),
    "ice": (["snow", "beach", "town", "snow", "home", "night"], "antarctic greenland glacier ice helium"),
    "food": (["meadow", "store", "wheat", "town", "home", "orchard"],
             "bee banana rice wheat corn potato tea coffee cacao sugar salt tomato peanut orange cow chicken grass fungi bamboo fertilizer soil earthworm insect ant spider bird bat frog snake vulture tree amazon"),
    "tech": (["home", "town", "store", "home", "night", "meadow"],
             "internet smartphone email social microchip lithium vending elevator fridge refrigerator air-conditioner traffic cash money"),
    "build": (["town", "home", "store", "meadow", "town", "night"],
              "bridge road car plane train bicycle concrete steel glass aluminum copper sand rubber plastic paper oil gas coal nuclear solar dam power zipper soap gold silver cat dog volcano great-lakes"),
}

EMO = {
    "bee": "🐝", "honey": "🍯", "almond": "🌰", "food": "🍽️", "crop": "🌾", "crops": "🌾", "farm": "🚜", "farmers": "👩‍🌾",
    "price": "💸", "prices": "💸", "money": "💰", "cash": "💵", "dollar": "💵", "bank": "🏦", "billion": "💰",
    "water": "💧", "rain": "🌧️", "river": "🏞️", "rivers": "🏞️", "ocean": "🌊", "sea": "🌊", "flood": "🌊", "floods": "🌊",
    "fish": "🐟", "whale": "🐋", "whales": "🐋", "shark": "🦈", "sharks": "🦈", "coral": "🪸", "seal": "🦭", "otter": "🦦",
    "bird": "🐦", "birds": "🐦", "frog": "🐸", "snake": "🐍", "spider": "🕷️", "ant": "🐜", "ants": "🐜", "bat": "🦇",
    "insect": "🐛", "insects": "🐛", "bugs": "🐛", "mosquito": "🦟", "mosquitoes": "🦟", "worm": "🪱", "worms": "🪱",
    "cow": "🐄", "cows": "🐄", "cattle": "🐄", "chicken": "🐔", "egg": "🥚", "eggs": "🥚", "milk": "🥛", "cheese": "🧀",
    "burger": "🍔", "burgers": "🍔", "steak": "🥩", "meat": "🥩", "bread": "🍞", "pizza": "🍕", "pasta": "🍝", "cake": "🎂",
    "rice": "🍚", "wheat": "🌾", "corn": "🌽", "potato": "🥔", "fries": "🍟", "tea": "🍵", "coffee": "☕", "chocolate": "🍫",
    "sugar": "🍬", "candy": "🍭", "soda": "🥤", "salt": "🧂", "tomato": "🍅", "ketchup": "🍅", "peanut": "🥜", "orange": "🍊",
    "juice": "🧃", "banana": "🍌", "bananas": "🍌", "apple": "🍎", "apples": "🍎", "avocado": "🥑", "avocados": "🥑",
    "tree": "🌳", "trees": "🌳", "forest": "🌲", "forests": "🌲", "flower": "🌸", "wildflowers": "🌼", "grass": "🌱",
    "mushroom": "🍄", "fungus": "🍄", "bamboo": "🎋", "panda": "🐼", "pandas": "🐼", "seaweed": "🌿", "kelp": "🌿",
    "sun": "☀️", "sunlight": "☀️", "moon": "🌕", "moonlight": "🌕", "star": "⭐", "stars": "⭐", "space": "🪐",
    "planet": "🪐", "planets": "🪐", "earth": "🌍", "satellite": "🛰️", "satellites": "🛰️", "rocket": "🚀", "compass": "🧭",
    "cloud": "☁️", "clouds": "☁️", "wind": "💨", "storm": "⛈️", "storms": "⛈️", "snow": "❄️", "ice": "🧊", "cold": "🥶",
    "heat": "🥵", "hot": "🥵", "fire": "🔥", "volcano": "🌋", "volcanoes": "🌋", "dark": "🌑", "darkness": "🌑", "night": "🌙",
    "light": "💡", "lights": "💡", "electricity": "⚡", "power": "⚡", "grid": "⚡", "battery": "🔋", "batteries": "🔋",
    "phone": "📱", "phones": "📱", "internet": "🌐", "email": "📧", "computer": "💻", "laptops": "💻", "chips": "💾",
    "car": "🚗", "cars": "🚗", "truck": "🚚", "trucks": "🚚", "bus": "🚌", "buses": "🚌", "train": "🚆", "trains": "🚆",
    "plane": "✈️", "planes": "✈️", "flights": "✈️", "ship": "🚢", "ships": "🚢", "boat": "⛵", "boats": "⛵", "bike": "🚲",
    "bikes": "🚲", "road": "🛣️", "roads": "🛣️", "bridge": "🌉", "bridges": "🌉", "traffic": "🚦", "map": "🗺️", "maps": "🗺️",
    "house": "🏠", "homes": "🏠", "building": "🏢", "buildings": "🏢", "skyscrapers": "🏙️", "city": "🏙️", "cities": "🏙️",
    "hospital": "🏥", "hospitals": "🏥", "doctor": "🩺", "medicine": "💊", "vaccines": "💉", "infections": "🦠", "surgery": "🩺",
    "oil": "🛢️", "gas": "⛽", "coal": "⚫", "nuclear": "☢️", "solar": "🔆", "factory": "🏭", "factories": "🏭", "steel": "🔩",
    "glass": "🪟", "windows": "🪟", "paper": "📄", "books": "📚", "plastic": "🧴", "clothes": "👕", "jeans": "👖", "shirt": "👕",
    "gold": "🥇", "silver": "🥈", "ring": "💍", "rings": "💍", "jewelry": "💍", "copper": "🔌", "wiring": "🔌",
    "soap": "🧼", "hands": "🙌", "cat": "🐈", "cats": "🐈", "dog": "🐕", "dogs": "🐕", "mice": "🐭", "rats": "🐀",
    "balloons": "🎈", "party": "🎉", "music": "🎵", "school": "🏫", "kids": "🧒", "people": "👥", "jobs": "💼",
    "work": "💼", "store": "🏪", "supermarkets": "🛒", "shelves": "🛒", "shopping": "🛒", "zipper": "🤐", "belt": "👖",
    "tires": "🛞", "sand": "🏖️", "beach": "🏖️", "desert": "🏜️", "island": "🏝️", "islands": "🏝️", "lake": "🏞️",
    "lakes": "🏞️", "tide": "🌊", "tides": "🌊", "time": "⏰", "years": "📅", "decades": "📅", "never": "🚫", "gone": "💨",
}

CAMS = {
    "dolly": dict(**{"from": [0, 1.6, 6.5]}, to=[0, 1.6, 4], look=[0, 1.4, 0]),
    "orbitL": dict(**{"from": [4, 2.2, 4]}, to=[-4, 2.2, 4], look=[0, 1.1, 0]),
    "orbitR": dict(**{"from": [-4, 2.2, 4]}, to=[4, 2.2, 4], look=[0, 1.1, 0]),
    "crane": dict(**{"from": [0, 6, 8.5]}, to=[0, 2.6, 5.5], look=[0, 1, -1]),
    "push": dict(**{"from": [1.2, 1.7, 3.6]}, to=[0.4, 1.7, 2.5], look=[0, 1.6, 0]),
    "pull": dict(**{"from": [0, 1.7, 2.8]}, to=[0, 3.2, 7.5], look=[0, 1.4, 0]),
    "low": dict(**{"from": [-1.8, 0.6, 3.6]}, to=[1.6, 0.8, 3.6], look=[0, 1.6, 0]),
    "walkcam": dict(**{"from": [-0.5, 1.6, 7]}, to=[0, 1.6, 4.6], look=[0, 1.3, 0]),
}
LOOKS = [("straw", "#c8352e"), ("top", "#2f4f8f"), ("cap", "#3f8f4f"), ("top", "#c8352e"), ("cap", "#e07a2e"), ("straw", "#7a3fa0")]


def h(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)


def category(vid):
    slug = vid.split("-", 1)[1]
    for cat, (_, words) in CATS.items():
        if any(w in slug for w in words.split()):
            return cat
    return "build"


def emojis_for(text, topic_emoji, n=3):
    found = []
    for w in re.findall(r"[a-zA-Z\-]+", text.lower()):
        e = EMO.get(w) or EMO.get(w.rstrip("s"))
        if e and e not in found:
            found.append(e)
    if topic_emoji not in found:
        found.append(topic_emoji)
    return found[:n]


def mood_pose(mood):
    return {"shock": "shock", "point": "point", "worried": "sad", "think": "think", "excited": "cheer", "wave": "wave"}[mood]


def spread(es, y=2.5, z=-0.6, anim="grow", s=0.75):
    xs = {1: [1.3], 2: [-1.2, 1.2], 3: [-1.5, 0, 1.5]}[len(es)]
    return [dict(ch=e, pos=[x, y + (0.4 if x == 0 and len(es) == 3 else 0), z], s=s, anim=anim) for e, x in zip(es, xs)]


def build(vid):
    d = json.load(open(f"{HERE}/public/data/{vid}.json"))
    sets = CATS[category(vid)][0]
    hat, coat = LOOKS[h(vid) % len(LOOKS)]
    topic = d["emoji"]
    words = d["words"]
    shots = []
    n = len(d["scenes"])
    for i, sc in enumerate(d["scenes"]):
        t0, t1 = sc["from"] / 30, (sc["from"] + sc["dur"]) / 30
        said = " ".join(w["w"] for w in words if t0 <= w["start"] < t1)
        text = f'{sc["kicker"]} {sc["headline"]} {sc["sub"]} {said}'
        es = emojis_for(text, topic)
        pose = mood_pose(sc["mood"])
        st = sets[i % len(sets)] if i < n - 1 else sets[0]
        seed = h(vid + str(i))
        base = dict(set=st, hat=hat, coat=coat)
        if i == 0:  # hook: walk in among the topic thing, then it vanishes in a puff
            ring = [dict(ch=topic, pos=[1.4, 2.3, -0.4], s=0.7, anim="buzz"), dict(ch=topic, pos=[-1.5, 2.6, -0.8], s=0.6, anim="buzz"),
                    dict(ch=topic, pos=[0.3, 3.0, -1.2], s=0.55, anim="buzz")]
            a = dict(base, pose="walk", walk=[[-1.6, -1.2], [0, 0.8]], cam=CAMS["walkcam"], props=ring)
            b = dict(base, pose="idle", pose2="shock", poseAt=0.4, heading=0.25, cam=CAMS["push"],
                     props=[dict(p, anim="poof", pos=[p["pos"][0] * 0.8, p["pos"][1] - 0.2, 0.3]) for p in ring])
        elif i == n - 1:  # outro: wave
            a = dict(base, pose="wave", cam=CAMS["dolly"], props=[dict(ch="❓", pos=[1.0, 2.6, 0], s=0.55, anim="float")])
            b = dict(base, pose="wave", cam=CAMS["pull"])
        else:
            m1 = ["crane", "orbitL", "orbitR", "dolly", "low"][seed % 5]
            m2 = ["push", "low", "dolly", "push"][(seed // 7) % 4]
            neg = pose in ("sad", "shock")
            walk_first = seed % 3 == 0 and pose != "shock"
            a = dict(base, pose="walk" if walk_first else pose, cam=CAMS["walkcam" if walk_first else m1],
                     props=spread(es, anim="grow"))
            if walk_first:
                a["walk"] = [[1.4, -1.2], [0, 0.6]]
            b = dict(base, pose=pose, heading=[0, 0.3, -0.3][seed % 3], cam=CAMS[m2],
                     props=spread(es[:2], y=2.4, z=0.2, anim="shrink" if neg else "float", s=0.6))
            if pose == "cheer":
                b["held"] = es[0]
            if st == "store":
                a["fill"], b["fill"] = ([1, 0.7], [0.7, 0.3]) if neg else ([1, 1], [1, 1])
            if st == "meadow" and neg:
                a["wilt"], b["wilt"] = [0, 0.6], [0.6, 1]
        h1 = sc["dur"] // 2
        a.update({"from": sc["from"], "dur": h1}); b.update({"from": sc["from"] + h1, "dur": sc["dur"] - h1})
        shots += [a, b]
    return {"id": vid, "durationInFrames": d["durationInFrames"], "audio": d["audio"], "shots": shots,
            "words": d["words"], "mouth": d["mouth"]}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ids = args or sorted(os.path.basename(p)[:-5] for p in glob.glob(f"{HERE}/public/data/*.json"))
    os.makedirs(f"{HERE}/public/story", exist_ok=True)
    for vid in ids:
        if vid in HAND:
            continue
        out = f"{HERE}/public/story/{vid}.json"
        if os.path.exists(out) and "--force" not in sys.argv:
            continue
        json.dump(build(vid), open(out, "w"), ensure_ascii=False, separators=(",", ":"))
    print("stories:", len(glob.glob(f"{HERE}/public/story/*.json")))
