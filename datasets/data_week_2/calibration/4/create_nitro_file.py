import os

def create_nitro_file(metaSource, nitroSource, output, start=8):
    metaLines = None
    with open(metaSource, "r") as f:
        metaLines = f.readlines()
    nitroLines = None
    with open(nitroSource, "r") as f:
        nitroLines = f.readlines()
    nitroLines = nitroLines[start:]
    N = len(nitroLines)
    with open(output, "w") as f:
        for i in range(len(metaLines)):
            if i < start:
                f.write(metaLines[i])
            else:
                metaline = metaLines[i].split(" ")
                nitroline = nitroLines[i%N].split(" ")
                metaline[-1] = nitroline[-1]
                f.write(" ".join(metaline))
    

if __name__ == "__main__":
    create_nitro_file(metaSource=os.getcwd()+"/nitro_after_sky_dip.txt",
                      nitroSource=os.getcwd()+"/dummy_nitro.txt",
                      output=os.getcwd()+"/nitro_after_dip.txt")