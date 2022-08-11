import sys
import pyvisa as visa
import pickle
import argparse
import time
import tqdm
import math as m
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RTO 1024 waveform acquistion for CH1+CH2',
                                 epilog='Version: 1.0')
    parser.add_argument('-p','--path',help='path', action='store', default='test')
    parser.add_argument('-n','--name',help='filename', action='store', default='signal')
    parser.add_argument('-e','--events',help='Events to acquire default 1', action='store', default='1')

    args = parser.parse_args()

    try:
        rm = visa.ResourceManager()
        inst = rm.open_resource("TCPIP::128.141.143.178::inst0::INSTR")
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        print(inst.query("*IDN?"))
    except Exception as e:
        print("Error creating instance: {0}".format(e))
        sys.exit()

    f = open("./RunParam.csv", "r")
    print("############################################################")
    print("Input parameters are:")
    #the input parametrs are declared as variebales as they are neamed in the anal_parameters.csv file
    for x in f:
        a=x.split(";",1)
        var=a[0]
        b=a[1].split("\n",1)
        val=float(b[0])
        print("#",var, "=", val)
        exec(var+"="+str(val))
    f.close()
    print("############################################################")

    #configure scale channels
    #scale1=1#V/div
    #scale2=0.1#V/div
    #offset2=0#V
    inst.write("CHANnel1:SCALe "+str(scale1))
    inst.write("CHANnel2:SCALe "+str(scale2))
    inst.write("CHANnel2:OFFSet "+str(offset2))
    #pos1=0#div
    #pos2=0#div
    inst.write("CHANnel1:POSition "+str(pos1))
    inst.write("CHANnel2:POSition "+str(pos2))
    inst.write("CHANnel1:COUPling DC")
    inst.write("CHANnel2:COUPling DCLimit")

    #configre timebase (first the reference then the scale)
    #timescale=100E-6#s/div
    #ref_pos=5#%
    #sample_rate=100E6#Sa/s
    inst.write("TIMebase:REFerence "+str(ref_pos))
    inst.write("TIMebase:SCALe "+str(timescale))
    inst.write("ACQuire:SRATe "+str(sample_rate))

    #configre trigger
    #trigger=-0.3#V
    inst.write("TRIGger1:SOURce CHANNEL1")
    inst.write("TRIGger1:TYPE EDGE")
    inst.write("TRIGger1:EDGE:SLOPe NEG")
    inst.write("TRIGger1:LEVel1 "+str(trigger))
    #inst.write("TRIGger1:MODE AUTO")
    inst.write("TRIGger1:MODE NORM")

    inst.write("RUNContinous")

    if os.path.isdir("./rawWFMs/"+args.path)==True:
        print("=======================================================================================")
        print("You are writing in an existing folder, you have 5 second to CTRL+C if you changed idea")
        time.sleep(5)
    else:
        os.mkdir("./rawWFMs/"+args.path)

    pathname="./rawWFMs/"+args.path+"/"+args.name

    start_time = time.time()
    for i in tqdm.tqdm(range(int(args.events))):
        # grab the waveform
        inst.query("channel1:data:header?")
        inst.write("format real,32")
        wfm1=inst.query_binary_values("channel1:data:values?", datatype='f')
        wfm2=inst.query_binary_values("channel2:data:values?", datatype='f')

        #save
        fsig = open(pathname+"_"+str(i)+".csv","w")
        for w in range(len(wfm1)):
            fsig.write(str(wfm1[w])+";"+str(wfm2[w])+"\n")
        fsig.close()

    finished_time= time.time()
    #save discharge rate during event
    fsig_rate = open(pathname+"_rateHz.csv","w")
    fsig_rate.write("events;"+args.events+"\n")
    fsig_rate.write("time(s);"+str((finished_time-start_time))+"\n")
    fsig_rate.write("rate(Hz);"+str( float(args.events)/(finished_time-start_time) )+"\n")
    fsig_rate.write("error(Hz);"+str(m.sqrt(float(args.events))/(finished_time-start_time)))
    fsig_rate.close()












#
