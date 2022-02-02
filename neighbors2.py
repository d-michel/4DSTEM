l1 = list(sublattice.x_position)
l2 = list(sublattice.y_position)

for i in range(0,N):
    print(i)
    pos[i][0] = l1[i]
    pos[i][1] = l2[i]

for j in range(0,N):
    posp = np.zeros(N)
    print(".", end="", flush=True)
    for k in range(0,N):
        posp[k] = np.sqrt((l1[j] - l1[k])**2 + (l2[j] - l2[k])**2)
        #print(",", end="", flush=True)
    neighbors = sorted(posp)[1:7]
    distances[j] = np.mean(neighbors)

x = l1
y = l2
z = distances

x1 = []
y1 = []
z1 = []

for i in range(0, N-1):
    if x[i] > 20 and x[i] < 260 and y[i] > 20 and y[i] < 260:
        x1.append(x[i])
        y1.append(y[i])
        z1.append(z[i])
        

fig, ax = p.subplots()
sc = ax.scatter(x1, y1, c=z1)
cbar = fig.colorbar(sc)
p.show()
