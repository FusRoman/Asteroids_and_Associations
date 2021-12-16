from astropy import coordinates
import numpy as np
import pandas as pd
from astropy.time import Time
from astropy.coordinates import SkyCoord
import astropy.units as u
from shutil import copyfile
import re
import subprocess
import os
import multiprocessing as mp
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from alert_association.continuous_integration import load_data


def time_to_decimal(time):
    return str(int(time[0]) * 3600 + int(time[1]) * 60 + int(time[0]))


def split_string(string, char_split="-"):
    return string.split(char_split)


def join_string(list_string, join_string):
    return join_string.join(list_string)


def concat_date(list_date):
    first_list = join_string(list_date[:-2], " ")
    return join_string([first_list] + list_date[-2:], "")


def band_to_str(band):
    if band == 1:
        return "g"
    elif band == 2:
        return "r"


half_month_letter = {
    "01": ["A", "B"],
    "02": ["C", "D"],
    "03": ["E", "F"],
    "04": ["G", "H"],
    "05": ["J", "K"],
    "06": ["L", "M"],
    "07": ["N", "O"],
    "08": ["P", "Q"],
    "09": ["R", "S"],
    "10": ["T", "U"],
    "11": ["V", "W"],
    "12": ["X", "Y"],
}


def second_letter(i, lowercase=True):
    """
    Examples
    --------
    >>> second_letter(1)
    'A'
    >>> second_letter(25)
    'Z'
    >>> second_letter(1, False)
    'a'
    >>> second_letter(25, False)
    'z'
    >>> second_letter(9)
    'J'
    >>> second_letter(9, False)
    'j'
    """
    if lowercase:
        case = 64
    else:
        case = 96

    if i <= 8:
        return chr(i + case)
    elif i <= 25:
        return chr(i + case + 1)


def left_shift(number, n):
    """
    Examples
    --------
    >>> left_shift(152, 1)
    15
    >>> left_shift(14589, 3)
    14
    """
    return number // 10 ** n


def right_shift(number, n):
    """
    Examples
    --------
    >>> right_shift(123, 1)
    3
    >>> right_shift(0, 1)
    0
    >>> right_shift(1234, 2)
    34
    """
    return number % 10 ** n


def letter_cycle(cycle):
    """
    Examples
    --------
    >>> letter_cycle(10)
    'A'
    >>> letter_cycle(19)
    'J'
    >>> letter_cycle(35)
    'Z'
    >>> letter_cycle(44)
    'j'
    >>> letter_cycle(60)
    'z'
    """
    cycle -= 10
    r = (cycle - 1) // 25
    if r > 0:
        cycle %= 25

        if cycle == 0:
            cycle = 25

        return second_letter(cycle, lowercase=False)
    else:
        if cycle == 0:
            cycle = 1
        elif cycle <= 8 and cycle >= 1:
            cycle += 1
        return second_letter(cycle)


def make_cycle(cycle):
    """
    Examples
    --------
    >>> make_cycle(0)
    '00'
    >>> make_cycle(10)
    '10'
    >>> make_cycle(108)
    'A8'
    >>> make_cycle(110)
    'B0'
    >>> make_cycle(127)
    'C7'
    >>> make_cycle(162)
    'G2'
    >>> make_cycle(193)
    'J3'
    >>> make_cycle(348)
    'Y8'
    >>> make_cycle(355)
    'Z5'
    >>> make_cycle(360)
    'a0'
    >>> make_cycle(418)
    'f8'
    >>> make_cycle(439)
    'h9'
    >>> make_cycle(440)
    'j0'
    """
    if cycle <= 9:
        return "0" + str(cycle)
    elif cycle <= 99:
        return str(cycle)
    else:
        digit = left_shift(cycle, 1)
        unit = right_shift(cycle, 1)
        return str(letter_cycle(digit)) + str(unit)


