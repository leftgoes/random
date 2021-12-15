import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erf, erfinv
import re


class IQ:
    def __init__(self, men: bool = True):
        self.sigma = 16.2 if men is True else 13.2
        self.mu = 100

    def gaussian(self, x):
        return np.exp(-(x - self.mu)**2/(2 * self.sigma**2))/(self.sigma * np.sqrt(2 * np.pi))

    def antiderivative(self, x) -> float:
        return erf((x - self.mu) / (np.sqrt(2) * self.sigma)) / 2

    def percentile(self, x: float) -> float:
        return 100 * (0.5 + self.antiderivative(x))

    def one_out_of(self, x: float) -> float:
        return -1/(self.antiderivative(x) - 0.5)

    def iq(self, x: float) -> float:
        percentile -= 0.5
        return np.sqrt(2) * self.sigma * erfinv(2 * x) + self.mu

    def graph(self, plot_iq: float = None, start: float = 40, end: float = 160):
        x = np.linspace(start, end, 500)
        y = self.gaussian(x)

        plt.xlabel('IQ')
        plt.ylabel('probability')
        plt.plot(x, y)

        if plot_iq is not None:
            percentile = self.percentile(plot_iq)
            if percentile > 99:
                p = str(round(percentile, re.search(r'[^9]', str(percentile)[3:]).start() + 1)) + 'th'
            else:
                p = str(round(percentile))
                p += 'st' if p.endswith('1') else 'nd' if p.endswith('2') else 'rd' if p.endswith('3') else 'th'
            plt.title(f'IQ = {plot_iq}, {p} percentile, 1 out of {round(self.one_out_of(plot_iq))}')
            plt.axvline(plot_iq, ls='--', c='red', lw=.8)
            plt.axhline(self.gaussian(plot_iq), ls='--', c='red', lw=.8)
            plt.plot(plot_iq, self.gaussian(plot_iq), 'o', c='black', ms=4)
        plt.show()


if __name__ == '__main__':
    iq = IQ()
    iq.graph(YOUR_IQ)
