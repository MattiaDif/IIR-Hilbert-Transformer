# @title      IIR HIlbert filter implementation
# @author     Mattia Di Florio
# @date       19 dic 2023
# @version    0.1
# @copyright
# © 2023 Mattia Di Florio
# SPDX-License-Identifier: MIT License
#
# @brief
# IIR Hilbert filter implementation as a cascade of 1st order sections
# For more info, refer to:
# Harris et al., "An Infinite Impulse Response (IIR) Hilbert Transformer Design Technique for Audio." 
# Audio Engineering Society Convention 129. Audio Engineering Society, 2010.
# 
# @changelog
# > 



import matplotlib.pyplot as plt
import numpy as np
from scipy import signal



class AllPass:

    def __init__(self, fs, f1, As, f2=0, N=0, warping=False):
        """
        Input:
        - fs: sampling frequency (Hz)
        - f1: starting passband edge frequency (Hz)
        - As: stopband attenuation (dB)
        - f2: stopping passband edge frequency (Hz)
        - N : order of the filter
        - warping: if applying warping or not

        IF WARPING IS NOT USED, JUST SET f1 --> PASSBAND EDGE FREQUENCY, f2 IS NOT REQUIRED
        BECAUSE THE FINAL PASSBAND IS COMPUTED

        IF WARPING IS USED, SETH BOTH f1 AND f2 --> THE FINAL PASSBAND WILL BE THE BAND
        BETWEEN f1 AND f2

        IN THE ORDER N IS NOT SPECIFIED, IT WILL BE AUTOMATICALLY COMPUTED 
        """

        self._fs      = fs
        self._As      = As
        self._N       = N

        if warping:
            self._f1 = f1
            if f2 == 0:
                raise AttributeError('If warping is used, please specify f2')
            self._f2 = f2
            self._coeff_generation_warping()
        else:
            self._f1 = f1
            self._coeff_generation()



    def _plt_fresp(self):
        """
        Plot frequency response
        """

        fig, ax1 = plt.subplots()
        ax1.set_title('Digital filter frequency response (Imaginary part)')
        ax1.plot(self._w, 20 * np.log10(abs(self._hi)), 'b')
        ax1.set_ylabel('Amplitude [dB]', color='b')
        ax1.set_xlabel('Frequency [Hz]')
        ax2 = ax1.twinx()
        angles_i = np.unwrap(np.angle(self._hi, deg=False))
        ax2.plot(self._w, angles_i, 'g')
        ax2.set_ylabel('Angle (deg)', color='g')
        ax2.grid(True)
        ax2.axis('tight')


        fig, ax3 = plt.subplots()
        ax3.set_title('Digital filter frequency response (Real part)')
        ax3.plot(self._w, 20 * np.log10(abs(self._hr)), 'b')
        ax3.set_ylabel('Amplitude [dB]', color='b')
        ax3.set_xlabel('Frequency [Hz]')
        ax4 = ax3.twinx()
        angles_r = np.unwrap(np.angle(self._hr, deg=False))
        ax4.plot(self._w, angles_r, 'g')
        ax4.set_ylabel('Angle (deg)', color='g')
        ax4.grid(True)
        ax4.axis('tight')


        fig, ax5 = plt.subplots()
        ax5.set_title('Phase response difference between Real and Imaginary')
        ax5.plot(self._w, 180*(angles_r-angles_i)/np.pi, 'g')
        ax5.set_ylabel('Angle (deg)', color='g')
        ax5.grid(True)
        ax5.axis('tight')

        plt.show()



    def _coeff_generation(self):
        """
        IIR HIlber filter coefficients generation
        """

        ####################################################################
        ####################################################################
        ####################################################################
        #### parameters initialization ####
        
        fn     = self._fs/2
        wp     = self._f1*np.pi/fn
        ws     = np.pi - wp

        ds     = pow(10, -self._As/20)

        r      = np.tan(wp/2)/np.tan(ws/2)
        rr     = np.sqrt(1-r**2)
        q0     = (1-np.sqrt(rr))/(2*(1+np.sqrt(rr)))
        q      = q0 + 2*(q0**5) + 15*(q0**9) + 150*(q0**13)




        ####################################################################
        ####################################################################
        ####################################################################
        #### filter order ####

        if self._N == 0:
            D         = ((1-ds**2)/(ds**2))**2
            threshold = np.log10(16*D)/np.log10(1/q)
            while self._N < threshold:
                self._N = self._N+1

        if self._N%2 == 0:
            self._N = self._N+1
            print("filter order must be odd, added 1")

        if self._N <= 3:
            self._N = 5
            print("filter order must be odd and greater than 3 for interlacing property, set to 5")

        print("filter order - N: " + str(self._N))




        ####################################################################
        ####################################################################
        ####################################################################
        #### coefficients computation ####

        alpha = []

        for k in range(1, int((self._N-1)/2)+1):
            num = 0
            den = 0
            for i in range(0,7,1):
                tmp_num = ((-1)**i)*(q**(i*(i+1)))*np.sin(((2*1+1)*k*np.pi)/self._N)
                num     = num + tmp_num

                tmp_den = ((-1)**i)*(q**(i*(i+1)))*np.cos((2*1*k*np.pi)/self._N)
                den     = den + tmp_den

            num = 2*(q**0.25)*num
            den = 1 + 2*den
            gamma = num/den

            bk = np.sqrt((1-r*(gamma**2))*(1-((gamma**2)/r)))
            ck = (2*bk)/(1+(gamma**2))

            alpha.append(np.sqrt(((2-ck)/(2+ck))))
            alpha.append(-np.sqrt(((2-ck)/(2+ck))))

        print("coefficients pre-warping: " + str(alpha))




        ####################################################################
        ####################################################################
        ####################################################################
        #### interlacing ####

        A0    = np.zeros((int((self._N-1)/2),1))
        A1    = np.zeros((int((self._N-1)/2),1))
        var   = 0
        idx_0 = 0
        idx_1 = 0

        for idx in range(self._N-2, -1, -1):
            if var < 2:
                A1[idx_1] = -alpha[idx]
                var       = var + 1
                idx_1     = idx_1 + 1
            else:
                A0[idx_0] = -alpha[idx]
                var       = var + 1
                idx_0     = idx_0 + 1
                var       = var%4

        A1 = np.insert(A1, 0, 0)

        print("A0 pre-warping interlaced: " + str(A0))
        print("A1 pre-warping interlaced: " + str(A1))

        self._A0 = A0
        self._A1 = A1




        ####################################################################
        ####################################################################
        ####################################################################
        #### transfer function computation ####

        self._w, hi = signal.freqz([A1[0], 1], [1, A1[0]], worN=1024, fs=self._fs)
        hr          = 1


        for i in range(0, A0.size, 1):
            _, hi_tmp  = signal.freqz([A1[i+1], 1], [1, A1[i+1]], worN=1024, fs=self._fs)
            _, hr_tmp  = signal.freqz([A0[i], 1], [1, A0[i]], worN=1024, fs=self._fs)
            hi         = hi*hi_tmp
            hr         = hr*hr_tmp   

        self._hr = hr
        self._hi = hi

        self._plt_fresp()





    def _coeff_generation_warping(self):
        """
        IIR HIlber filter coefficients generation with warping
        """

        ####################################################################
        ####################################################################
        ####################################################################
        #### parameters initialization ####
        
        fn     = self._fs/2
        w1     = self._f1*np.pi/fn
        w2     = self._f2*np.pi/fn

        tan1   = np.tan(w1/2)
        tan2   = np.tan(w2/2)

        sqrt_p = np.sqrt(tan1/tan2)
        sqrt_s = np.sqrt(tan2/tan1)

        #warping --> improve filter response close to 0
        wp     = 2*np.arctan(sqrt_p)    #f1 for warping
        ws     = 2*np.arctan(sqrt_s)    #f2 for warping

        beta   = np.sqrt(tan1*tan2)
        kb     = (beta-1)/(beta+1)
        ds     = pow(10, -self._As/20)

        r      = np.tan(wp/2)/np.tan(ws/2)
        rr     = np.sqrt(1-r**2)
        q0     = (1-np.sqrt(rr))/(2*(1+np.sqrt(rr)))
        q      = q0 + 2*(q0**5) + 15*(q0**9) + 150*(q0**13)




        ####################################################################
        ####################################################################
        ####################################################################
        #### filter order ####

        if self._N == 0:
            D         = ((1-ds**2)/(ds**2))**2
            threshold = np.log10(16*D)/np.log10(1/q)
            while self._N < threshold:
                self._N = self._N+1

        if self._N%2 == 0:
            self._N = self._N+1
            print("filter order must be odd, added 1")

        if self._N <= 3:
            self._N = 5
            print("filter order must be odd and greater than 3 for interlacing, set to 5")

        print("filter order - N: " + str(self._N))




        ####################################################################
        ####################################################################
        ####################################################################
        #### coefficients computation ####

        alpha = []

        for k in range(1, int((self._N-1)/2)+1):
            num = 0
            den = 0
            for i in range(0,7,1):
                tmp_num = ((-1)**i)*(q**(i*(i+1)))*np.sin(((2*1+1)*k*np.pi)/self._N)
                num     = num + tmp_num

                tmp_den = ((-1)**i)*(q**(i*(i+1)))*np.cos((2*1*k*np.pi)/self._N)
                den     = den + tmp_den

            num = 2*(q**0.25)*num
            den = 1 + 2*den
            gamma = num/den

            bk = np.sqrt((1-r*(gamma**2))*(1-((gamma**2)/r)))
            ck = (2*bk)/(1+(gamma**2))

            alpha.append(np.sqrt(((2-ck)/(2+ck))))
            alpha.append(-np.sqrt(((2-ck)/(2+ck))))

        print("coefficients pre-warping: " + str(alpha))




        ####################################################################
        ####################################################################
        ####################################################################
        #### interlacing ####

        A0    = np.zeros((int((self._N-1)/2),1))
        A1    = np.zeros((int((self._N-1)/2),1))
        var   = 0
        idx_0 = 0
        idx_1 = 0

        for idx in range(self._N-2, -1, -1):
            if var < 2:
                A1[idx_1] = -alpha[idx]
                var       = var + 1
                idx_1     = idx_1 + 1
            else:
                A0[idx_0] = -alpha[idx]
                var       = var + 1
                idx_0     = idx_0 + 1
                var       = var%4

        A1 = np.insert(A1, 0, 0)

        print("A0 pre-warping interlaced: " + str(A0))
        print("A1 pre-warping interlaced: " + str(A1))




        ####################################################################
        ####################################################################
        ####################################################################
        #### warping ####

        A0_w    = np.zeros((int((self._N-1)/2),1))
        A1_w    = np.zeros((int((self._N-1)/2)+1,1))

        for i in range(0, A0.size, 1):
            A0_w[i] = (-A0[i] + kb)/(-A0[i]*kb + 1);

        print(A0.size)

        for i in range(0, A1.size, 1):
            A1_w[i] = (-A1[i] + kb)/(-A1[i]*kb + 1);

        print("A0 warped: " + str(A0_w))
        print("A1 warped: " + str(A1_w))

        self._A0 = A0_w
        self._A1 = A1_w




        ####################################################################
        ####################################################################
        ####################################################################
        #### transfer function computation ####

        self._w, hi = signal.freqz([A1_w[0], 1], [1, A1_w[0]], worN=1024, fs=self._fs)
        hr          = 1


        for i in range(0, A0.size, 1):
            _, hi_tmp  = signal.freqz([A1_w[i+1], 1], [1, A1_w[i+1]], worN=1024, fs=self._fs)
            _, hr_tmp  = signal.freqz([A0_w[i], 1], [1, A0_w[i]], worN=1024, fs=self._fs)
            hi         = hi*hi_tmp
            hr         = hr*hr_tmp   

        self._hr = hr
        self._hi = hi

        self._plt_fresp()

