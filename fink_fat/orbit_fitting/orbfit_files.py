import os
import traceback
import logging
from glob import glob
import numpy as np

from fink_fat import __file__


def write_inp(ram_dir, first_designation, second_designation=None):
    """
    Write the input files of Orbfit.
    Two designations can be given to perform an orbit fitting for two trajectory arcs.

    Parameters
    ----------
    ram_dir : string
        the path where to write the temporary file generated by orbfit.
    first_designation : string
        the provisional designation of the first arc
    second_designation : string
        the provisional designation of the second arc

    Return
    ------
    None

    Examples
    --------
    >>> write_inp("fink_fat/test/", "DESIG1")
    >>> filecmp.cmp("fink_fat/test/DESIG1.inp", "fink_fat/test/DESIG1_test.inp")
    True

    >>> write_inp("fink_fat/test/", "DESIG1", "DESIG2")
    >>> filecmp.cmp("fink_fat/test/DESIG1_DESIG2.inp", "fink_fat/test/DESIG1_DESIG2_test.inp")
    True

    >>> os.remove("fink_fat/test/DESIG1.inp")
    >>> os.remove("fink_fat/test/DESIG1_DESIG2.inp")
    """
    if second_designation is None:
        with open(ram_dir + first_designation + ".inp", "wt") as file:
            file.write(ram_dir + first_designation)
    else:
        with open(
            ram_dir + first_designation + "_" + second_designation + ".inp", "wt"
        ) as file:
            file.write(ram_dir + first_designation + "_" + second_designation)


