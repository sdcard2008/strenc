#keys.json generated using "strenc -genpath ./ -type random" and chunk length 4.
#Import class "Strenc"

from strenc import Strenc

strEnc = Strenc(key_path="./") #Load the file (key_path should be the path before keys.json)

encoded = strEnc.encode("Test text" , folds=10) # Encode 10 times

print(repr(encoded))

decoded = strEnc.decode(encoded , True , folds=10) # Decoding

print(decoded)

