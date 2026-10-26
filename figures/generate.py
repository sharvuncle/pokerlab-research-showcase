"""Build figures solely from reviewed aggregate facts; optional matplotlib dependency."""
import json
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'svg.fonttype':'none','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
def main():
 d=json.loads((ROOT/'examples/published_results.json').read_text());fig,axs=plt.subplots(1,2,figsize=(10,3.8),layout='constrained')
 for ax,game in zip(axs,('kuhn','leduc')):
  for seed,color,style in zip((1807,1829,1843),('#174a7e','#4e78a0','#8aa3bc'),('-','--',':')):
   rows=[x for x in d['toy_convergence'][game] if x['seed']==seed];ax.loglog([x['iterations'] for x in rows],[x['nash_conv'] for x in rows],label=str(seed),color=color,linestyle=style)
  ax.set(title=game.capitalize(),xlabel='CFR iterations',ylabel='NashConv (ante chips / hand)');ax.grid(alpha=.15);ax.legend(title='Initialization seed',frameon=False)
 fig.suptitle('Verified tabular CFR: three recorded initialization seeds');fig.savefig(ROOT/'figures/cfr_convergence.svg');fig.savefig(ROOT/'figures/cfr_convergence.png',dpi=150);plt.close(fig)
 groups=('all','2','3','4','5','6');rows=[next(x for x in d['nlhe_v21']['comparisons'] if x['group']==g) for g in groups];mean=np.array([x['delta_bb100'] for x in rows]);lo=np.array([x['paired_t95'][0] for x in rows]);hi=np.array([x['paired_t95'][1] for x in rows]);fig,ax=plt.subplots(figsize=(8,4),layout='constrained');ax.errorbar(mean,np.arange(len(rows)),xerr=np.array([mean-lo,hi-mean]),fmt='o',color='#174a7e',capsize=4);ax.axvline(0,color='gray',lw=1);ax.set(yticks=np.arange(len(rows)),yticklabels=['Overall']+[g+' players' for g in groups[1:]],xlabel='Aggression minus reference (bb / 100 hands)',title='v2.1 matched NLHE improvement; whole-block t95 intervals');ax.invert_yaxis();fig.savefig(ROOT/'figures/nlhe_improvement.svg');fig.savefig(ROOT/'figures/nlhe_improvement.png',dpi=150);plt.close(fig)
 fig,axs=plt.subplots(1,2,figsize=(10,3.8),layout='constrained')
 for ax,group,label in zip(axs,('all','6'),('Overall','Six players')):
  for offset,mode,color,name in ((-.18,'reference','#a4a9ae','Original reference'),(.18,'aggression','#174a7e','Aggression')):
   row=next(x for x in d['nlhe_v21']['behavior_and_risk'] if x['group']==group and x['policy']==mode);ax.bar(np.arange(2)+offset,[100*row['rates'][k] for k in ('full_stack_loss_rate','large_pot_loss_rate')],width=.35,label=name,color=color)
  ax.set(title=label,xticks=[0,1],xticklabels=['Full starting-stack loss','Net loss >=10BB'],ylabel='Observed hands (%)');ax.legend(frameon=False)
 fig.suptitle('Aggression increased loss risk in the simulated suite');fig.savefig(ROOT/'figures/loss_risk.svg');fig.savefig(ROOT/'figures/loss_risk.png',dpi=150);plt.close(fig)
if __name__=='__main__':main()
