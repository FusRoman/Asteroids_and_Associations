import pandas as pd
import matplotlib.pyplot as plt

from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np


def load_data(columns=None):
    """
    Load all the observations of solar system object in Fink 
    from the period between 1st of November 2019 and 16th of January 2022

    Parameters
    ----------
    None

    Return
    ------
    sso_data : Pandas Dataframe
        all sso alerts with the following columns
            - 'objectId', 'candid', 'ra', 'dec', 'jd', 'nid', 'fid', 'ssnamenr',
                'ssdistnr', 'magpsf', 'sigmapsf', 'magnr', 'sigmagnr', 'magzpsci',
                'isdiffpos', 'day', 'nb_detection', 'year', 'month'
    """
    return pd.read_parquet("sso_data", columns=columns)

def plot_nb_det_distribution(df):
    """
    Plot the distribution of the number of detection for each sso in Fink
    """
    unique_nb_detection = df.drop_duplicates("ssnamenr")["nb_detection"]
    plt.hist(unique_nb_detection, 100, alpha=0.75, log=True)
    plt.xlabel('Number of detection')
    plt.ylabel('Number of SSO')
    plt.title('Number of detection of each sso in Fink')
    ax = plt.gca()
    plt.text(0.72, 0.8, 'min={},max={},median={}'.format(min(unique_nb_detection), max(unique_nb_detection), int(unique_nb_detection.median())), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    plt.grid(True)
    plt.show()


def plot_tw_distribution(df):
    """
    Plot the distribution of the observation window for each sso in Fink
    """
    tw = df.groupby("ssnamenr").agg(
    tw=("jd", lambda x: list(x)[-1] - list(x)[0])
        ).sort_values("tw")["tw"]
    plt.hist(tw, 100, alpha=0.75, log=True)
    plt.xlabel('Observation window')
    plt.ylabel('Number of SSO')
    plt.title('Observation window of each sso in Fink')
    ax = plt.gca()
    plt.text(0.72, 0.8, 'min={},max={},median={}'.format(min(tw), max(tw), int(tw.median())), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    plt.grid(True)
    plt.show()


def sep_df(x):
    """
    Compute the speed between two observations of solar system object
    """
    ra, dec, jd = x["ra"].values, x["dec"].values, x["jd"].values

    c1 = SkyCoord(ra, dec, unit = u.degree)

    diff_jd = np.diff(jd)

    sep = c1[0:-1].separation(c1[1:]).degree

    velocity = np.divide(sep, diff_jd)

    return velocity