def oop_options(
    file,
    ram_dir,
    first_desig,
    second_desig=None,
    prop_epoch=None,
    n_triplets=10,
    noise_ntrials=10,
    with_ephem=0,
    start_ephem=None,
    end_ephem=None,
    step_ephem=None,
    obscode=None,
    verbose=1,
):
    """
    Write the lines of the OrbFit options file.

    Parameters
    ----------
    file : file object
        the file descriptor for the OrbFit options file.
    ram_dir : string
        the path where to write the temporary file generated by orbfit.
    first_designation : string
        the provisional designation of the first arc
    second_designation : string
        the provisional designation of the second arc
    prop_epoch : string
        Epoch at which output orbital elements
        Epochs can be specified in Julian Days, Modified Julian Days or
        calendar date/time, according to the following examples
        prop_epoch     = CAL 1998/Jun/18 22:35:40.00 UTC
            or         = CAL 1998/06/18  22:35:40.00 UTC
            or         = JD  2450983.44143519 UTC
            or         = MJD 50982.94143519 UTC ! MJD with fractional part
            or         = MJD 50982 81340.00 UTC ! integer MJD & secs within day)
    n_triplets : integer
        max number of triplets of observations to be tried for the initial orbit determination
    noise_ntrials : integer
        number of trials for each triplet for the initial orbit determination
    with_ephem : integer
        Compute the ephemeris or not:
            0: no ephemeris
            1: compute ephemeris is possible
            2: always compute ephemeris
    start_ephem : string
        start date to compute the ephemeris, same format as the prop_epoch keyword.
    end_epehm : string
        start date to compute the ephemeris.
    step_ephem : float
        Ephemeris stepsize in days
    obscode : integer
        Observatory code for which ephemeris has to be computed, required for applying topocentric correction.
        Observatory codes can be found here : https://en.wikipedia.org/wiki/List_of_observatory_codes
        Take only the observatory code before 999 (those without letters).
    verbose : integer
        Verbosity levels of Orbfit
        1 = summary information on the solution found
        2 = summary information on all trials
        3 = debug

    Returns
    -------
    None

    Examples
    --------
    >>> file = open("fink_fat/test/test.oop", "w")
    >>> oop_options(file, "fink_fat/test/", "DESIG1")
    >>> file.close()
    >>> filecmp.cmp("fink_fat/test/test.oop", "fink_fat/test/DESIG1_test.oop")
    True

    >>> os.remove("fink_fat/test/test.oop")

    >>> file = open("fink_fat/test/test.oop", "w")
    >>> oop_options(file, "fink_fat/test/", "DESIG1", "DESIG2", "JD  2450983.44143519 UTC", 24, 12, 1, "JD  2450993.44143519 UTC", "JD  2451003.44143519 UTC", 5.3, 675)
    >>> file.close()
    >>> filecmp.cmp("fink_fat/test/test.oop", "fink_fat/test/DESIG1_DESIG2_test.oop")
    True

    >>> os.remove("fink_fat/test/test.oop")

    >>> file = open("fink_fat/test/test.oop", "w")
    >>> oop_options(file, "fink_fat/test/", "DESIG1", "DESIG2", "JD  2450983.44143519 UTC", -3, -10, 1, "JD  2450993.44143519 UTC", "JD  2451003.44143519 UTC", -2, 675)
    >>> file.close()

    >>> filecmp.cmp("fink_fat/test/test.oop", "fink_fat/test/DESIG1_DESIG2_neg_test.oop")
    True

    >>> os.remove("fink_fat/test/test.oop")

    >>> file = open("fink_fat/test/test.oop", "w")
    >>> oop_options(file, "fink_fat/test/", "DESIG1", with_ephem=10, verbose=10)
    >>> file.close()

    >>> filecmp.cmp("fink_fat/test/test.oop", "fink_fat/test/DESIG1_no_ephem_test.oop")
    True

    >>> os.remove("fink_fat/test/test.oop")
    """
    # write output options
    file.write("output.\n")
    file.write("\t.elements = 'KEP'\n")
    if prop_epoch is not None:
        file.write("\t.epoch = {}\n".format(prop_epoch))

    # write init_orb options
    file.write("init_orbdet.\n")
    if verbose not in [1, 2, 3]:
        verbose = 1
    file.write("\t.verbose = {}\n".format(verbose))
    if n_triplets <= 0:
        n_triplets = 10
    file.write("\t.n_triplets = {}\n".format(n_triplets))
    if noise_ntrials <= 0:
        noise_ntrials = 10
    file.write("\t.noise.ntrials = {}\n".format(noise_ntrials))

    # write operations options
    file.write("operations.\n")
    file.write("\t.init_orbdet = 2\n")
    file.write("\t.diffcor = 2\n")
    if second_desig is None:
        file.write("\t.ident = 0\n")
    else:
        file.write("\t.ident = 2\n")

    if with_ephem not in [0, 1, 2]:
        with_ephem = 0
    file.write("\t.ephem = {}\n".format(with_ephem))

    if with_ephem in [1, 2]:
        # write ephem options
        file.write("ephem.\n")
        file.write("\t.epoch.start = {}\n".format(start_ephem))
        file.write("\t.epoch.end = {}\n".format(end_ephem))
        if step_ephem is not None:
            if step_ephem <= 0:
                step_ephem = 1
            file.write("\t.step = {}\n".format(step_ephem))
        file.write("\t.obscode =  {}\n".format(obscode))
        file.write("\t.timescale = UTC\n")
        file.write(
            "\t.fields = cal,mjd,coord,mag,delta,r,elong,phase,glat,appmot,skyerr\n"
        )

    # write error model options
    file.write("error_model.\n")
    file.write("\t.name='fcct14'\n")

    # write additional options
    file.write("IERS.\n")
    file.write("\t.extrapolation = .T.\n")

    # write reject options
    file.write("reject.\n")
    file.write("\t.rejopp = .FALSE.\n")

    # write propagation options
    file.write("propag.\n")
    file.write("\t.iast = 17\n")
    file.write("\t.npoint = 600\n")
    file.write("\t.dmea = 0.2d0\n")
    file.write("\t.dter = 0.05d0\n")

    # write location files options
    file.write("\t.filbe=" + ram_dir + "AST17\n")
    file.write("\noutput_files.\n")

    if second_desig is None:
        file.write("\t.elem = " + ram_dir + first_desig + ".oel\n")
    else:
        file.write("\t.elem = " + ram_dir + first_desig + "_" + second_desig + ".oel\n")

    file.write("object1.\n")
    file.write("\t.obs_dir = " + ram_dir + "mpcobs\n")
    file.write("\t.name = " + first_desig)

    if second_desig is not None:
        # write second object location
        file.write("\nobject2.\n")
        file.write("\t.obs_dir = " + ram_dir + "mpcobs\n")
        file.write("\t.name = " + second_desig)


