import matplotlib.pyplot as plt
with open('data.txt') as f:
    values = list(f.readlines())
for i in values:
    i = float(i[:-2])
x1 = 0.0102955
xs = [ x1*n for n in range(len(values))]
plt.plot(xs, values)
plt.xlabel('t, с')
plt.ylabel('U, В')
plt.show()