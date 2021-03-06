"""
This program reads in all six off-diagonal stress tensor components vs time
generated by 'gmx energy' from an *.edr file, and computes the autocovariance
of each, saves each autocovariance to an output file, and plots each one.

Cameron Abrams cfa22@drexel.edu
"""

import numpy as np
import argparse as ap
import statsmodels.tsa.api as tsa
from myacfplot import myacfplot

if __name__ == '__main__':
    parser=ap.ArgumentParser()
    parser.add_argument('xvgfile', metavar='xvg', type=str,
                        help='xvgfile')
    parser.add_argument('-op',type=str,default='acov-avg6.png',help='output plot image file')
    parser.add_argument('-od',type=str,default='acov-avg6.dat',help='output data file')
    args=parser.parse_args()

    print('Reading {:s}...'.format(args.xvgfile))
    t,xy,xz,yx,yz,zx,zy=np.loadtxt(args.xvgfile,comments=['#','@'],unpack=True)
    print('{:s} has {:d} lines'.format(args.xvgfile,len(t)))

    dat=np.array([[xy,yx],[xz,zx],[yz,zy]])
    labels=[['xy','yx'],['xz','zx'],['yz','zy']]
    started=False
    count=0
    for r in range(3):
        for c in range(2):
            this_acf=tsa.stattools.acovf(dat[r][c],fft=True)
            np.savetxt('acov{:s}.dat'.format(labels[r][c]),np.array([t[0:len(this_acf)],this_acf]).T)
            print('Wrote acov{:s}.dat.'.format(labels[r][c]))
            if not started:
                acf=this_acf.copy()
                started=True
            else:
                acf+=this_acf
            count+=1
    acf/=count
    np.savetxt(args.od,np.array([t[0:len(acf)],acf]).T,header='lag(ps) acov(bar^2)')
    print('Wrote {:d}-fold average to {:s}'.format(count,args.od))
    print('Plotting to {:s}...'.format(args.op))
    myacfplot(t,acf,args.op)
