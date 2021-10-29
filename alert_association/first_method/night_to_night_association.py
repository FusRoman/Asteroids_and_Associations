from astropy.coordinates.solar_system import get_body_barycentric
import astropy.units as u
from astropy.coordinates import SkyCoord
import pandas as pd
import numpy as np
from collections import Counter
import time as t

from pandas.core.indexes import multi

from intra_night_association import intra_night_association
from intra_night_association import new_trajectory_id_assignation
from intra_night_association import magnitude_association
from intra_night_association import removed_mirrored_association
from intra_night_association import get_n_last_observations_from_trajectories



def night_to_night_separation_association(old_observation, new_observation, separation_criterion):
    """
    Perform night-night association based on the separation between the alerts. The separation criterion was computed by a data analysis on the MPC object.

    Parameters
    ----------
    old_observation : dataframe
        observation of night t-1
    new_observation : dataframe
        observation of night t
    separation_criterion : float
        the separation limit between the alerts to be associated, must be in arcsecond

    Returns
    -------
    left_assoc : dataframe
        Associations are a binary relation with left members and right members, return the left members (from old_observation) of the associations
    right_assoc : dataframe
        return right members (from new_observation) of the associations
    sep2d : list
        return the separation between the associated alerts
    """

    old_observations_coord = SkyCoord(old_observation['ra'], old_observation['dec'], unit=u.degree)
    new_observations_coord = SkyCoord(new_observation['ra'], new_observation['dec'], unit=u.degree)

    new_obs_idx, old_obs_idx, sep2d, _ = old_observations_coord.search_around_sky(new_observations_coord, separation_criterion)

    old_obs_assoc = old_observation.iloc[old_obs_idx]
    new_obs_assoc = new_observation.iloc[new_obs_idx]
    return old_obs_assoc, new_obs_assoc, sep2d

def angle_three_point(a, b, c):
    ba = b - a
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)


def angle_df(x):
    ra_x, dec_x, jd_x = x[1], x[2], x[3]

    ra_y, dec_y, jd_y = x[5], x[6], x[7]

    a = np.array([ra_x[0], dec_x[0]])
    b = np.array([ra_x[1], dec_x[1]])
    c = np.array([ra_y, dec_y])

    jd_x = jd_x[1]

    diff_jd = jd_y - jd_x

    if diff_jd > 1:
        res_angle = angle_three_point(a, b, c) / diff_jd
    else:
        res_angle = angle_three_point(a, b, c)
    
    return res_angle


def cone_search_association(two_last_observations, traj_assoc, new_obs_assoc, angle_criterion):
    # reset the index of the associated members in order to recovered the right rows after the angle filters. 
    traj_assoc = traj_assoc.reset_index(drop=True).reset_index()
    new_obs_assoc = new_obs_assoc.reset_index(drop=True).reset_index()

    # rename the new trajectory_id column to another name in order to give the trajectory_id of the associated trajectories
    # and keep the new trajectory_id
    new_obs_assoc = new_obs_assoc.rename({'trajectory_id' : 'tmp_traj'}, axis=1)
    new_obs_assoc['trajectory_id'] = traj_assoc['trajectory_id']
    
    # get the two last observations of the associated trajectories in order to compute the cone search angle
    two_last = two_last_observations[two_last_observations['trajectory_id'].isin(traj_assoc['trajectory_id'])]

    two_last = two_last.groupby(['trajectory_id']).agg({
        "ra" : list,
        "dec" : list,
        "jd" : list,
        "candid" : lambda x : len(x)
    })
    
    # merge the two last observation with the new observations to be associated
    prep_angle = two_last.merge(new_obs_assoc[['index', 'ra', 'dec', 'jd', 'trajectory_id']], on='trajectory_id')

    # compute the cone search angle
    prep_angle['angle'] = prep_angle.apply(angle_df, axis=1)
    # filter by the physical properties angle
    remain_assoc = prep_angle[prep_angle['angle'] <= angle_criterion]

    # keep only the alerts that match with the angle filter
    traj_assoc = traj_assoc.loc[remain_assoc['index'].values]
    new_obs_assoc = new_obs_assoc.loc[remain_assoc['index'].values]

    return traj_assoc.drop(['index'], axis=1), new_obs_assoc.drop(['index'], axis=1)



def trajectory_tracklets_associations(two_last_observations, tracklets_extremity, sep_criterion, mag_criterion_same_fid, mag_criterion_diff_fid, angle_criterion): 
    # get the last obeservations of the trajectories to perform the associations 
    last_traj_obs = two_last_observations.groupby(['trajectory_id']).last().reset_index()

    # night_to_night association between the last observations from the trajectories and the first tracklets observations of the next night
    traj_assoc, new_obs_assoc, _ = night_to_night_separation_association(last_traj_obs, tracklets_extremity, sep_criterion)
    traj_assoc, new_obs_assoc = magnitude_association(traj_assoc, new_obs_assoc, mag_criterion_same_fid, mag_criterion_diff_fid)
    traj_assoc, new_obs_assoc = removed_mirrored_association(traj_assoc, new_obs_assoc)
    
    if len(traj_assoc) != 0:
        return cone_search_association(two_last_observations, traj_assoc, new_obs_assoc, angle_criterion)
    else:
        return traj_assoc, new_obs_assoc


def assign_new_trajectory_id_to_new_tracklets(new_obs_to_be_assign, traj_next_night):
    for _, rows in new_obs_to_be_assign.iterrows():
        traj_id = rows['tmp_traj']

        # get all the alerts associated with this first observations 
        mask = traj_next_night.trajectory_id.apply(lambda x: np.any(x == traj_id))
        multi_traj = traj_next_night[mask.values]
        # change the trajectory_id of the associated alerts with the original trajectory_id of the associated trajectory
        traj_next_night.loc[multi_traj.index.values, 'trajectory_id'] = [[rows['trajectory_id']]]
    
    return traj_next_night