def make_designation(time, discovery_number):
    """
    Examples
    --------
    >>> make_designation("2021-05-22 07:33:02.111", 0)
    'K21K00A'
    >>> make_designation("2021-05-22 07:33:02.111", 24)
    'K21K00Z'
    >>> make_designation("2021-05-22 07:33:02.111", 25)
    'K21K01A'
    >>> make_designation("2021-05-22 07:33:02.111", 49)
    'K21K01Z'
    >>> make_designation("2021-05-22 07:33:02.111", 50)
    'K21K02A'
    >>> make_designation("2021-05-22 07:33:02.111", 8999)
    'K21KZ9Z'
    >>> make_designation("2021-05-22 07:33:02.111", 9000)
    'K21Ka0A'
    >>> make_designation("2021-01-01 07:33:02.111", 0)
    'K21A00A'
    >>> make_designation("2022-07-04 07:33:02.111", 0)
    'K22N00A'
    """
    time_split = time.split(" ")[0].split("-")
    year = time_split[0][-2:]

    half_month = half_month_letter[time_split[1]]
    if int(time_split[2]) <= 15:
        half_month = half_month[0]
    else:
        half_month = half_month[1]

    order = discovery_number % 25 + 1
    cycle = int(discovery_number / 25)
    return "K" + year + half_month + make_cycle(cycle) + second_letter(order)


def make_date(date):
    d = date.split(" ")
    return concat_date(d[0].split("-") + ["."] + [time_to_decimal(d[1].split(":"))])


def write_observation_file(obs_df):
    obs_df = obs_df.sort_values(["trajectory_id", "jd"])
    ra = obs_df["ra"]
    dec = obs_df["dec"]
    dcmag = obs_df["dcmag"]
    band = obs_df["fid"]
    date = obs_df["jd"]
    traj_id = obs_df["trajectory_id"].values[0]

    coord = SkyCoord(ra, dec, unit=u.degree).to_string("hmsdms")
    translation_rules = {ord(i): " " for i in "hmd"}
    translation_rules[ord("s")] = ""
    coord = [el.translate(translation_rules) for el in coord]

    coord = [
        re.sub(r"(\d+)\.(\d+)", lambda matchobj: matchobj.group()[:5], s) for s in coord
    ]

    t = Time(date, format="jd")
    date = t.iso
    prov_desig = make_designation(date[0], traj_id)

    date = [make_date(d) for d in date]
    res = [join_string([el1] + [el2], " ") for el1, el2 in zip(date, coord)]
    res = [
        "     "
        + prov_desig
        + "  C"  # how the observation was made : C means CCD
        + el
        + "         "
        + str(round(mag, 1))
        + " "
        + band_to_str(b)
        + "      I41"  # ZTF observation code
        for el, mag, b in zip(res, dcmag, band)
    ]

    dir_path = "mpcobs/"
    with open(dir_path + prov_desig + ".obs", "wt") as file:
        file.write(join_string(res, "\n"))

    return prov_desig


def write_inp(provisional_designation):
    with open(provisional_designation + ".inp", "wt") as file:
        file.write(provisional_designation)


def write_oop(provisional_designation):
    oop_template = "template.oop"
    copyfile(oop_template, provisional_designation + ".oop")


def prep_orbitfit():

    dir_path = "mpcobs/"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    subprocess.call(
        ["ln", "-s", "OrbitFit/tests/bineph/testout/AST17.bai_431_fcct", "AST17.bai"]
    )
    subprocess.call(
        ["ln", "-s", "OrbitFit/tests/bineph/testout/AST17.bep_431_fcct", "AST17.bep"]
    )


def call_orbitfit(provisional_designation):
    orbitfit_path = "OrbitFit/bin/"
    command = (
        "./"
        + orbitfit_path
        + "orbfit.x < "
        + provisional_designation
        + ".inp >/dev/null 2>&1"
    )
    subprocess.call([command], shell=True)


def obs_clean(prov_desig):
    command1 = "rm " + prov_desig
    subprocess.call([command1], shell=True)


def seq_obs_clean(prov_desig):
    command1 = "rm " + prov_desig + ".*"
    command2 = "rm mpcobs/" + prov_desig + ".*"
    subprocess.call([command1], shell=True)
    subprocess.call([command2], shell=True)


def final_clean():
    command = "rm -rf *.bai *.bep *.log mpcobs"
    subprocess.call([command], shell=True)


