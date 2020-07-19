import matplotlib.pyplot as plt 


def draw(f):
    data = f.readlines()
    data = [int(i) for i in data]
    plt.plot(data)
    average = []
    for i in range(len(data[10:-10])):
        average.append(sum(data[i-10:i+10])/20)
    plt.plot(list(range(10, len(data[10:-10])+10)),average)
    plt.show()