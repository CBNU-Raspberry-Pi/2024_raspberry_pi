import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors


class make_graph:
    def __init__(self):
        self.clim=(350,780)
        norm = plt.Normalize(*self.clim)
        wl = np.arange(self.clim[0],self.clim[1]+1,2)
        colorlist = list(zip(norm(wl),[self.wavelength_to_rgb(w) for w in wl]))
        self.spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)

    def make_image(self, WaveNum_1, WaveNum_2, flux):
        fig, axs = plt.subplots(1, 1, figsize=(8,5), tight_layout=True)
        wavelengths = np.linspace(WaveNum_1, WaveNum_2, 640)
        plt.plot(wavelengths, flux, color='black')

        y = np.linspace(0, 300, 300)
        X,Y = np.meshgrid(wavelengths, y)

        extent=(np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))
        plt.imshow(X, clim=self.clim,  extent=extent, cmap=self.spectralmap, aspect='auto')
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity')
        plt.fill_between(wavelengths, flux, 300, color='w')
        fig.canvas.draw()
        graph = np.array(fig.canvas.renderer._renderer)
        plt.close()
        return(graph)


    def wavelength_to_rgb(self, wavelength, gamma=0.8):
        wavelength = float(wavelength)
        if wavelength >= 380 and wavelength <= 750:
            A = 1.
        else:
            A=0.5
        if wavelength < 380:
            wavelength = 380.
        if wavelength >750:
            wavelength = 750.
        if wavelength >= 380 and wavelength <= 440:
            attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
            R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
            G = 0.0
            B = (1.0 * attenuation) ** gamma
        elif wavelength >= 440 and wavelength <= 490:
            R = 0.0
            G = ((wavelength - 440) / (490 - 440)) ** gamma
            B = 1.0
        elif wavelength >= 490 and wavelength <= 510:
            R = 0.0
            G = 1.0
            B = (-(wavelength - 510) / (510 - 490)) ** gamma
        elif wavelength >= 510 and wavelength <= 580:
            R = ((wavelength - 510) / (580 - 510)) ** gamma
            G = 1.0
            B = 0.0
        elif wavelength >= 580 and wavelength <= 645:
            R = 1.0
            G = (-(wavelength - 645) / (645 - 580)) ** gamma
            B = 0.0
        elif wavelength >= 645 and wavelength <= 750:
            attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
            R = (1.0 * attenuation) ** gamma
            G = 0.0
            B = 0.0
        else:
            R = 0.0
            G = 0.0
            B = 0.0
        return (R,G,B,A)