import chardet
rawdata = open('data/investments_VC.csv', 'rb').read(1000)
print(chardet.detect(rawdata))