import matplotlib.pyplot as plt 


def draw(f):
    data = f.readlines()
    data = [int(i) for i in data]
    plt.plot(data)
    average = []
    for i in range(len(data[5:-5])):
        average.append(sum(data[i-5:i+5])/10)
    plt.plot(list(range(5, len(data[5:-5])+5)),average)
    plt.show()