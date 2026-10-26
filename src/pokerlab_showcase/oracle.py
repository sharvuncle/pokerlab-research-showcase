"""Independent sequence-form LP oracle; never used in CFR updates."""
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix,hstack
from scipy.optimize import linprog


class SequenceOracle:
 def __init__(self,t):
  self.tree=t;self.maps=[];self.flows=[];self.rhs=[]
  for player in (0,1):
   infos=np.flatnonzero(t.info_player==player);seq={};nextid=1
   for i in infos:
    for a in np.flatnonzero(t.legal[i]):seq[(int(i),int(a))]=nextid;nextid+=1
   rr=[0];cc=[0];vv=[1.];b=np.zeros(len(infos)+1);b[0]=1
   for row,i in enumerate(infos,1):
    parent=t.parents[i];rr.append(row);cc.append(0 if parent is None else seq[parent]);vv.append(-1.)
    for a in np.flatnonzero(t.legal[i]):rr.append(row);cc.append(seq[(int(i),int(a))]);vv.append(1.)
   self.maps.append(seq);self.flows.append(coo_matrix((vv,(rr,cc)),shape=(len(b),nextid)).tocsr());self.rhs.append(b)
  rows=[];cols=[];values=[]
  def traverse(node,seq0,seq1,prob):
   owner=t.owner[node]
   if owner<0:rows.append(seq0);cols.append(seq1);values.append(prob*t.utility[node]);return
   info=int(t.info[node])
   for a in np.flatnonzero(t.legal[info]):
    ns=self.maps[owner][(info,int(a))];traverse(t.children[node,a],ns if owner==0 else seq0,ns if owner==1 else seq1,prob)
  for node,prob in zip(t.roots,t.root_prob):traverse(node,0,0,float(prob))
  self.payoff=coo_matrix((values,(rows,cols)),shape=(self.flows[0].shape[1],self.flows[1].shape[1])).tocsr()
 def realization(self,p,player):
  x=np.zeros(self.flows[player].shape[1]);x[0]=1
  for i in sorted(np.flatnonzero(self.tree.info_player==player),key=lambda i:len(self.tree.infos[i][3])+len(self.tree.infos[i][4])):
   parent=self.tree.parents[i];reach=1 if parent is None else x[self.maps[player][parent]]
   for a in np.flatnonzero(self.tree.legal[i]):x[self.maps[player][(int(i),int(a))]]=reach*p[i,a]
  assert np.max(np.abs(self.flows[player]@x-self.rhs[player]))<1e-9
  return x
 def behavior(self,x,player):
  p=self.tree.uniform()
  for i in np.flatnonzero(self.tree.info_player==player):
   legal=np.flatnonzero(self.tree.legal[i]);w=np.array([x[self.maps[player][(int(i),int(a))]] for a in legal]);total=w.sum()
   if total>1e-12:p[i]=0;p[i,legal]=np.maximum(w,0)/np.maximum(w,0).sum()
  return p
 @staticmethod
 def solve_maximin(A,E,e,F,f):
  nx=A.shape[0];ny=len(f);c=np.concatenate([np.zeros(nx),-f]);ub=hstack([-A.T,F.T]).tocsr();eq=hstack([E,csr_matrix((len(e),ny))]).tocsr()
  r=linprog(c,A_ub=ub,b_ub=np.zeros(A.shape[1]),A_eq=eq,b_eq=e,bounds=[(0,None)]*nx+[(None,None)]*ny,method='highs')
  if not r.success:raise RuntimeError('Sequence-form minimax failed: '+r.message)
  return -float(r.fun),r.x[:nx]
 def equilibrium(self):
  A=self.payoff;E,F=self.flows;e,f=self.rhs;v0,x=self.solve_maximin(A,E,e,F,f);v1,y=self.solve_maximin(-A.T,F,f,E,e);p=self.behavior(x,0);q=self.behavior(y,1);p[self.tree.info_player==1]=q[self.tree.info_player==1]
  return p,{'value':v0,'opposite_value':v1,'duality_gap':abs(v0+v1),'realization_sizes':[len(x),len(y)],'flow_constraints':[len(e),len(f)]}
 def evaluate(self,p):
  x=self.realization(p,0);y=self.realization(p,1);br=[]
  for player,c in ((0,-self.payoff@y),(1,self.payoff.T@x)):
   r=linprog(c,A_eq=self.flows[player],b_eq=self.rhs[player],bounds=(0,None),method='highs')
   if not r.success:raise RuntimeError('Best response LP failed')
   br.append(-float(r.fun))
  return {'ev_player0':float(x@self.payoff@y),'br0_value':br[0],'br1_value':br[1],'nash_conv':sum(br),'exploitability':sum(br)/2}


def catalog_ev(tree,policy):
 """Separate terminal-history/physical-deck enumeration, no advance/payoff tree."""
 from itertools import permutations
 catalogs={'kuhn':[((1,1),None,0),((2,1),None,1),((2,0),1,0),((1,2,1),None,1),((1,2,0),-1,0)],
 'leduc':[((1,1),None,0),((2,1),None,1),((2,2,1),None,2),((1,2,1),None,1),((1,2,2,1),None,2),((2,0),1,0),((2,2,0),-1,1),((1,2,0),-1,0),((1,2,2,0),1,1)]}
 game=tree.game;physical=list(permutations(range(3 if game=='kuhn' else 6),2 if game=='kuhn' else 3));total=0.
 def probability(private,board,first,sequence):
  value=1.
  for j,a in enumerate(sequence):
   actor=j%2;key=(actor,private[actor],board,first,sequence[:j]);value*=policy[tree.info_index[key],a]
  return value
 for deal in physical:
  private=deal if game=='kuhn' else tuple(c//2 for c in deal[:2]);board=-1 if game=='kuhn' else deal[2]//2
  score=lambda rank:(rank==board,rank) if game=='leduc' else (False,rank)
  sign=0 if score(private[0])==score(private[1]) else (1 if score(private[0])>score(private[1]) else -1)
  value=0.
  for history,fold,invest in catalogs[game]:
   mass=probability(private,-1,(),history)
   if fold is not None:value+=mass*fold*(1+(1 if game=='kuhn' else 2)*invest)
   elif game=='kuhn':value+=mass*sign*(1+invest)
   else:
    base=1+2*invest
    for second,fold2,invest2 in catalogs['leduc']:
     p=mass*probability(private,board,history,second);value+=p*(sign*(base+4*invest2) if fold2 is None else fold2*(base+4*invest2))
  total+=value/len(physical)
 return total


def kuhn_analytic(tree,alpha=1/3):
 if tree.game!='kuhn' or not 0<=alpha<=1/3:raise ValueError('Kuhn equilibrium family only')
 p=tree.uniform()
 for i,(actor,card,board,first,h) in enumerate(tree.infos):
  if actor==0 and not h:raise_rate=(alpha,0,3*alpha)[card];p[i]=[0,1-raise_rate,raise_rate]
  elif actor==0:call=(0,alpha+1/3,1)[card];p[i]=[1-call,call,0]
  elif h==(1,):raise_rate=(1/3,0,1)[card];p[i]=[0,1-raise_rate,raise_rate]
  else:call=(0,1/3,1)[card];p[i]=[1-call,call,0]
 tree.validate(p);return p
