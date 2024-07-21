#%%
def calculate_offset(ssb_freq = -0.1, offsetToPointA = -1, pointAFreq = -0.1, k_ssb = -1, frequencyDomainResources = 6, sc=0.015):
    # Use only MHz for frquency variables.
    # ssb_freq: ssb center frequency
    # pointAFreq: 'absoluteFrequencyPointA' in RRC setup
    # offsetToPointA: 'offsetToPoint' in RRC setup
    # k_ssb: 'ssb-SubcarrierOffset' in RRC setup 
    # frequencyDomainResources: number of 1s specified at 'frequencyDomainResources' in RRC setup
    # sc: subcarrierSpacing
    if pointAFreq > 0 and offsetToPointA > 0:
        print("************Both absoluteFrequencyPointA and offsetToPointA are given. This might be wrong configuration.")
        return -1
    elif pointAFreq > 0:
        # Calculate PDCCH BW and PDCCH center frqeuncy
        PDCCH_bw = frequencyDomainResources * 6 * 12 * sc
        PDCCH_center = pointAFreq + (PDCCH_bw/2)
        # print(PDCCH_center)
        # Get offset between PDCCH and ssb and return
        return round((ssb_freq-PDCCH_center)/sc)
    else:
        # Calculate pointA frequency
        pointA = ssb_freq - (240*sc/2) - (k_ssb*sc) - (offsetToPointA*12*sc)
        # Calculate PDCCH BW and PDCCH center frqeuncy
        PDCCH_bw = frequencyDomainResources * 6 * 12 * sc
        PDCCH_center = pointA + (PDCCH_bw/2)
        # Get offset between PDCCH and ssb and return
        return round((ssb_freq-PDCCH_center)/sc, 2)
        
#%%
# with absolutePointAFrequency
calculate_offset(ssb_freq=626.45,\
                pointAFreq = 622.46,\
                frequencyDomainResources=16,\
                sc=0.015)
#%%
calculate_offset(ssb_freq=1939.25,\
                offsetToPointA = 38,\
                k_ssb= 10,\
                frequencyDomainResources=16,\
                sc=0.015)
# %%
calculate_offset(ssb_freq=	626.45,\
                pointAFreq = 622.46,\
                frequencyDomainResources=16,\
                sc=0.015)
# %%
310/0.015
# %%
