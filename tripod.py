from epics import caget,caput
import time
import math

P = "DMC_KB:"
DELAY = 0.01 	#Necessary delay to perform multi-caput commands

#Stop IOC motion on 
	# real axes A,B,C
	# virtual axes I,J,K (Y, Rx, Rz)
caput (P+"A.SPMG","Stop")
caput (P+"B.SPMG","Stop")
caput (P+"C.SPMG","Stop")
caput (P+"I.SPMG","Stop")
caput (P+"J.SPMG","Stop")
caput (P+"K.SPMG","Stop")


#Setup motors. 
	#VELOCITY
	#ACCEL
	#DCEL
	#Proportional gain
VELOCITY = 30000
ACCEL = 133120
DCEL = 133120
KP_A = 2.2
KP_B = 2.2
KP_C = 2.2

'''caput (P+"SEND_STR_CMD","vmax_a = "+ str(VELOCITY))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","vmax_b = "+ str(VELOCITY))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","vmax_c = "+ str(VELOCITY))
time.sleep(DELAY)'''


caput (P+"SEND_STR_CMD","ACA = "+ str(ACCEL))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","ACB = "+ str(ACCEL))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","ACC = "+ str(ACCEL))
time.sleep(DELAY)

caput (P+"SEND_STR_CMD","DCA = "+ str(DCEL))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","DCB = "+ str(DCEL))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","DCC = "+ str(DCEL))
time.sleep(DELAY)

caput (P+"SEND_STR_CMD","kp_a = "+ str(KP_A))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","kp_b = "+ str(KP_B))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","kp_c = "+ str(KP_C))
time.sleep(DELAY)

# Ask inputs
	#Y - Vertical Translation
	#Rx - Pitch
	#Rz - Roll
Y = input("Set Y pos [um]:")
Rx = input("Set Rx pos [urad]:")
Rz = input("Set Rz pos [urad]:")

# Calculate outputs in um
	#sp_a - set point for real axis A
	#sp_b - set point for real axis B
	#sp_c - set point for real axis C
sp_a = Y + 0.1235*Rx
sp_b = Y + 0.133*Rz - 0.1235*Rx
sp_c = Y - 0.133*Rz - 0.1235*Rx

print "sp_a:",sp_a," um"
print "sp_b:",sp_b," um"
print "sp_c",sp_c," um"

# Move motors
	# 1. Disable closed-loop control flag:  cl_on = 0
	# 2. Calculate velocities to motion A,B,C ends at same time
	# 3. Calculate set points to Galil. (sp_galil = sp_axis / encoder_res)
	# 4. Enable closed-loop control flag : cl_on = 1 to start the motion at 'same' time
	# Note: Galil performance closed-loop: 2x3 ms
caput (P+"SEND_STR_CMD","cl_on = 0")
time.sleep(DELAY)
higher_sp = max(sp_a,sp_b,sp_c)
vel_a_factor = math.fabs(sp_a/higher_sp)
vel_b_factor = math.fabs(sp_b/higher_sp)
vel_c_factor = math.fabs(sp_c/higher_sp)

vmax_a = vel_a_factor*VELOCITY
vmax_b = vel_b_factor*VELOCITY
vmax_c = vel_c_factor*VELOCITY

print "vel_a_max:", vmax_a
print "vel_b_max:", vmax_b
print "vel_c_max:", vmax_c

caput (P+"SEND_STR_CMD","vmax_a = "+ str(vmax_a))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","vmax_b = "+ str(vmax_b))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","vmax_c = "+ str(vmax_c))
time.sleep(DELAY)

sp_a_galil = sp_a*20
sp_b_galil = sp_b*20
sp_c_galil = sp_c*20

caput (P+"SEND_STR_CMD","sp_a = "+ str(sp_a_galil))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","sp_b = "+ str(sp_b_galil))
time.sleep(DELAY)
caput (P+"SEND_STR_CMD","sp_c = "+ str(sp_c_galil))
time.sleep(DELAY) 

caput (P+"SEND_STR_CMD","cl_on = 1")
time.sleep(DELAY)
