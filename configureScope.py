import pyvisa
import time

rm = pyvisa.ResourceManager()
visa_string="TCPIP::128.141.143.178::inst0::INSTR"
inst = rm.open_resource(visa_string)

inst.read_termination = '\n'
inst.write_termination = '\n'

#inst.write('*IDN?')
#while True:
#    print(inst.read_bytes(1))

print(inst.query("*IDN?"))


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


"""
#set autonaming
path="C:\Documents and Settings\All Users\Documents\discharges"
description = input("Enter the run description: ")
description = "test"

inst.write("MMEMory:AUTonaming:DEFaultpath "+path)
inst.write("MMEMory:AUTonaming:TEXT "+description)

inst.write("MMEMory:AUTonaming:PREFix OFF")
inst.write("MMEMory:AUTonaming:USERtext ON")
inst.write("MMEMory:AUTonaming:DATE ON")
inst.write("MMEMory:AUTonaming:INDex OFF")
inst.write("MMEMory:AUTonaming:TIME ON")
"""

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
sample_rate=100E6#Sa/s
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


while True:
	print(inst.query("STATus:OPERation:EVENt?"))
	#print(bin(int(inst.query("STATus:OPERation:EVENt?"))).replace("0b", ""),bin(int(inst.query("STATus:OPERation:CONDition?"))).replace("0b", ""))
	#print(inst.query("STATus:OPERation:CONDition?"))
	#time.sleep(1)
	#inst.write("format real,32")


"""
#configure ultra segmentation
waveforms=10
inst.write("ACQuire:SEGMented:STATe ON")
inst.write("ACQuire:SEGMented:MAX OFF")
inst.write("ACQuire:SEGMented:AUToreplay OFF")
inst.write("ACQuire:COUNt "+str(waveforms))


#RUNNING!!!
inst.write("RUNContinous")
time.sleep(1)
print("RUNNING")
while inst.query("ACQuire:AVAilable?")!=str(waveforms):
    #print(inst.query("ACQuire:AVAilable?"))
    time.sleep(1)
print("FINISH!")




#save waveforms
#inst.write("EXPort:WAVeform:NAME 'C:\Temp\test.csv'")


inst.write("EXPort:WAVeform:MULTichannel ON")
inst.write("CHANnel1:EXPortstate ON")
inst.write("CHANnel2:EXPortstate ON")
inst.write("CHANnel3:EXPortstate OFF")
inst.write("CHANnel4:EXPortstate OFF")

inst.write("EXPort:WAVeform:SCOPe WFM")

inst.write("CHANnel1:HISTory ON")
inst.write("CHANnel2:HISTory ON")

inst.write("CHANnel1:HISTory:STARt "+str(-(waveforms-1)))
inst.write("CHANnel1:HISTory:STOP "+str(0))
inst.write("CHANnel2:HISTory:STARt "+str(-(waveforms-1)))
inst.write("CHANnel2:HISTory:STOP "+str(0))

inst.write("EXPort:WAVeform:SAVE")
"""


















#
