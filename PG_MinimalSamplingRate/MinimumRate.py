'''
File: MinimumRate.py
Author: James Jolly
Date Created: May 9, 2024
Purpose: Read in a data file from MealWatcher and output a sequence of the data rate for each segment of a file
Synchronizes time, then looks at the number of data points within a segment to calculate average sampling rate.

NOTE: This is not the actual sampling rate for a missing chunk of data, 
	but does provide an idea of sampling rate when dropping at a constant rate.  
'''
##########################
####### Import Libraries
##########################
import numpy as np
import struct # used for unpacking binary
import time
import datetime
# import datetime.fromtimestamp as Epoch2Datetime
import matplotlib.pyplot as plt

print("Finished Importing Libraries.")



##########################
####### Read File Data
##########################

# Import Binary File to Arrays

# fileName = 'DataFiles/10006-2024-05-01-18-17-48-ring.data'
fileName = 'DataFiles/10012-2024-05-08-13-20-22-ring.data'


# Flag used for whether the System time is overwriting some of the pose data or not
SYSTIME_DEBUG_FLAG = True

#DEFAULT ALL VALUES TO TRUE AND PLAN TO PARSE
READ_GYRO_FLAG = True
READ_RAWACC_FLAG = True
READ_MAGNET_FLAG = True
READ_SYSTIME_FLAG = True
READ_POSE_FLAG = True
READ_POSE_FLAG = True
READ_LINACC_FLAG = True
READ_TIMESTAMP_FLAG = True

# TURN OFF WITH COMMENTS ANY YOU WISH TO KEEP
# READ_GYRO_FLAG = False
# READ_RAWACC_FLAG = False
READ_MAGNET_FLAG = False
# READ_SYSTIME_FLAG = False
# READ_POSE_FLAG = False
READ_LINACC_FLAG = False
# READ_TIMESTAMP_FLAG = False

#Initialize all arrays to empty lists
Gyro_Data = []
RawAcc_Data = []
Magnet_Data = []
Pose_Data = []
SysTime_Data = []
LinAcc_Data = []
Timestamp_Data = []

FilePtr = open(fileName,"rb")
BITES_PER_LINE = 80
cntr = 0
# for line in FilePtr: # Doesn't work since there are no newline chars in file
line = FilePtr.read(BITES_PER_LINE) #read first 60 bytes
while (line != b''):
	cntr+=1
	lineIdx = 0 # set the line index to the start

	# Read Gryoscopes 
	if (READ_GYRO_FLAG == True):
		lineIdx = 0 # Start of GyroData
		currData = []
		for i in range(3):
			currData.append(struct.unpack('<f',line[lineIdx:lineIdx+4])[0])
			lineIdx+=4 # Move index now that float was read
		#end of Gryo loop
		Gyro_Data.append(currData)
	#end of ReadGyro

	# Read Raw acceleration 
	if (READ_RAWACC_FLAG == True):
		lineIdx = 12 # Start of GyroData
		currData = []
		for i in range(3):
			currData.append(struct.unpack('<f',line[lineIdx:lineIdx+4])[0])
			lineIdx+=4 # Move index now that float was read
		#end of Gryo loop
		RawAcc_Data.append(currData)
	#end of ReadGyro

	# Read Magnetometers 
	if (READ_MAGNET_FLAG == True):
		lineIdx = 24 # Start of GyroData
		currData = []
		for i in range(3):
			currData.append(struct.unpack('<f',line[lineIdx:lineIdx+4])[0])
			lineIdx+=4 # Move index now that float was read
		#end of Gryo loop
		Magnet_Data.append(currData)
	#end of ReadGyro

	if (READ_POSE_FLAG == True):
		lineIdx = 36 # Start of GyroData
		currData = []
		for i in range(4):
			currData.append(struct.unpack('<f',line[lineIdx:lineIdx+4])[0])
			lineIdx+=4 # Move index now that float was read
		#end of Gryo loop
		Pose_Data.append(currData)
	#end of ReadGyro

	# Read Linear Acceleration 
	if (READ_LINACC_FLAG == True):
		lineIdx = 52 # Start of GyroData
		currData = []
		for i in range(3):
			currData.append(struct.unpack('<f',line[lineIdx:lineIdx+4])[0])
			lineIdx+=4 # Move index now that float was read
		#end of Gryo loop
		LinAcc_Data.append(currData)
	#end of ReadGyro
	
	# Read Ring Timestamp 
	if (READ_TIMESTAMP_FLAG == True):
		lineIdx = 64 # Start of GyroData
		currData = []
		# currData.append(struct.unpack('<Q',line[lineIdx:lineIdx+8]))
		# lineIdx+=8 # Move index now that float was read
		# Timestamp_Data.append(currData[:])
		Timestamp_Data.append(struct.unpack('<Q',line[lineIdx:lineIdx+8])[0])
		# currTimestamp = np.double(struct.unpack('<Q',line[lineIdx:lineIdx+8])[0])
		# if cntr % 5000 == 0:
			# print(currTimestamp)
		# print("{:f}".format(struct.unpack('<d',line[lineIdx:lineIdx+8])[0]))
	#end of ReadGyro
	
	# Read Systime
	if (READ_SYSTIME_FLAG == True):
		lineIdx = 72 # Start of GyroData
		SysTime_Data.append(struct.unpack('<Q',line[lineIdx:lineIdx+8])[0])
	# end of if sys_time_debug is True
	
	# UPDATE THE LINE LOOP VARIABLE
	line = FilePtr.read(BITES_PER_LINE)
	
	if (cntr > 1 and cntr % 10000 == 0):
		print("Through {:d} lines of file...".format(cntr))
		# print("Next Line is {:d} bytes long.".format(len(line)))
	# end of progress print
