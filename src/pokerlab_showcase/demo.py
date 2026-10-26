"""Bounded standalone CFR reproduction; no models, datasets or private repository."""
import argparse,json
from pathlib import Path
from .games import Tree
from .cfr import CFR
from .oracle import SequenceOracle,catalog_ev

def run(game,iterations,seed):
 tree=Tree(game);solver=CFR(tree,seed)
 for _ in range(iterations):solver.step()
 policy=solver.average();metric=tree.evaluate(policy);independent=SequenceOracle(tree).evaluate(policy)
 assert max(abs(metric[k]-v) for k,v in independent.items())<1e-8
 assert abs(catalog_ev(tree,policy)-metric['ev_player0'])<1e-8
 return {'game':game,'seed':seed,'iterations':iterations,'information_sets':len(tree.infos),'exact':metric,'independent_LP':independent}

def main():
 p=argparse.ArgumentParser();p.add_argument('--game',choices=['kuhn','leduc','both'],default='both');p.add_argument('--iterations',type=int,default=2000);p.add_argument('--seeds',default='1807');p.add_argument('--output');a=p.parse_args()
 if not 1<=a.iterations<=100000:p.error('Use a bounded iteration count between1 and100000')
 seeds=[int(s) for s in a.seeds.split(',')]
 if len(seeds)>10:p.error('At most10 seeds per invocation')
 result=[run(g,a.iterations,s) for g in (['kuhn','leduc'] if a.game=='both' else [a.game]) for s in seeds];text=json.dumps(result,indent=2)
 if a.output:
  out=Path(a.output)
  if out.exists():raise FileExistsError('Refusing to overwrite completed reproduction output')
  out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding='utf-8')
 print(text)
if __name__=='__main__':main()
