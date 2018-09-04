import numpy as np

#vecs is a tuple of unit vectors of axes of rotation on the Poincare sphere of the first piezoelectric transducer
#thetas is a tuple of angles that I'd like to rotate about the axes.
def get_single_rotation_matrix(theta,vec):
    ux = vec[0]
    uy = vec[1]
    uz = vec[2]

    R = np.zeros((3,3))

    R[0,0] = np.cos(theta) + ux*ux*(1-np.cos(theta))
    R[0,1] = ux*uy*(1-np.cos(theta)) - uz*np.sin(theta)
    R[0,2] = ux*uz*(1-np.cos(theta)) + uy*np.sin(theta)
    R[1,0] = uy*ux*(1-np.cos(theta)) + uz*np.sin(theta)
    R[1,1] = np.cos(theta) + uy*uy*(1-np.cos(theta))
    R[1,2] = uy*uz*(1-np.cos(theta)) - ux*np.sin(theta)
    R[2,0] = ux*uz*(1-np.cos(theta)) - uy*np.sin(theta)
    R[2,1] = uy*uz*(1-np.cos(theta)) + ux*np.sin(theta)
    R[2,2] = np.cos(theta) + uz*uz*(1-np.cos(theta))
    return R