def write_oop(
    ram_dir,
    first_designation,
    second_designation=None,
    prop_epoch=None,
    n_triplets=10,
    noise_ntrials=10,
    with_ephem=0,
    start_ephem=None,
    end_ephem=None,
    step_ephem=None,
    obscode=None,
    verbose=1,
):
    """
    Write the option file of OrbFit.

    Parameters
    ----------
    ram_dir : string
        the path where to write the temporary file generated by orbfit.
    first_designation : string
        the provisional designation of the first arc
    second_designation : string
        the provisional designation of the second arc
    prop_epoch : string
        Epoch at which output orbital elements
        Epochs can be specified in Julian Days, Modified Julian Days or
        calendar date/time, according to the following examples
        prop_epoch     = CAL 1998/Jun/18 22:35:40.00 UTC
            or         = CAL 1998/06/18  22:35:40.00 UTC
            or         = JD  2450983.44143519 UTC
            or         = MJD 50982.94143519 UTC ! MJD with fractional part
            or         = MJD 50982 81340.00 UTC ! integer MJD & secs within day)
    n_triplets : integer
        max number of triplets of observations to be tried for the initial orbit determination
    noise_ntrials : integer
        number of trials for each triplet for the initial orbit determination
    with_ephem : integer
        Compute the ephemeris or not:
            0: no ephemeris
            1: compute ephemeris is possible
            2: always compute ephemeris
    start_ephem : string
        start date to compute the ephemeris, same format as the prop_epoch keyword.
    end_epehm : string
        start date to compute the ephemeris.
    step_ephem : float
        Ephemeris stepsize in days
    obscode : integer
        Observatory code for which ephemeris has to be computed, required for applying topocentric correction.
        Observatory codes can be found here : https://en.wikipedia.org/wiki/List_of_observatory_codes
        Take only the observatory code before 999 (those without letters).
    verbose : integer
        Verbosity levels of Orbfit
        1 = summary information on the solution found
        2 = summary information on all trials
        3 = debug

    Return
    ------
    None

    Examples
    --------
    >>> write_oop("fink_fat/test/", "DESIG1")
    >>> filecmp.cmp("fink_fat/test/DESIG1.oop", "fink_fat/test/DESIG1_test.oop")
    True

    >>> os.remove("fink_fat/test/DESIG1.oop")

    >>> write_oop("fink_fat/test/", "DESIG1", "DESIG2")
    >>> filecmp.cmp("fink_fat/test/DESIG1_DESIG2.oop", "fink_fat/test/DESIG1_DESIG2_test2.oop")
    True

    >>> os.remove("fink_fat/test/DESIG1_DESIG2.oop")
    """
    if second_designation is None:
        with open(ram_dir + first_designation + ".oop", "w") as file:
            oop_options(
                file,
                ram_dir,
                first_designation,
                prop_epoch=prop_epoch,
                n_triplets=n_triplets,
                noise_ntrials=noise_ntrials,
                with_ephem=with_ephem,
                start_ephem=start_ephem,
                end_ephem=end_ephem,
                step_ephem=step_ephem,
                obscode=obscode,
                verbose=verbose,
            )
    else:
        with open(
            ram_dir + first_designation + "_" + second_designation + ".oop", "w"
        ) as file:
            oop_options(
                file,
                ram_dir,
                first_designation,
                second_desig=second_designation,
                prop_epoch=prop_epoch,
                n_triplets=n_triplets,
                noise_ntrials=noise_ntrials,
                with_ephem=with_ephem,
                start_ephem=start_ephem,
                end_ephem=end_ephem,
                step_ephem=step_ephem,
                obscode=obscode,
                verbose=verbose,
            )


