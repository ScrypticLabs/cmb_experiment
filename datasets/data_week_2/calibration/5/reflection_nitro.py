import os

def create_nitro_file(ambientSource, nitroSource, output, start=8, R_2=0.00826446):
    ambientLines = None
    with open(ambientSource, "r") as f:
        ambientLines = f.readlines()
    nitroLines = None
    with open(nitroSource, "r") as f:
        nitroLines = f.readlines()
    nitroLines = nitroLines
    N = len(nitroLines)
    with open(output, "w") as f:
        for i in range(len(nitroLines)):
            if i < start:
                f.write(nitroLines[i])
            else:
                ambientline = ambientLines[i].split(" ")
                nitroline = nitroLines[i].split(" ")
                nitroline[-1] = str(float(nitroline[-1].strip()) + R_2*float(ambientline[-1].strip()))+"\n"
                f.write(" ".join(nitroline))
    

if __name__ == "__main__":
    create_nitro_file(ambientSource=os.getcwd()+"/ambient_before_dip.txt",
                      nitroSource=os.getcwd()+"/nitro_before_dip.txt",
                      output=os.getcwd()+"/corrected_nitro_before_dip_2.txt")