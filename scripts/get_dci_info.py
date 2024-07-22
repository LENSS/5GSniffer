#%%
TimeDomainAllocationList = {0:13, 1:12, 2: 11, 3:12, 4: 11, 5: 10, 6:11, 7:10, 8:9}
mcs_table = {
    'MCS Index': {
        0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 
        12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 20: 20, 21: 21, 
        22: 22, 23: 23, 24: 24, 25: 25, 26: 26, 27: 27, 28: 28, 29: 29, 30: 30, 31: 31
    },
    'Modulation Order (Qm)': {
        0: 2, 1: 2, 2: 2, 3: 2, 4: 2, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 11: 6, 
        12: 6, 13: 6, 14: 6, 15: 6, 16: 6, 17: 6, 18: 6, 19: 6, 20: 8, 21: 8, 22: 8, 
        23: 8, 24: 8, 25: 8, 26: 8, 27: 8, 28: 2, 29: 4, 30: 6, 31: 8
    },
    'Target Code Rate (R x [1024])': {
        0: 120, 1: 193, 2: 308, 3: 449, 4: 602, 5: 378, 6: 434, 7: 490, 8: 553, 9: 616, 
        10: 658, 11: 466, 12: 517, 13: 567, 14: 616, 15: 666, 16: 719, 17: 772, 18: 822, 
        19: 873, 20: 682.5, 21: 711, 22: 754, 23: 797, 24: 841, 25: 885, 26: 916.5, 
        27: 948
    },
    'Spectral Efficiency': {
        0: 0.2344, 1: 0.377, 2: 0.6016, 3: 0.877, 4: 1.1758, 5: 1.4766, 6: 1.6953, 
        7: 1.9141, 8: 2.1602, 9: 2.4063, 10: 2.5703, 11: 2.7305, 12: 3.0293, 13: 3.3223, 
        14: 3.6094, 15: 3.9023, 16: 4.2129, 17: 4.5234, 18: 4.8164, 19: 5.1152, 20: 5.332, 
        21: 5.5547, 22: 5.8906, 23: 6.2266, 24: 6.5703, 25: 6.9141, 26: 7.1602, 27: 7.4063
    },
    'Effective Bits per RB': {
        0: 39.375, 1: 63.328125, 2: 101.0625, 3: 147.328125, 4: 197.53125, 5: 248.0625, 
        6: 284.8125, 7: 321.5625, 8: 362.90625, 9: 404.25, 10: 431.8125, 11: 458.71875, 
        12: 508.921875, 13: 558.140625, 14: 606.375, 15: 655.59375, 16: 707.765625, 
        17: 759.9375, 18: 809.15625, 19: 859.359375, 20: 895.78125, 21: 933.1875, 
        22: 989.625, 23: 1046.0625, 24: 1103.8125, 25: 1161.5625, 26: 1202.90625, 
        27: 1244.25}
}

def allocated_bits_in_DCI_1_1(raw_dci):
    freq_res = raw_dci[2:20]
    time_res = raw_dci[20:24]
    mcs_scheme = raw_dci[24:29]

    # Count the allocated RBs on frequency domain
    RBs = 0
    for b in freq_res:
        if b == "1":
            RBs += 8
    # Multiply the # of RBs to the allocated time domain
    try: 
        RBs = RBs * TimeDomainAllocationList[int(time_res,2)]
    except:
        print(f"Wrong value for TimeDomainAllocationList. There are 8 entries but got {int(time_res,2)}.")
        return -1
    # Apply MCS table
    try:
        allocated_bits = RBs * mcs_table['Effective Bits per RB'][int(mcs_scheme,2)]
    except:
        print(f"Wrong value for MCS index. There are 27 entries but got {int(mcs_scheme,2)}.")
        return -1

    return allocated_bits


#%%
# if __name__=="__main__": 
dci_info = {"size":[], "time":[], "rawDCI":[], "corr":[], "entry_cnt":0}
with open('../collected_data/output_2.txt', 'r') as file:
    for line in file:
        if "Found DCI" in line:
            dci_info['size'].append(int(line.split(',')[2][-2:])) # DCI size
            dci_info['time'].append(float(line.split(',')[3][8:])) # Time stamp
            dci_info['rawDCI'].append(line.split(',')[-2].split(' ')[-1]) # Raw DCI    
            dci_info['corr'].append(line.split(',')[-1].split(" ")[-1][:-1]) # Correlation 
            dci_info['entry_cnt'] += 1

