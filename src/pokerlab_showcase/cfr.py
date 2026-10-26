"""Full-tree simultaneous vanilla CFR, separate from evaluation/oracle code."""
import numpy as np


class CFR:
 def __init__(self,tree,seed):
  self.tree=tree;self.regrets=np.zeros(tree.legal.shape);self.strategy_sum=np.zeros(tree.legal.shape);self.iterations=0;self.rng=np.random.default_rng(seed)
  self.initial=self.rng.random(tree.legal.shape)*tree.legal;self.initial/=self.initial.sum(1,keepdims=True)
 def policy(self):
  if not self.iterations:return self.initial.copy()
  positive=np.maximum(self.regrets,0)*self.tree.legal;total=positive.sum(1,keepdims=True)
  return np.divide(positive,total,out=self.tree.uniform(),where=total>0)
 def average(self):
  total=self.strategy_sum.sum(1,keepdims=True)
  return np.divide(self.strategy_sum,total,out=self.tree.uniform(),where=total>0)
 def step(self):
  t=self.tree;p=self.policy();reach=t.reaches(p);v=t.values(p);ids=t.live;infos=t.info[ids];owners=t.owner[ids];cf=t.chance[ids]*reach[ids,1-owners];own=t.chance[ids]*reach[ids,owners];sign=1-2*owners
  for a in range(3):
   legal=t.legal[infos,a];reg=cf*sign*(v[t.children[ids,a]]-v[ids])*legal
   self.regrets[:,a]+=np.bincount(infos,weights=reg,minlength=len(t.infos))
   self.strategy_sum[:,a]+=np.bincount(infos,weights=own*p[infos,a],minlength=len(t.infos))
  self.iterations+=1
