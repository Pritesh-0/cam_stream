import cv2
import numpy as np
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

elements={
        'Orthorhombic sulphur':[265,285],
        'Polymeric sulphur':[360],
        'Sulphur Dioxide':[280],
        'Iron-sulphur clusters':[450,620],
        'Phosphate':[370,436,690,827],
        'Nitrate':[203,302],
        'Manganese':[336,358,401,436,530],
        'Zinc':[302,455],
        'Citric Acid':[200],
        'Butyric Acid':[206],
        'Iron Oxide Nanoparticles':[295],
        'Fe203 NP':[320,420],
        'Al203':[491,562,650],
        'Silica NP':[206]
        }

def check(elements,peaks,thresh):
    for element, ref_peaks in elements.items():
        diff = all(abs(peak-ref_peak) <=thresh for peak, ref_peak in zip(peaks,ref_peaks))
        print(element,' : ',diff)
        if diff:
            print(element)

def graph(simg):


    image = cv2.imread(simg, cv2.IMREAD_GRAYSCALE)

    pixel_positions = np.arange(0, image.shape[1])
    #print(pixel_positions)

    calibration_factor=2.9
    wavelengths = pixel_positions * calibration_factor

    # Extract the spectrum
    spectrum = np.sum(image, axis=0)  # Sum along columns
    #print(len(spectrum),len(pixel_positions))

    peaks=find_peaks(spectrum,height=10,threshold=5,distance=5)
    print(wavelengths[peaks[0]])

    
    plt.style.use('Solarize_Light2')
    fig=plt.figure(figsize=(10, 5))
    plt.plot(wavelengths, spectrum, color='b', linewidth=2)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.title('Wavelength Spectrum')
    plt.grid(True)
    plt.show()
    #plt.draw()
    #plt.waitforbuttonpress(0)
    #input()
    #plt.close(fig)

    check(elements,wavelengths[peaks[0]],10)

    fig,ax=plt.subplots(4,4)
    r,c=0,0
    for i in elements:
        #ax[r,c].figure(figsize=(10, 5))
        mini,maxi=elements[i][0]-50,elements[i][-1]+50
        ax[r,c].plot(wavelengths, spectrum, color='b', linewidth=2)
        ax[r,c].set_xlim([mini,maxi])
        for j in elements[i]:
            ax[r,c].axvline(x=j,color='red',linestyle='dashed')
        #ax[r,c].set(xlabel='Wavelength (nm)')
        #ax[r,c].set(ylabel='Intensity')
        ax[r,c].set_title(i)
        #ax[r,c].grid(True)
        r+=1
        if r>3:
            r=0
            c+=1
        if c>3:
            break


    plt.subplots_adjust(top=0.94,
    bottom=0.07,
    left=0.125,
    right=0.9,
    hspace=0.315,
    wspace=0.2)
    #plt.subplot_tool()
    #print(plt.style.available)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()

graph('sample1.png')
