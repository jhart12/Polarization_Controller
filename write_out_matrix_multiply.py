# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

foutname = 'get_polarization_rotation_matrix.py'

'''
d=[['d11','d12','d13'],['d21','d22','d23'],['d31','d32','d33']]

c=[['c11','c12','c13'],['c21','c22','c23'],['c31','c32','c33']]

b=[['b11','b12','b13'],['b21','b22','b23'],['b31','b32','b33']]

a=[['a11','a12','a13'],['a21','a22','a23'],['a31','a32','a33']]
'''
d = [['np.cos(theta_d)+dx**2*(1-np.cos(theta_d))','dx*dy*(1-np.cos(theta_d))-dz*np.sin(theta_d)','dx*dz*(1-np.cos(theta_d))+dy*np.sin(theta_d)'],
['dx*dy*(1-np.cos(theta_d))+dz*np.sin(theta_d)','np.cos(theta_d)+dy**2*(1-np.cos(theta_d))','dy*dz*(1-np.cos(theta_d))-dx*np.sin(theta_d)'],
['dx*dz*(1-np.cos(theta_d))-dy*np.sin(theta_d)','dy*dz*(1-np.cos(theta_d))+dx*np.sin(theta_d)','np.cos(theta_d)+dz**2*(1-np.cos(theta_d))']]

c = [['np.cos(theta_c)+cx**2*(1-np.cos(theta_c))','cx*cy*(1-np.cos(theta_c))-cz*np.sin(theta_c)','cx*cz*(1-np.cos(theta_c))+cy*np.sin(theta_c)'],
['cx*cy*(1-np.cos(theta_c))+cz*np.sin(theta_c)','np.cos(theta_c)+cy**2*(1-np.cos(theta_c))','cy*cz*(1-np.cos(theta_c))-cx*np.sin(theta_c)'],
['cx*cz*(1-np.cos(theta_c))-cy*np.sin(theta_c)','cy*cz*(1-np.cos(theta_c))+cx*np.sin(theta_c)','np.cos(theta_c)+cz**2*(1-np.cos(theta_c))']]

b = [['np.cos(theta_b)+bx**2*(1-np.cos(theta_b))','bx*by*(1-np.cos(theta_b))-bz*np.sin(theta_b)','bx*bz*(1-np.cos(theta_b))+by*np.sin(theta_b)'],
['bx*by*(1-np.cos(theta_b))+bz*np.sin(theta_b)','np.cos(theta_b)+by**2*(1-np.cos(theta_b))','by*bz*(1-np.cos(theta_b))-bx*np.sin(theta_b)'],
['bx*bz*(1-np.cos(theta_b))-by*np.sin(theta_b)','by*bz*(1-np.cos(theta_b))+bx*np.sin(theta_b)','np.cos(theta_b)+bz**2*(1-np.cos(theta_b))']]

a = [['np.cos(theta_a)+ax**2*(1-np.cos(theta_a))','ax*ay*(1-np.cos(theta_a))-az*np.sin(theta_a)','ax*az*(1-np.cos(theta_a))+ay*np.sin(theta_a)'],
['ax*ay*(1-np.cos(theta_a))+az*np.sin(theta_a)','np.cos(theta_a)+ay**2*(1-np.cos(theta_a))','ay*az*(1-np.cos(theta_a))-ax*np.sin(theta_a)'],
['ax*az*(1-np.cos(theta_a))-ay*np.sin(theta_a)','ay*az*(1-np.cos(theta_a))+ax*np.sin(theta_a)','np.cos(theta_a)+az**2*(1-np.cos(theta_a))']]


out = [['','',''],['','',''],['','','']]
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                for m in range(3):
                    if out[i][m] == '':
                        out[i][m] += '('+a[l][m]+')*('+b[k][l]+')*('+c[j][k]+')*('+d[i][j]+')'
                    else:
                        out[i][m] += '+('+a[l][m]+')*('+b[k][l]+')*('+c[j][k]+')*('+d[i][j]+')'
                        
f = open(foutname,'w')
f.write('import numpy as np\n\n')
f.write('#a_vec is the unit vector of axis of rotation on the Poincare sphere of the first piezoelectric transducer\n')
f.write("#theta_a is the angle that I'd like to rotate about this axis.\n")
f.write('def get_polarization_rotation_matrix(thetas,*vecs):\n')

f.write('\ta_vec = vecs[0]\n')
f.write('\tb_vec = vecs[1]\n')
f.write('\tc_vec = vecs[2]\n')
f.write('\td_vec = vecs[3]\n')

f.write('\tax = a_vec[0]\n')
f.write('\tay = a_vec[1]\n')
f.write('\taz = a_vec[2]\n')
f.write('\tbx = b_vec[0]\n')
f.write('\tby = b_vec[1]\n')
f.write('\tbz = b_vec[2]\n')
f.write('\tcx = c_vec[0]\n')
f.write('\tcy = c_vec[1]\n')
f.write('\tcz = c_vec[2]\n')
f.write('\tdx = d_vec[0]\n')
f.write('\tdy = d_vec[1]\n')
f.write('\tdz = d_vec[2]\n\n')

f.write('\ttheta_a = thetas[0]\n')
f.write('\ttheta_b = thetas[1]\n')
f.write('\ttheta_c = thetas[2]\n')
f.write('\ttheta_d = thetas[3]\n')

f.write('\tR = np.zeros((3,3))\n\n')
for row in range(3):
    for col in range(3):
        f.write('\tR['+str(row)+','+str(col)+'] = '+out[row][col]+'\n')
f.write('\treturn R')
f.close()