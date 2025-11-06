import igraph

g = igraph.Graph.Read_Ncol('net.txt', names=True, weights=True)

for v in g.vs:
    v['size'] = 40
    v['label'] = v['name']

    if v['name'][0] == 'I':
        v['color'] = 'lightblue'
    elif v['name'][0] == 'O':
        v['color'] = 'lightpink'
    else:
        v['color'] = 'lightgrey'


for e in g.es:
    if e['weight'] < 0:
        e['color'] = 'lightcoral'
    elif e['weight'] == 0:
        e['color'] = 'grey'
    else:
        e['color'] = 'green'

    width = abs(e['weight'])
    e['width'] = 1 + 1.25 * (width / 8192.0)


if len(g.vs) < 12:
    bbox = (400, 400)
    layout = 'fruchterman_reingold'
elif len(g.vs) < 18:
    bbox = (500, 500)
    layout = 'fruchterman_reingold'
elif len(g.vs) < 24:
    bbox = (800, 800)
    layout = 'fruchterman_reingold'
elif len(g.vs) < 26:
    bbox = (800, 800)
    layout = 'fruchterman_reingold'
elif len(g.vs) < 50:
    bbox = (1000, 1000)
    layout = 'fruchterman_reingold'
elif len(g.vs) < 130:
    bbox = (1200, 1000)
    layout = 'fruchterman_reingold'
elif len(g.vs) < 150:
    bbox = (4000, 4000)
    layout = 'fruchterman_reingold'
    for v in g.vs:
        v['size'] *= 1.5
elif len(g.vs) < 200:
    bbox = (4000, 4000)
    layout = 'kamada_kawai'
    for v in g.vs:
        v['size'] *= 2
else:
    bbox = (8000, 8000)
    layout = 'fruchterman_reingold'


igraph.plot(g, "net.svg", edge_curved=True, bbox=bbox, margin=64, layout=layout)