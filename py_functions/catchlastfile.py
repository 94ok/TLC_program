import os

def catchlastfile(path) : 
    fname_and_timelst = []
    for files in os.listdir(f"{path}") :
        written_time = os.path.getctime(f"{path}{files}")
        fname_and_timelst.append((files,written_time))
    fname_and_timelst = sorted(fname_and_timelst, key=lambda x: x[1], reverse=True)
    try:
        fname=fname_and_timelst[0][0]
    except:
        fname=None
    return fname