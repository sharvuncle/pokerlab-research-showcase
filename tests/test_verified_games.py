import numpy as np
import pytest
from pokerlab_showcase.games import Tree
from pokerlab_showcase.cfr import CFR
from pokerlab_showcase.oracle import SequenceOracle,catalog_ev,kuhn_analytic

@pytest.mark.parametrize('game,infos,nc',[('kuhn',12,11/12),('leduc',288,4.747222222222222)])
def test_uniform_fixtures_and_independent_oracles(game,infos,nc):
 t=Tree(game);assert len(t.infos)==infos;oracle=SequenceOracle(t);p=t.uniform();metric=t.evaluate(p);assert metric['nash_conv']==pytest.approx(nc,abs=1e-10)
 for seed in (7,19):
  p=np.random.default_rng(seed).random(t.legal.shape)*t.legal;p/=p.sum(1,keepdims=True);m=t.evaluate(p);o=oracle.evaluate(p)
  assert abs(catalog_ev(t,p)-m['ev_player0'])<1e-9
  assert all(abs(m[k]-v)<1e-9 for k,v in o.items())
 eq,proof=oracle.equilibrium();assert proof['duality_gap']<1e-8 and t.evaluate(eq)['nash_conv']<1e-8
 assert proof['value']==pytest.approx(-1/18 if game=='kuhn' else -.085606424078,abs=1e-9)

@pytest.mark.parametrize('alpha',[0,.2,1/3])
def test_kuhn_analytic_equilibrium_family(alpha):
 t=Tree('kuhn');p=kuhn_analytic(t,alpha);assert t.ev(p)==pytest.approx(-1/18,abs=1e-12);assert t.evaluate(p)['nash_conv']<1e-10

@pytest.mark.parametrize('game,limit',[('kuhn',.05),('leduc',.15)])
def test_small_CFR_run_improves_over_uniform(game,limit):
 t=Tree(game);c=CFR(t,1807)
 for _ in range(2000):c.step()
 p=c.average();t.validate(p);assert t.evaluate(p)['nash_conv']<limit
 assert np.all(c.regrets[~t.legal]==0)

def test_counterfactual_regret_matches_independent_deviation_value():
 t=Tree('kuhn');c=CFR(t,71);p=c.policy();base=catalog_ev(t,p);reaches=t.reaches(p);c.step()
 for i in range(len(t.infos)):
  node=next(n for n in t.live if t.info[n]==i);owner=t.info_player[i];own=reaches[node,owner]
  for a in np.flatnonzero(t.legal[i]):
   changed=p.copy();changed[i]=0;changed[i,a]=1
   expected=(catalog_ev(t,changed)-base)*(1-2*owner)/own
   assert c.regrets[i,a]==pytest.approx(expected,abs=1e-12)