def read_oel(prov_desig):
    try:
        with open(prov_desig + ".oel") as file:
            lines = file.readlines()
            orb_params = " ".join(lines[7].strip().split()).split(" ")
            if len(lines) > 12:
                rms = " ".join(lines[12].strip().split()).split(" ")
            else:
                rms = [-1, -1, -1, -1, -1, -1, -1, -1]
            return orb_params[1:] + rms[2:]
    except FileNotFoundError:
        return list(np.ones(12, dtype=np.float64) * -1)


def get_orbit_param(df):
    traj_id = df["trajectory_id"].values[0]
    prov_desig = write_observation_file(df)
    write_inp(prov_desig)
    write_oop(prov_desig)
    call_orbitfit(prov_desig)
    return [traj_id, prov_desig] + read_oel(prov_desig)


def compute_df_orbit_param(trajectory_df, cpu_count):
    all_traj_id = np.unique(trajectory_df["trajectory_id"])

    prep_orbitfit()
    all_track = [mpc[mpc["trajectory_id"] == traj_id] for traj_id in all_traj_id]
    pool = mp.Pool(cpu_count)
    results = pool.map(get_orbit_param, all_track)
    pool.close()
    obs_clean(
        join_string(
            [res[1] + ".*" + " mpcobs/" + res[1] + ".*" for res in results], " "
        )
    )
    final_clean()

    return orbit_elem_dataframe(np.array(results))


def orbit_elem_dataframe(orbit_elem):

    column_name = [
        "trajectory_id",
        "provisional designation",
        "a",
        "e",
        "i",
        "long. node",
        "arg. peric",
        "mean anomaly",
        "rms_a",
        "rms_e",
        "rms_i",
        "rms_long. node",
        "rms_arg. peric",
        "rms_mean anomaly",
    ]

    df_orb_elem = pd.DataFrame(orbit_elem, columns=column_name,)

    for col_name in set(column_name).difference(set(["provisional designation"])):
        df_orb_elem[col_name] = pd.to_numeric(df_orb_elem[col_name])

    return df_orb_elem


def get_mpc_database():

    mpc_database = pd.read_json("../../data/mpc_database/mpcorb_extended.json")
    mpc_database["Number"] = mpc_database["Number"].astype("string").str[1:-1]
    return mpc_database

def color_dict(mpc_database):
    orbit_color = [
        "gold",
        "red",
        "dodgerblue",
        "limegreen",
        "grey",
        "magenta",
        "chocolate",
        "blue",
        "orange",
        "mediumspringgreen",
        "deeppink",
    ]

    return {
        orbit_type: orbit_color
        for orbit_type, orbit_color in zip(
            np.unique(mpc_database["Orbit_type"]), orbit_color
        )
    }

def plot_residue(df, orbit_color, n_trajectories, n_points):
    df = df.reset_index(drop=True)
    orbit_type = np.unique(df["Orbit_type"])
    computed_elem = df[
        ["a_x", "e_x", "i_x", "long. node", "arg. peric", "mean anomaly"]
    ]
    known_elem = df[["a_y", "e_y", "i_y", "Node", "Peri", "M"]]

    df[["da", "de", "di", "dNode", "dPeri", "dM"]] = (
        computed_elem.values - known_elem.values
    )

    fig, axes = plt.subplots(3, 2, sharex=True)
    fig.suptitle("Orbital elements residuals, {} trajectories, {} points".format(n_trajectories, n_points))

    subplot_title = [
        "semi-major axis",
        "eccentricity",
        "inclination",
        "Longitude of the ascending node",
        "Argument of perihelion",
        "Mean anomaly"
    ]

    for ax, orb_elem, title in zip(axes.flatten(), ["da", "de", "di", "dNode", "dPeri", "dM"], subplot_title):
        ax.set_title(title)
        ax.axhline(0, ls="--", color="grey")
        for otype in orbit_type:
            v = df[df["Orbit_type"] == otype]
            omean = np.mean(v[orb_elem].values)

            failed_orb = np.where(v["a_x"].values == -1)
            success_orb = np.where(v["a_x"].values != -1)
            ax.scatter(
                np.array(v.index)[success_orb],
                v[orb_elem].values[success_orb],
                label="{}: {}, mean : {}, fail: {}".format(
                    otype, len(v), np.around(omean, decimals=4), len(failed_orb[0])
                ),
                color=orbit_color[otype],
            )
            ax.scatter(
                np.array(v.index)[failed_orb],
                v[orb_elem].values[failed_orb],
                marker="x",
                color=orbit_color[otype],
            )

            ax.axhline(omean, ls=":", color=orbit_color[otype])
            ax.set_ylabel("$\delta$ {}".format(orb_elem[1:]))
        ax.legend(prop={"size": 7})

    plt.show()