downlink = {"time":[], "allocated_bits":[]}
uplink = {}

for i in range(dci_info['entry_cnt']):
    if dci_info['size'][i] == 49 :
        allocated_bits = allocated_bits_in_DCI_1_1(dci_info["rawDCI"][i])
        if allocated_bits != -1:
            downlink["time"].append(dci_info["time"][i])
            downlink["allocated_bits"].append(allocated_bits)
#%%
import pandas as pd
import matplotlib.pyplot as plt
downlink_df = pd.DataFrame(downlink)
downlink_df['aggregated_bits'] = downlink_df['allocated_bits'].cumsum()
downlink_df['aggregated_bytes'] = downlink_df['aggregated_bits'] / 8

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(downlink_df['time'].to_numpy(), downlink_df['aggregated_bytes'].to_numpy(), label='Aggregated Bytes')
plt.xlabel('Time (seconds)')
plt.ylabel('Aggregated Bytes Allocated by DCI 1_1')
#plt.title('Aggregated  Over Time')
plt.legend()
plt.grid(True)
plt.show()
#%%
#%%
"""
1110010010000000000001100100000000010000000010000
  100100100000000000
                    0110

DCI format identifier: 1 bit
Frequency domain resource: 8 bits -> type0 and configuration 1
Time domain resource: 4 bits
          pdsch-TimeDomainAllocationList -> setup
           [0]
            mappingType : typeA
            startSymbolAndLength : 40 -> start: 1, length: 13
           [1]
            mappingType : typeA
            startSymbolAndLength : 53 -> start: 2, length: 12 
           [2]
            mappingType : typeA
            startSymbolAndLength : 66 -> start: 3, length: 11
           [3]
            mappingType : typeA
            startSymbolAndLength : 54 -> start: 1, length: 12
           [4]
            mappingType : typeA
            startSymbolAndLength : 67 -> start: 2, length: 11
           [5]
            mappingType : typeA
            startSymbolAndLength : 80 -> start: 3, length: 10
           [6]
            mappingType : typeA
            startSymbolAndLength : 68 -> start: 1, length: 11
           [7]
            mappingType : typeA
            startSymbolAndLength : 81 -> start: 2, length: 10
           [8]
            mappingType : typeA
            startSymbolAndLength : 94 -> start: 3, length: 9
MCS: 5 bits
    Related parameters: "mcs-Table: 256qam", following Table 5.1.3.1-2
"""
# import pandas as pd
# # Define the MCS table
# mcs_table = { # 38.214 v15.10 - Table 5.1.3.1-2
#     "MCS Index": list(range(32)),
#     "Modulation Order (Qm)": [2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 2, 4, 6, 8],
#     "Target Code Rate (R x [1024])": [120, 193, 308, 449, 602, 378, 434, 490, 553, 616, 658, 466, 517, 567, 616, 666, 719, 772, 822, 873, 682.5, 711, 754, 797, 841, 885, 916.5, 948, 'reserved', 'reserved', 'reserved', 'reserved'],
#     "Spectral Efficiency": [0.2344, 0.3770, 0.6016, 0.8770, 1.1758, 1.4766, 1.6953, 1.9141, 2.1602, 2.4063, 2.5703, 2.7305, 3.0293, 3.3223, 3.6094, 3.9023, 4.2129, 4.5234, 4.8164, 5.1152, 5.3320, 5.5547, 5.8906, 6.2266, 6.5703, 6.9141, 7.1602, 7.4063, 'reserved', 'reserved', 'reserved', 'reserved']
# }
# mcs_df = pd.DataFrame(mcs_table) # Convert the dictionary to a pandas DataFrame
# num_subcarriers = 12 # define constants
# effective_symbols = 14 # Assume we can use all OFDM symbols.
# def calculate_effective_bits_per_rb(row): # Calculate effective bits per RB for each MCS index
#     if row["Target Code Rate (R x [1024])"] == 'reserved':
#         return 'reserved'
#     Qm = row["Modulation Order (Qm)"]
#     R = row["Target Code Rate (R x [1024])"] / 1024
#     raw_bits = num_subcarriers * effective_symbols * Qm
#     effective_bits = raw_bits * R
#     return effective_bits
# mcs_df["Effective Bits per RB"] = mcs_df.apply(calculate_effective_bits_per_rb, axis=1)