def prep_orbitfit(ram_dir):
    """
    Preparation for OrbFit computation

    Copy the AST17 ephemeris files needed for the orbfit computation to the correct location.
    Set their permissions to be read by OrbFit.

    Parameters
    ----------
    ram_dir : string
        path where to write file

    Returns
    -------

    Examples
    --------

    >>> prep_orbitfit("")

    >>> os.path.islink("AST17.bai")
    True

    >>> os.path.islink("AST17.bep")
    True

    >>> shutil.rmtree("mpcobs")
    >>> os.remove("AST17.bai")
    >>> os.remove("AST17.bep")
    """

    try:
        fink_fat_path = os.path.dirname(__file__)
        orbfit_path = os.path.join(fink_fat_path, "orbit_fitting")
        dir_path = ram_dir + "mpcobs/"

        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        if not os.path.islink(ram_dir + "AST17.bai"):
            os.symlink(
                os.path.join(orbfit_path, "AST17.bai_431_fcct"), ram_dir + "AST17.bai"
            )

        if not os.path.islink(ram_dir + "AST17.bep"):
            os.symlink(
                os.path.join(orbfit_path, "AST17.bep_431_fcct"), ram_dir + "AST17.bep"
            )
    except Exception:  # pragma: no cover
        logging.error(traceback.format_exc())


def rm_files(files):
    """
    Remove all files contains in the files parameters

    Parameters
    files : string list
        A list of files path (typically return by the glob library)

    Return
    ------
    None
    """
    for path_f in files:
        os.remove(path_f)


def obs_clean(ram_dir, prov_desig):
    """
    Remove all the temporary file named as prov_desig created during the OrbFit process.

    Parameters
    ----------
    ram_dir : string
        Path where files are located
    prov_desig : string
        the provisional designation of the trajectory that triggered the OrbFit process.

    Returns
    -------
    None

    Examples
    --------

    >>> prov_desig = "A000001"
    >>> open(prov_desig + ".oel", 'a').close()
    >>> open(prov_desig + ".err", 'a').close()

    # >>> os.makedirs("mpcobs")
    >>> open("mpcobs/" + prov_desig + ".obs", 'a').close()
    >>> open("mpcobs/" + prov_desig + ".rwo", 'a').close()

    >>> obs_clean("", prov_desig)

    >>> os.rmdir("mpcobs")
    """

    rm_files(glob(ram_dir + prov_desig + ".*"))
    rm_files(glob(ram_dir + "mpcobs/" + prov_desig + ".*"))


def final_clean(ram_dir):
    """
    Remove the residuals files used by OrbFit

    Parameters
    ----------
    ram_dir : string
        Path where files are located

    Returns
    -------
    None

    Examples
    --------
    >>> prep_orbitfit("")

    >>> os.path.islink("AST17.bai")
    True
    >>> os.path.islink("AST17.bep")
    True

    >>> final_clean("")

    >>> os.path.exists("AST17.bai")
    False
    >>> os.path.exists("AST17.bep")
    False
    """

    for p in glob(ram_dir + "*.bai"):
        os.unlink(p)

    for p in glob(ram_dir + "*.bep"):
        os.unlink(p)

    rm_files(glob(ram_dir + "*.log"))


def get_orb_and_rms(lines, index_orb, index_rms):
    """
    Read the orbital and the rms at the specified index.

    Parameters
    ----------
    lines : string list
        lines of the .oel files return by OrbFit
    index_orb : integer
        index of the line where is located the orbital elements
    index_rms : integer
        index of the line where is located the rms

    Returns
    -------
    orb_params_rms : float list
        a list containing the 6 keplerian orbital elements and their rms readed from the .oel files

    Examples
    --------

    """
    orb_params = " ".join(lines[index_orb].strip().split()).split(" ")
    if len(lines) > index_rms:
        rms = " ".join(lines[index_rms].strip().split()).split(" ")

        for i_error in range(2, len(rms)):
            tmp_error = rms[i_error]
            if tmp_error[-4] != "E":
                rms[i_error] = tmp_error[:-4] + "E" + tmp_error[-4:]
    else:  # pragma: no cover
        rms = [-1, -1, -1, -1, -1, -1, -1, -1]

    return orb_params[1:] + rms[2:]