def plot_cpu_time(all_time, n_trajectories, n_points):

    plt.plot(np.arange(1, mp.cpu_count() + 1), all_time)
    plt.xlabel("number of cpu")
    plt.ylabel("computation time")
    plt.title("CPU Time analysis, {} trajectories with {} points".format(n_trajectories, n_points))
    plt.show()

if __name__ == "__main__":
    print("Load sso data")
    data_path = "../data/month=0"
    df_sso = load_data("Solar System MPC")

    exit()
    import doctest
    import time as t

    doctest.testmod()[0]

    n_trajectories = 3000
    n_points = 20

    gb_ssn = df_sso.groupby(["ssnamenr"]).agg({"candid": len}).sort_values(["candid"])
    all_track = gb_ssn[gb_ssn["candid"] == n_points].reset_index()["ssnamenr"].values
    mpc = df_sso[df_sso["ssnamenr"].isin(all_track[:n_trajectories])][
        ["ra", "dec", "dcmag", "fid", "jd", "ssnamenr"]
    ]
    all_ssnamenr = np.unique(mpc["ssnamenr"].values)
    ssnamenr_translate = {
        ssn: i for ssn, i in zip(all_ssnamenr, range(len(all_ssnamenr)))
    }
    mpc["trajectory_id"] = mpc.apply(
        lambda x: ssnamenr_translate[x["ssnamenr"]], axis=1
    )
    mpc["ssnamenr"] = mpc["ssnamenr"].astype("string")
    
    print("MPC DATABASE loading")
    t_before = t.time()
    mpc_database = get_mpc_database()

    print("MPC DATABASE end loading, elapsed time: {}".format(t.time() - t_before))
    print()

    print("orbital element computation started, n_trajectories: {}".format(min(n_trajectories, len(all_track))))
    t_before = t.time()
    orbit_results = compute_df_orbit_param(mpc, mp.cpu_count())
    multiprocess_time = t.time() - t_before
    print("total multiprocessing orbfit time: {}".format(multiprocess_time))

    ztf_mpc_with_orbit_param = mpc.merge(orbit_results, on="trajectory_id")
    print()
    print("cross match with mpc database")
    cross_match_mpc = ztf_mpc_with_orbit_param.merge(
        mpc_database, how="inner", left_on="ssnamenr", right_on="Number"
    )

    dict_color_orbit = color_dict(mpc_database)
    plot_residue(cross_match_mpc.drop_duplicates(["ssnamenr"]), dict_color_orbit, min(n_trajectories, len(all_track)), n_points)

    exit()
    # Sequential orbitfit
    t_before_tot = t.time()
    all_traj_id = np.unique(mpc["trajectory_id"])
    prep_orbitfit()
    for traj_id in all_traj_id:
        current_mpc = mpc[mpc["trajectory_id"] == traj_id]
        t_before = t.time()
        prov_desig = write_observation_file(current_mpc)
        write_inp(prov_desig)
        write_oop(prov_desig)
        call_orbitfit(prov_desig)
        mpc.loc[current_mpc.index, "prov_desig"] = prov_desig
        orb_elem = read_oel(prov_desig)
        seq_obs_clean(prov_desig)
        # print("traj_id: {}, nb observation: {}, write time: {}".format(traj_id, len(current_mpc), t.time() - t_before))
    final_clean()
    sequential_time = t.time() - t_before_tot
    print(
        "total sequential orbfit time: {}\nratio: {} %".format(
            sequential_time, (multiprocess_time / sequential_time) * 100
        )
    )