# end of For Line
print("Total Lines = {:d}".format(cntr))


FilePtr.close()

#Convert all arrays to NumPy
Gyro_Data = np.array(Gyro_Data)
RawAcc_Data = np.array(RawAcc_Data)
Magnet_Data = np.array(Magnet_Data)
SysTime_Data = np.array(SysTime_Data)
Pose_Data = np.array(Pose_Data)
LinAcc_Data = np.array(LinAcc_Data)
Timestamp_Data = np.array(Timestamp_Data)


print("Finished Reading Data File into Arrays.")


##########################
####### Convert Time to Zero-based
##########################

# Some quick checks for data, and converting Time into some meaningful data (zero-based times)

# print((Timestamp_Data[1]/1000))
# print((SysTime_Data[1]/1000))
secRawTimestamps = Timestamp_Data/1000
secSysTimestamps = SysTime_Data/1000
print("Sensor Start and End Timestamps (with Drift):")
print(datetime.datetime.fromtimestamp(secRawTimestamps[7]))
print(datetime.datetime.fromtimestamp(secRawTimestamps[-7]))
print("")

print("Ssystem Start and End Timestamps (with Drift):")
print(datetime.datetime.fromtimestamp(secSysTimestamps[7]))
print(datetime.datetime.fromtimestamp(secSysTimestamps[-7]))
print("")

zero_time_sec = secRawTimestamps - secRawTimestamps[0]
zero_systime_sec = secSysTimestamps - secSysTimestamps[0]
#Calculate difference (Ring - sys)
TimeDiff_sec = zero_time_sec - zero_systime_sec





##########################
####### Adjust for Clock Drift the time
##########################
SamplingSize = 100
averageStart_Time = sum(zero_time_sec[0:SamplingSize])
averageStart_SysTime = sum(zero_time_sec[0:SamplingSize])
averageEnd_Time = sum(zero_time_sec[-SamplingSize:-1])
averageEnd_SysTime = sum(zero_time_sec[-SamplingSize:-1])

TimeDilationFactor =  (averageEnd_SysTime - averageStart_SysTime) / (averageEnd_Time - averageStart_Time)

timestamps_sec = zero_time_sec * TimeDilationFactor

print("Successfully Dilated Sensor times to account for ring drift...\n")

##########################
####### Adjust for Clock Drift the time
##########################

ChunkRates = [] # calculate data in 5 second chunks

currChunkStartIdx = 0; # start idx of current chunk
ExpChunkSize = 500;
NextJump = int(ExpChunkSize/2) # binary search

for i in range(0,int(np.floor(timestamps_sec[-1]/5))):
	RoverIdx = currChunkStartIdx + ExpChunkSize
	
	if RoverIdx > len(timestamps_sec):
		break
	# end of error bound check
	while ((timestamps_sec[RoverIdx] < i*5) or (timestamps_sec[RoverIdx-1] > i*5)): #Only break on stradling the time boundary
		if (timestamps_sec[RoverIdx] < i*5): # if rover is too early
			RoverIdx += NextJump
		else:
			RoverIdx -= NextJump
		# end if rover early
		NextJump = max(1,int(np.floor(NextJump/2))) # Shrink binary step
	#end while
	
	ChunkRates.append(((RoverIdx-1)-currChunkStartIdx)/5) #add the number of samples for the 5 sec chunk to list
	
	# Move Chunk Forward
	currChunkStartIdx = RoverIdx
	NextJump = 250
	
	if (i % 10 == 0):
		print("Through chunk {:d} of {:d}...".format(i,int(np.floor(timestamps_sec[-1]/5))))
	# end of progress print
# end of for i in range



for i in range(0,len(ChunkRates),5):
	print("Chunk {}: {} Hz".format(i,ChunkRates[i]))
# end of for i = 0...len(ChunkRates)