def read_oel_lines(lines, second_desig=False):
    """
    Convert the lines from the .oel file generate by OrbFit into list.

    Parameters
    ----------
    lines : string list
        Lines from a .oel file

    Returns
    -------
    orb_params_list : float list
        reference epoch, orbital parameters and their errors

    Examples
    --------
    >>> file = open("fink_fat/test/K21E00A_test.oel", "r")
    >>> lines = file.readlines()
    >>> read_oel_lines(lines)
    [2459274.881182641, '1.2989984390232820E+00', '0.237563404272872', '3.0006189587041', '139.1486265719337', '316.7163361462099', '42.4810617056960', '2.63690E-155', '2.15639E-155', '0.00000E+00', '1.50627E-153', '4.02731E-159', '0.00000E+00']

    >>> file.close()

    >>> file = open("fink_fat/test/K19V00D_K20X01J_test.oel", "r")
    >>> lines = file.readlines()
    >>> read_oel_lines(lines, True)
    [2459752.003580741, 'K19V00D', '5.2086582985661405E+00', '0.041037517072330', '20.4845468192319', '315.8436056618594', '126.7174037870516', '7.0363794445434', '2.35603E-04', '3.46490E-05', '1.04465E-04', '7.88344E-04', '6.53409E-02', '5.72363E-02', 'K20X01J', '5.2122586158728774E+00', '0.043339815768804', '20.4718394776065', '315.8521946724863', '124.1615864980219', '9.5592054339815', '5.43003E-04', '7.69670E-05', '7.18353E-05', '7.45307E-04', '6.50158E-02', '5.84310E-02', 'K19V00D=K20X01J', '5.2324744800289800E+00', '0.047273267080124', '20.4776234947047', '315.7811350105440', '125.9308606763452', '7.9896140760145', '8.45403E-04', '7.46487E-05', '8.08826E-05', '8.42129E-04', '1.31115E-01', '1.17070E-01']

    >>> file.close()
    """
    if len(lines) <= 2:  # pragma: no cover
        raise Exception("Not enough lines")
    ref_mjd = float(lines[9].strip().split()[1])
    # conversion from modified julian date to julian date
    ref_jd = ref_mjd + 2400000.5

    orb_params_rms = get_orb_and_rms(lines, 8, 13)

    if second_desig:
        if len(lines) < 34 or len(lines) < 58:  # pragma: no cover
            raise Exception("Not enough lines")
        first_desig = lines[6].rstrip()
        second_desig = lines[31].rstrip()
        merge_desig = lines[56].rstrip()
        orb_rms_second = get_orb_and_rms(lines, 33, 38)
        orb_rms_merge = get_orb_and_rms(lines, 58, 62)
        orb_params_list = (
            [ref_jd]
            + [first_desig]
            + orb_params_rms
            + [second_desig]
            + orb_rms_second
            + [merge_desig]
            + orb_rms_merge
        )
        return orb_params_list

    orb_params_list = [ref_jd] + orb_params_rms
    return orb_params_list


