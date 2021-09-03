from cryptography.fernet import Fernet
import json
import os
import sys


class CryptoInfo:

    def __init__(self, buyInfo, isInital = False):
        self.buyInfo = buyInfo
        if isInital != True:
            print("[CryptoInfo] Loading Key...")
            k = self.LoadKey()
            if k != None:
                print("[CryptoInfo] Key Loaded")
                self.cipher_suite = Fernet(k.encode())
            else:
                print("[CryptoInfo] Key Could not be loaded. \n You might need to encrypt your info.json first, or add in key in en.json.")
                sys.exit()

    def Inital_Encrypt(self):
        k = Fernet.generate_key()
        k = k.decode()
        self.cipher_suite = Fernet(k)
        print("[CryptoInfo] Key Created")
        self.WriteKey(k)
        return self.encrypt()


    def encrypt(self):
        print("[CryptoInfo] Encrypting Info....")
        for key, value in self.buyInfo.items():
            self.buyInfo[key] = str(self.cipher_suite.encrypt(value.encode()))[2:-1]
            # print("{}:{}".format(key, self.buyInfo[key]))
        # for key, value in self.buyInfo.items():
        #     print("{}:{}".format(key, value))

        return self.buyInfo


    def decrypt(self):
        print("[CryptoInfo] Decrypting Info....")
        for key, value in self.buyInfo.items():
            self.buyInfo[key]  = str(self.cipher_suite.decrypt(value.encode()))[2:-1]
        # for key, value in self.buyInfo.items():
        #     print("{}:{}".format(key, value))
        print("[CryptoInfo] Decrypting Done")
        return self.buyInfo

    def WriteKey(self, key):
        with open('en.json', 'w') as outfile:
            json.dump(key, outfile)
        print("[CryptoInfo] en.json Saved")

    def LoadKey(self):
        if os.path.isfile("en.json"):
            with open('en.json') as json_data:
                k = json.load(json_data)
            print("[CryptoInfo] en.json Loaded")
        else:
            k = None
            self.WriteKey(None)
            print("[CryptoInfo] Please Enter key in en.json, or encrypt \n Exiting....")
            sys.exit()

        return k
