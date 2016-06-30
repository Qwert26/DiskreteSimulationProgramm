import matplotlib.pyplot as plot;
def main():
    points={};
    points[0]=0;
    points[3]=9;
    points[2]=4;
    points[1]=1;
    plot.plot(points);
    plot.xlabel("x");
    plot.ylabel("y");
    plot.show();
    return;
if __name__ == "__main__":
    main();