def trajectory_id_management(traj_left, traj_right, traj_next_night, trajectory_df):
    traj_left = traj_left.reset_index(drop=True).reset_index()
    traj_right = traj_right.reset_index(drop=True)

    # detect the multiple associations with the left members (trajectories)
    multiple_assoc = traj_left.groupby(['trajectory_id']).agg({
        "index" : list,
        "candid" : lambda x : len(x)
    })

    # get the associations not involved in a multiple associations
    single_obs = traj_right.loc[multiple_assoc[multiple_assoc['candid'] == 1].explode(['index'])['index'].values]

    # get the tracklets extremity implies in the multiple associations
    multiple_obs = traj_right.loc[multiple_assoc[multiple_assoc['candid'] > 1].explode(['index'])['index'].values]
    
    # get the first occurence in the multiple associations
    first_occur = multiple_obs[multiple_obs.duplicated(['trajectory_id'])]

    # get the others occurences
    other_occur = multiple_obs[~multiple_obs.duplicated(['trajectory_id'])]
    

    # add the trajectory_id of the all other occurences to the list of trajectory_id of the associated trajectories
    for _, rows in other_occur.iterrows():
        traj_id = rows['trajectory_id']

        # get all rows of the associated trajectory 
        mask = trajectory_df.trajectory_id.apply(lambda x: any(i == traj_id for i in x))
        multi_traj = trajectory_df[mask]

        # get the trajectory id list of the associated trajectory
        multi_traj_id = multi_traj['trajectory_id'].values
        # duplicates the new trajectory_id which will be added to the trajectory id list
        new_traj_id = [[rows['tmp_traj']] for _ in range(len(multi_traj))]

        # concatenate the trajectory id list with the new trajectory id and add this new list to the trajectory_id columns of the associated trajectory
        trajectory_df.loc[multi_traj.index.values, 'trajectory_id'] = [el1 + el2 for el1, el2 in zip(multi_traj_id, new_traj_id)]


    traj_next_night = assign_new_trajectory_id_to_new_tracklets(first_occur, traj_next_night)
    traj_next_night = assign_new_trajectory_id_to_new_tracklets(single_obs, traj_next_night)

    other_occur = other_occur.drop(['trajectory_id'], axis=1).rename({'tmp_traj' : 'trajectory_id'}, axis=1)
    first_occur = first_occur.drop(['tmp_traj'], axis=1)

    # add all the new observations in the trajectory dataframe with the right trajectory_id
    return pd.concat([trajectory_df, first_occur, other_occur, single_obs.drop(['tmp_traj'], axis=1)]), traj_next_night



def night_to_night_association(trajectory_df, old_observation, new_observation, sep_criterion=0.43*u.degree, mag_criterion_same_fid=1.36, mag_criterion_diff_fid=1.31, angle_criterion=29.52):
    # get the last two observations for each trajectories
    two_last_observation_trajectory = get_n_last_observations_from_trajectories(trajectory_df, 2)

    # get the maximum trajectory_id and increment it to return the new trajectory_id baseline
    last_trajectory_id = np.max(trajectory_df.explode(['trajectory_id'])['trajectory_id'].values) + 1

    # intra-night association of the new observations
    new_left, new_right, _ = intra_night_association(new_observation)
    traj_next_night = new_trajectory_id_assignation(new_left, new_right, last_trajectory_id)


    # get the oldest extremity of the new tracklets to perform associations with the youngest observations in the trajectories 
    tracklets_extremity = get_n_last_observations_from_trajectories(traj_next_night, 1, False)  

    # trajectory association with the new tracklets
    traj_left, traj_extrimity_associated = trajectory_tracklets_associations(
        two_last_observation_trajectory,
        tracklets_extremity,
        sep_criterion,
        mag_criterion_same_fid,
        mag_criterion_diff_fid,
        angle_criterion
        )

    # remove the tracklets extremity implies in an associations
    traj_next_night = traj_next_night[~traj_next_night['candid'].isin(traj_extrimity_associated['candid'])].reset_index(drop=True)
    tracklets_extremity = tracklets_extremity[~tracklets_extremity['candid'].isin(traj_extrimity_associated['candid'])].reset_index(drop=True)

    trajectory_df, traj_next_night = trajectory_id_management(traj_left, traj_extrimity_associated, traj_next_night, trajectory_df)

    return trajectory_df

    

if __name__ == "__main__":
    df_sso = pd.read_pickle("../../data/month=03")

    df_sso = df_sso.drop_duplicates(['candid'])

    all_night = np.unique(df_sso['nid'])
    print(all_night)

    for i in range(len(all_night)-1):
        t_before = t.time()
        n1 = all_night[i]
        n2 = all_night[i+1]
        if n2 - n1 == 1:
            print(n1)
            print(n2)
            print()
            df_night1 = df_sso[(df_sso['nid'] == 1521) & (df_sso['fink_class'] == 'Solar System MPC')]
            df_night2 = df_sso[(df_sso['nid'] == 1522) & (df_sso['fink_class'] == 'Solar System MPC')]

            left, right, _ = intra_night_association(df_night1)
            traj_df = new_trajectory_id_assignation(left, right, 0)
            traj_df = traj_df.reset_index(drop=True)

            old_observation = df_night1[~df_night1['candid'].isin(traj_df['candid'])]

            traj_df = night_to_night_association(traj_df, old_observation, df_night2)
        print("elapsed time: {}".format(t.time() - t_before))
        print()
        print()
        break
        
        
        