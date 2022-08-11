import sys
import pyvisa as visa
import pickle
import argparse
import numpy as np
import matplotlib.pyplot as plt

VERSION = 0.2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RTO remote waveform demo utility',
                                 epilog='Version: ' + str(VERSION))
    parser.add_argument('-b','--binary',help='save binary file of floats as a pickle',action='store_true')
    parser.add_argument('-c','--channel',help='scope channel to use',action='store', default='1', type=int, choices=range(1, 5))
    parser.add_argument('-n','--name',help='filename', action='store', default='signal')
    parser.add_argument('-t','--text',help='save text file of floats',action='store_true')
    parser.add_argument('-p','--plot',help='plot captured waveform',action='store_true')
    parser.add_argument('-f','--plotfft',help='plot captured waveform as FFT',action='store_true')
    parser.add_argument('-s','--sampling',help='sampling frequency, default is 1 M', action='store', default='1000000')


    args = parser.parse_args()
    ch = 'channel'+str(args.channel)

    try:
        rm = visa.ResourceManager()
        inst = rm.open_resource("TCPIP::128.141.143.178::inst0::INSTR")
        print(inst.query("*IDN?"))
    except Exception as e:
        print("Error creating instance: {0}".format(e))
        sys.exit()

    # grab the waveform
    try:
        inst.query(ch + ":data:header?")
        inst.write("format real,32")
        values=inst.query_binary_values(ch + ":data:values?", datatype='f')
    except Exception as e:
        print("Error retrieving the waveform: {0}".format(e))
        print("Did you specify the right channel?")
        sys.exit()

    # do something with the waveform
    if args.plot:
        plt.plot(values)
        plt.show()

    if args.text:
        fsig = open(args.name+".txt","w")
        for value in values:
            fsig.write("%s\n" % value)
        fsig.close()

    if args.binary:
        fsig = open(args.name+".pickle","wb")
        pickle.dump(values,fsig,pickle.HIGHEST_PROTOCOL)
        fsig.close()

    if args.plotfft:
        Fs = float(args.sampling)       # sampling frequency
        n=len(values)                   # number of samples
        Ts=1/Fs                         # sampling period
        s=np.fft.rfft(values)           # computer fft for real input.  s is the complex transform array
        fs=np.fft.rfftfreq(n,Ts)        # return the frequencies
        plt.plot(fs,np.absolute(s))
        plt.show()

    inst.close()
    print("finished")