def read_oel(ram_dir, first_desig, second_desig=None):
    """
    Read the .oel file return by orbfit. This file contains the orbital elements, the reference epoch of the orbit computation and
    the rms of the orbital elements

    Parameters
    ----------
    ram_dir : string
        Path where the files are located
    prov_desig : string
        the provisional designation of the trajectory that triggered the OrbFit process.

    Returns
    -------
    orb_elem : integer list
        A list with the reference epoch first then the orbital elements and finally the rms.

    Examples
    --------
    >>> read_oel("fink_fat/test/", "K21E00A_test")
    [2459274.881182641, '1.2989984390232820E+00', '0.237563404272872', '3.0006189587041', '139.1486265719337', '316.7163361462099', '42.4810617056960', '2.63690E-155', '2.15639E-155', '0.00000E+00', '1.50627E-153', '4.02731E-159', '0.00000E+00']

    >>> read_oel("", "")
    [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]

    >>> read_oel("fink_fat/test/call_orbfit/", "K21H00A")
    [2459345.797868819, '3.1514694062448680E+00', '0.113946062348132', '1.6879159876457', '38.1016474068882', '136.1915246941109', '46.5628893357021', '7.94527E-03', '1.83696E-02', '4.77846E-02', '3.17863E-01', '1.34503E+01', '9.82298E+00']

    >>> read_oel("fink_fat/test/", "K20K00H", "K20R01N")
    [2459752.003580741, 'K20K00H', '3.2770176197522716E+00', '0.489813406860185', '35.4071377670066', '226.6207914399979', '31.7464752385818', '155.1565090050280', '1.87409E-03', '3.06154E-04', '2.61077E-03', '6.34970E-03', '1.72381E-02', '1.47562E-01', 'K20R01N', '3.2383542557794258E+00', '0.481691420534986', '35.4276816300695', '226.5233903480844', '31.5657299503385', '158.2732975448453', '8.93757E-05', '1.30080E-05', '3.24117E-04', '3.15449E-04', '2.50948E-03', '7.41469E-03', 'K20K00H=K20R01N', '3.2349020268784363E+00', '0.482351607052538', '35.4236361556923', '226.5195200701270', '31.4737170165724', '158.4560587571972', '1.15171E-04', '1.79974E-05', '4.67414E-04', '3.35064E-04', '3.15876E-03', '1.04831E-02']

    """
    try:
        if second_desig is None:
            with open(ram_dir + first_desig + ".oel") as file:
                lines = file.readlines()
                return read_oel_lines(lines)
        else:
            with open(ram_dir + first_desig + "_" + second_desig + ".oel") as file:
                lines = file.readlines()
                return read_oel_lines(lines, second_desig=True)

    except FileNotFoundError:
        if second_desig is None:
            return list(np.ones(13, dtype=np.float64) * -1)
        else:  # pragma: no cover
            return list(np.ones(40, dtype=np.float64) * -1)
    except Exception as e:  # pragma: no cover
        if second_desig is not None:
            return list(np.ones(40, dtype=np.float64) * -1)
        print("----")
        print(e)
        print()
        print("ERROR READ OEL FILE: {}".format(first_desig))
        print()
        print(lines)
        print()
        print()
        logging.error(traceback.format_exc())
        print("----")
        return list(np.ones(13, dtype=np.float64) * -1)


