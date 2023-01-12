#Import class "Strenc"
from strenc import Strenc

strEnc = Strenc(seed="923072371273@2") #Use this format for seed : [seed@chunk-length]

encoded = strEnc.encode("Test text" , folds=10) # This line will encode the given string 10 times

print(repr(encoded)) # Print encoded string

decoded = strEnc.decode(encoded , True , folds=10) # This line will decode the encoded string. Value of "folds" should be same as encode

print(decoded)

 