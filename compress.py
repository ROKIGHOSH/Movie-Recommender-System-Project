import pickle
import bz2

# Compress the file
with open("similarity.pkl", "rb") as f:
    data = pickle.load(f)

with bz2.BZ2File("similarity.pkl.bz2", "wb") as f:
    pickle.dump(data, f)
