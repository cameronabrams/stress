import numpy as np
import argparse as ap
import matplotlib.pyplot as plt

def myacfplot (lags,acf,outfile='plot.png',**kwargs):
    fig,ax=plt.subplots(1,1)
    ax.set_xlabel('lag (ps)')
    ax.set_ylabel('C(t) (bar$^2$)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.scatter(lags[0:len(acf)],acf,marker='.',alpha=0.3,
                color='blue',facecolors='none',s=5)
    plt.savefig(outfile,bbox_inches='tight')
    print('Generated {:s}.'.format(outfile))

if __name__ == '__main__':
    parser=ap.ArgumentParser()
    parser.add_argument('acffile',type=str,help='input acf file')
    parser.add_argument('-op',type=str,default='acf.png')
    args=parser.parse_args()
    print('Reading {:s}...'.format(args.acffile))
    lags,acf=np.loadtxt(args.acffile,unpack=True)
    print('Generating plot in {:s}...'.format(args.op))
    myacfplot(lags,acf,args.op)
