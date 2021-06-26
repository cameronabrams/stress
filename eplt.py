
import matplotlib.pyplot as plt
import numpy as np
import argparse as ap

Pa_per_bar = 1.e5 # Pascals per bar
k_kJmolK = 8.3144621e-3 # Boltzmann constant in kJ/mol/K
bar_kJmolnm3 = 16.6 # bar per (kJ/mol/m^3)

parser=ap.ArgumentParser()
parser.add_argument('f',type=str,default='e.dat',nargs='+')
parser.add_argument('-ct',type=str,default='')
parser.add_argument('-T',type=float,default=600)
parser.add_argument('-L',type=float,default=8.16018)
parser.add_argument('-op',type=str,default='E=3Gstar.png')

args=parser.parse_args()
V_nm3 = args.L*args.L*args.L # volume in nm^3
kT_kJmol = args.T*k_kJmolK # kT in kJ/mol
fac_bar = V_nm3/kT_kJmol/bar_kJmolnm3 # V/kT in bar^{-1}

fig,ax=plt.subplots(1,1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('frequency (1/s)')
started=False
count=0
if len(args.f)>1:
    print('Averaging {:d} files.'.format(len(args.f)))
for file in args.f:
    thisid,this_freq_ps,this_e_Pa=np.loadtxt(file,unpack=True)
    if not started:
        freq_ps=this_freq_ps
        e_Pa=this_e_Pa
        started=True
    else:
        e_Pa+=this_e_Pa
    count+=1
e_Pa/=count

# if an autocovariance (bar^2 vs ps) is specified, read it in and plot using the
# Alvarez trick (i.e., plot G(t) vs 1/sqrt(2pi)t)
if args.ct!='':
    ax.set_ylabel("$G^*(\omega)$, $G(1/\sqrt{2\pi}t)$ (Pa)")
    # plot as G*(omega), not E, with omega [=] 1/s, not 1/ps
    ax.scatter(freq_ps*1.e12,e_Pa/3,marker='o',alpha=0.3,color='blue',facecolors='none',label='$G^*$')
    lags,ct=np.loadtxt(args.ct,unpack=True)
    invlags=1./np.sqrt(2*np.pi)*np.reciprocal(lags)
    # plot G(t) in Pa; C(t) is in bar^2
    ax.scatter(invlags[::100]*1.e12,fac_bar*1.e5*ct[::100],marker='o',alpha=0.2,color='red',facecolors='none',label='$G(t)$ vs $1/(\sqrt{2\pi}t)$')
    ax.legend()
else:
    ax.set_ylabel('$E = 3G^*$ (Pa)')
    ax.scatter(freq_ps*1.e12,e_Pa,marker='o',alpha=0.3,color='blue',facecolors='none',label='$G^*$')

plt.savefig(args.op,bbox_inches='tight')