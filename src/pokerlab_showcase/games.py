"""Explicit ante-chip Kuhn/Leduc rules and finite perfect-recall game tree."""
from dataclasses import dataclass
from itertools import permutations
from collections import Counter
import numpy as np


@dataclass(frozen=True)
class State:
 street:int=0
 actor:int=0
 contributions:tuple=(1,1)
 bets:tuple=(0,0)
 history:tuple=()
 first:tuple=()
 raises:int=0
 checks:int=0
 payoff:float|None=None


def worlds(game):
 if game=='kuhn':return [(a,b,-1,1/6) for a,b in permutations(range(3),2)]
 if game!='leduc':raise ValueError('Unknown reduced game')
 # Independent physical deck labels; collapse only payoff-irrelevant suits.
 counts=Counter(tuple(card//2 for card in deal) for deal in permutations(range(6),3))
 return [(*ranks,n/120) for ranks,n in sorted(counts.items())]


def actions(game,s):
 if s.payoff is not None:return ()
 needed=max(s.bets)-s.bets[s.actor];cap=1 if game=='kuhn' else 2
 return tuple(([0] if needed else [])+[1]+([2] if s.raises<cap else []))


def advance(game,s,a,world):
 if a not in actions(game,s):raise ValueError('Illegal reduced-game action')
 p=s.actor;hist=s.history+(a,);amount=max(s.bets)-s.bets[p];con=list(s.contributions);bets=list(s.bets)
 if a==0:return State(**{**s.__dict__,'history':hist,'payoff':float(-con[0] if p==0 else con[1])})
 if a==2:
  payment=amount+(1 if game=='kuhn' else (2 if s.street==0 else 4));con[p]+=payment;bets[p]+=payment
  return State(s.street,1-p,tuple(con),tuple(bets),hist,s.first,s.raises+1,0)
 con[p]+=amount;bets[p]+=amount
 if amount or s.checks==1:
  if game=='leduc' and s.street==0:return State(1,0,tuple(con),(0,0),(),hist,0,0)
  left,right,board,_=world
  l=(left==board,left) if game=='leduc' else (False,left);r=(right==board,right) if game=='leduc' else (False,right)
  payoff=0. if l==r else float(con[1] if l>r else -con[0])
  return State(s.street,1-p,tuple(con),tuple(bets),hist,s.first,s.raises,s.checks,payoff)
 return State(s.street,1-p,tuple(con),tuple(bets),hist,s.first,s.raises,s.checks+1)


def information(s,world):
 return (s.actor,world[s.actor],world[2] if s.street else -1,s.first,s.history)


class Tree:
 def __init__(self,game):
  self.game=game;self.infos=[];self.info_index={};nodes=[];roots=[];self.parents=[];self.legal=[];self.info_player=[]
  def add(s,w,depth,seq):
   idx=len(nodes);nodes.append(None)
   if s.payoff is not None:nodes[idx]=(-1,-1,[-1]*3,s.payoff,depth,w[3]);return idx
   key=information(s,w);owner=s.actor;legal=actions(game,s)
   if key not in self.info_index:
    i=len(self.infos);self.info_index[key]=i;self.infos.append(key);self.parents.append(seq[owner]);self.legal.append([a in legal for a in range(3)]);self.info_player.append(owner)
   i=self.info_index[key];assert self.parents[i]==seq[owner] and self.legal[i]==[a in legal for a in range(3)],'Perfect recall/legal actions violated'
   children=[-1]*3
   for a in legal:
    ns=list(seq);ns[owner]=(i,a);children[a]=add(advance(game,s,a,w),w,depth+1,tuple(ns))
   nodes[idx]=(owner,i,children,0.,depth,w[3]);return idx
  self.worlds=worlds(game)
  for w in self.worlds:roots.append(add(State(),w,0,(None,None)))
  self.owner=np.array([n[0] for n in nodes]);self.info=np.array([n[1] for n in nodes]);self.children=np.array([n[2] for n in nodes]);self.utility=np.array([n[3] for n in nodes]);self.depth=np.array([n[4] for n in nodes]);self.chance=np.array([n[5] for n in nodes]);self.roots=np.array(roots);self.root_prob=np.array([w[3] for w in self.worlds]);self.legal=np.array(self.legal);self.info_player=np.array(self.info_player)
  self.live=np.flatnonzero(self.owner>=0);self.levels=[self.live[self.depth[self.live]==d] for d in range(int(self.depth.max())+1)];assert abs(self.root_prob.sum()-1)<1e-12
 def uniform(self):return self.legal/self.legal.sum(1,keepdims=True)
 def validate(self,p):
  if p.shape!=self.legal.shape or not np.isfinite(p).all() or np.any(p<0) or np.any(p[~self.legal]!=0) or not np.allclose(p.sum(1),1):raise ValueError('Invalid information-set policy')
 def values(self,p):
  self.validate(p);v=self.utility.copy()
  for ids in reversed(self.levels):
   if len(ids):v[ids]=(p[self.info[ids]]*v[self.children[ids]]).sum(1)
  return v
 def ev(self,p):return float(self.root_prob@self.values(p)[self.roots])
 def reaches(self,p):
  r=np.zeros((len(self.owner),2));r[self.roots]=1
  for ids in self.levels:
   if not len(ids):continue
   for a in range(3):
    valid=self.children[ids,a]>=0;ps=ids[valid];cs=self.children[ps,a];r[cs]=r[ps];r[cs,self.owner[ps]]*=p[self.info[ps],a]
  return r
 def best_response(self,p,player):
  """One action per infoset, maximizing chance*opponent weighted values."""
  reach=self.reaches(p);cf=self.chance*reach[:,1-player];v=self.utility.copy()*(1 if player==0 else -1);q=p.copy()
  for ids in reversed(self.levels):
   if not len(ids):continue
   mine=ids[self.owner[ids]==player];theirs=ids[self.owner[ids]!=player]
   if len(theirs):v[theirs]=(p[self.info[theirs]]*v[self.children[theirs]]).sum(1)
   if len(mine):
    infos=np.unique(self.info[mine]);scores=np.stack([np.bincount(self.info[mine],weights=cf[mine]*v[self.children[mine,a]]*self.legal[self.info[mine],a],minlength=len(self.infos)) for a in range(3)],axis=1);scores[~self.legal]=-np.inf;best=scores[infos].argmax(1);q[infos]=0;q[infos,best]=1;v[mine]=(q[self.info[mine]]*v[self.children[mine]]).sum(1)
  return float(self.root_prob@v[self.roots]),q
 def evaluate(self,p):
  value=self.ev(p);br0,_=self.best_response(p,0);br1,_=self.best_response(p,1);nc=br0+br1
  assert nc>=-1e-10
  return {'ev_player0':value,'br0_value':br0,'br1_value':br1,'nash_conv':max(0.,nc),'exploitability':max(0.,nc)/2,'units':'ante chips per hand, exact full game'}


def features(key):
 owner,private,board,first,current=key;x=np.zeros(41,dtype=np.float32);x[owner]=1;x[2+private]=1;x[5+board+1]=1
 for r,hist in enumerate((first,current)):
  for j in range(4):x[9+r*16+j*4+(hist[j]+1 if j<len(hist) else 0)]=1
 return x