def read_rwo(ram_dir, prov_desig, nb_obs):
    """
    Read the .rwo file return by orbfit. This file contains the observations of the trajectories and the goodness of the fit computed by OrbFit.
    Return the chi values for each observations.

    Parameters
    ----------
    ram_dir : string
        Path where files are located
    prov_desig : string
        the provisional designation of the trajectory that triggered the OrbFit process.

    Returns
    -------
    chi : integer list
        The list of all chi values of each observations.

    Examples
    --------
    >>> read_rwo("fink_fat/test/call_orbfit/", "K19V00D_test", 156)
    array([1.5800e+00, 6.1000e-01, 3.0000e-01, 2.0000e-01, 1.3603e+02,
           3.7000e-01, 9.1000e-01, 3.9000e-01, 1.0200e+00, 1.1800e+00,
           3.7970e+02, 1.2840e+01, 2.6970e+01, 5.2242e+02, 5.5700e+00,
           1.6100e+00, 2.1200e+00, 2.5000e+00, 9.7000e-01, 1.3900e+00,
           3.5000e-01, 1.9400e+00, 4.4000e-01, 1.3400e+00, 1.7600e+00,
           2.3000e-01, 1.0100e+00, 1.5000e+00, 1.2400e+00, 9.9000e-01,
           1.3300e+00, 5.2000e-01, 1.2700e+00, 9.0000e-01, 3.3000e-01,
           8.4000e-01, 9.0000e-02, 7.9000e-01, 1.1800e+00, 4.7000e-01,
           1.2400e+00, 3.9000e-01, 5.0000e-02, 1.2500e+00, 1.4700e+00,
           1.2600e+00, 1.0200e+00, 1.2000e+00, 1.8500e+00, 4.1000e-01,
           3.9000e-01, 1.2400e+00, 4.0000e-02, 5.3000e-01, 6.8000e-01,
           1.9700e+00, 4.8000e-01, 8.1000e-01, 1.3400e+00, 3.6000e-01,
           2.8300e+00, 4.3700e+00, 4.2000e-01, 2.2000e-01, 6.9000e-01,
           1.8700e+00, 2.2500e+00, 1.7100e+00, 3.6000e-01, 3.2300e+00,
           8.7000e-01, 6.1000e-01, 1.9000e-01, 9.5000e-01, 1.5500e+00,
           2.0700e+00, 1.7400e+00, 4.6000e-01, 8.0000e-01, 3.4200e+00,
           1.2700e+00, 1.3800e+00, 2.5700e+00, 3.2100e+00, 7.1000e-01,
           1.4000e+00, 3.3500e+00, 5.8000e-01, 5.8000e-01, 2.9000e-01,
           4.0000e-01, 1.4800e+00, 1.6300e+00, 4.3000e+00, 4.5000e-01,
           6.5000e-01, 6.6000e-01, 9.4000e-01, 1.2500e+00, 7.9000e-01,
           1.9900e+00, 2.1000e-01, 2.8100e+00, 3.2600e+00, 5.7000e-01,
           3.6000e+00, 1.2000e+00, 3.8800e+00, 5.0100e+00, 2.6200e+00,
           4.2000e-01, 2.5300e+00, 2.3100e+00, 2.3000e-01, 3.5700e+00,
           1.4900e+00, 2.5000e+00, 1.0700e+00, 1.5700e+00, 1.1800e+00,
           1.3700e+00, 3.9500e+00, 1.8500e+00, 3.4000e+00, 2.1700e+00,
           5.2600e+00, 1.3400e+00, 4.0700e+00, 4.0800e+00, 1.9100e+00,
           2.8300e+00, 3.5400e+00, 3.7200e+00, 1.7000e+00, 1.9900e+00,
           3.4900e+00, 3.7400e+00, 2.9400e+00, 3.6100e+00, 3.6000e+00,
           4.3300e+00, 3.9500e+00, 9.0600e+00, 6.3700e+00, 5.4900e+00,
           5.9200e+00, 6.1100e+00, 6.6400e+00, 6.4100e+00, 7.5700e+00,
           7.5900e+00, 1.1230e+01, 7.1400e+00, 7.2500e+00, 9.1000e+00,
           9.0600e+00, 9.1800e+00], dtype=float32)

    >>> read_rwo("", "", 0)
    []

    >>> read_rwo("fink_fat/test/call_orbfit/", "K19V00D", 4)
    [-1.0, -1.0, -1.0, -1.0]
    """
    try:
        with open(ram_dir + "mpcobs/" + prov_desig + ".rwo") as file:
            lines = file.readlines()

            chi_obs = [obs_l.strip().split(" ")[-3] for obs_l in lines[7:]]

            return np.array(chi_obs).astype(np.float32)
    except FileNotFoundError:
        return list(np.ones(nb_obs, dtype=np.float64) * -1)
    except ValueError:  # pragma: no cover
        return list(np.ones(nb_obs, dtype=np.float64) * -1)
    except Exception as e:  # pragma: no cover
        print("----")
        print(e)
        print()
        print("ERROR READ RWO FILE: {}".format(prov_desig))
        print()
        print(lines)
        print()
        print()
        logging.error(traceback.format_exc())
        print("----")
        return list(np.ones(nb_obs, dtype=np.float64) * -1)


if __name__ == "__main__":  # pragma: no cover
    import sys
    import doctest
    from pandas.testing import assert_frame_equal  # noqa: F401
    import fink_fat.test.test_sample as ts  # noqa: F401
    from unittest import TestCase  # noqa: F401
    import shutil  # noqa: F401
    import filecmp  # noqa: F401
    import stat  # noqa: F401

    if "unittest.util" in __import__("sys").modules:
        # Show full diff in self.assertEqual.
        __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999

    sys.exit(doctest.testmod()[0])
