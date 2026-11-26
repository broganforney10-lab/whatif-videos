# Shot list for the bees 3D story. Two shots per narration scene (4.5 s -> 2 x 2.25 s).
S = []
def two(a, b): S.extend([a, b])
F = "straw"
two(dict(set="meadow", pose="walk", walk=[[-1.6, -1.2], [0, 1]], cam=dict(**{"from": [-1, 1.6, 7]}, to=[0, 1.5, 5], look=[0, 1.2, 0]),
         props=[dict(ch="🐝", pos=[1.5, 2, 0], s=0.5, anim="buzz"), dict(ch="🐝", pos=[2.5, 2.4, -1], s=0.45, anim="buzz"), dict(ch="🐝", pos=[0.8, 2.6, -0.5], s=0.4, anim="buzz")]),
    dict(set="meadow", pose="idle", pose2="shock", poseAt=0.45, heading=0.3, cam=dict(**{"from": [1.5, 1.7, 4]}, to=[0.6, 1.7, 2.6], look=[0, 1.5, 0]),
         props=[dict(ch="🐝", pos=[1.2, 2.1, 0.3], s=0.5, anim="poof"), dict(ch="🐝", pos=[-1.1, 2.4, 0], s=0.45, anim="poof"), dict(ch="🐝", pos=[0.3, 2.8, -0.4], s=0.4, anim="poof")]))
two(dict(set="meadow", pose="point", heading=0.4, cam=dict(**{"from": [0, 6, 9]}, to=[0, 3.5, 6], look=[0, 0.5, -2]),
         props=[dict(ch="🍎", pos=[-2, 2.5, -2], s=1, anim="grow"), dict(ch="🍓", pos=[0, 3, -2.5], s=1, anim="grow"), dict(ch="🥑", pos=[2, 2.5, -2], s=1, anim="grow")]),
    dict(set="meadow", pose="point", heading=-0.3, cam=dict(**{"from": [3, 1.5, 4]}, to=[1.5, 1.6, 3.5], look=[0, 1.6, 0]),
         props=[dict(ch="🍎", pos=[-1.6, 2.6, -1], s=0.9, anim="float"), dict(ch="☕", pos=[-0.4, 3.1, -1.2], s=0.9, anim="float"), dict(ch="🥑", pos=[0.9, 2.7, -1], s=0.9, anim="float")]))
two(dict(set="orchard", pose="walk", walk=[[0, -1], [0, 2.2]], cam=dict(**{"from": [0, 1.4, 8]}, to=[0, 1.6, 5.5], look=[0, 1.3, 0]), props=[dict(ch="🌸", pos=[1.5, 2.5, 1], s=0.6, anim="float")]),
    dict(set="orchard", pose="idle", pose2="sad", poseAt=0.4, heading=0.6, cam=dict(**{"from": [-3, 2, 4]}, to=[-1.5, 1.8, 3], look=[0, 1.5, 0]),
         props=[dict(ch="🐝", pos=[1.4, 2.2, 0.5], s=0.45, anim="poof")]))
two(dict(set="store", pose="walk", fill=[1, 0.95], walk=[[0, -0.5], [0, 2]], held="🧺", cam=dict(**{"from": [0, 1.7, 7]}, to=[0, 1.7, 5], look=[0, 1.3, -2])),
    dict(set="store", pose="shock", fill=[0.95, 0.4], heading=0.2, held="🧺", cam=dict(**{"from": [-2.5, 2.4, 3.5]}, to=[2.5, 2.4, 3.5], look=[0, 1.2, -1.5])))
two(dict(set="town", pose="idle", pose2="shock", poseAt=0.5, heading=0, cam=dict(**{"from": [0, 2, 6]}, to=[0, 1.8, 3.8], look=[0, 1.5, 0]),
         props=[dict(ch="☕", pos=[-0.8, 1.35, -0.3], s=0.6, anim="shrink"), dict(ch="🍎", pos=[0, 1.35, -0.3], s=0.6, anim="shrink"), dict(ch="🥑", pos=[0.8, 1.35, -0.3], s=0.6, anim="shrink")]),
    dict(set="town", pose="shock", heading=0, cam=dict(**{"from": [1.2, 1.6, 2.8]}, to=[0.5, 1.7, 2.2], look=[0, 1.7, 0]),
         props=[dict(ch="💸", pos=[-0.9, 2.4, 0.3], s=0.55, anim="rise"), dict(ch="📈", pos=[0.9, 2.3, 0.3], s=0.6, anim="rise")]))
two(dict(set="meadow", pose="sad", wilt=[0, 1], heading=0, cam=dict(**{"from": [5, 2.5, 5]}, to=[-5, 2.5, 5], look=[0, 0.8, 0])),
    dict(set="meadow", pose="sad", wilt=[1, 1], heading=0.8, cam=dict(**{"from": [0, 1.2, 3.5]}, to=[0, 1.6, 2.8], look=[0, 1.6, 0]),
         props=[dict(ch="🐦", pos=[-1, 2.5, -1], s=0.6, anim="flyaway"), dict(ch="🐦", pos=[0.5, 2.8, -2], s=0.5, anim="flyaway")]))
two(dict(set="orchard", pose="cheer", heading=0, cam=dict(**{"from": [0, 3, 6]}, to=[0, 1.8, 4], look=[0, 1.5, 0]),
         props=[dict(ch="💰", pos=[1.3, 2.6, 0.4], s=0.6, anim="grow")]),
    dict(set="orchard", pose="point", heading=-0.9, held="🖌️", cam=dict(**{"from": [-2, 1.5, 3]}, to=[-1, 1.8, 2.4], look=[0.6, 1.6, -0.5]),
         props=[dict(ch="🌸", pos=[1.4, 2.3, -0.3], s=0.6, anim="float")]))
two(dict(set="wheat", pose="think", heading=0, cam=dict(**{"from": [0, 1.8, 5]}, to=[0, 1.7, 3.5], look=[0, 1.5, 0]),
         props=[dict(ch="❓", pos=[0.7, 2.5, 0.2], s=0.5, anim="float")]),
    dict(set="wheat", pose="cheer", heading=0, cam=dict(**{"from": [-3, 4, 6]}, to=[3, 3, 6], look=[0, 1, 0]),
         props=[dict(ch="🌾", pos=[-1.5, 2.6, -0.5], s=0.8, anim="grow"), dict(ch="🍚", pos=[0, 3.0, -0.5], s=0.8, anim="grow"), dict(ch="🌽", pos=[1.5, 2.6, -0.5], s=0.8, anim="grow")]))
two(dict(set="meadow", pose="wave", heading=0, cam=dict(**{"from": [0, 1.6, 5]}, to=[0, 1.7, 3.2], look=[0, 1.5, 0]), props=[dict(ch="❓", pos=[0.9, 2.6, 0], s=0.55, anim="float")]),
    dict(set="meadow", pose="wave", heading=0, cam=dict(**{"from": [0, 1.7, 3.2]}, to=[0, 3, 7], look=[0, 1.4, 0])))
for s in S: s.setdefault("hat", F)
