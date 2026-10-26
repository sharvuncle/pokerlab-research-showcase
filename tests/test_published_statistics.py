import json
from pathlib import Path
import numpy as np
from scipy.stats import t

def test_published_interval_recomputes_from_independent_block_differences():
 data=json.loads((Path(__file__).parents[1]/'examples/published_results.json').read_text())
 for row in data['nlhe_v21']['comparisons']:
  d=np.array(row['whole_seed_block_deltas']);assert len(d)==10
  half=t.ppf(.975,9)*d.std(ddof=1)/np.sqrt(10)
  assert abs(d.mean()-row['delta_bb100'])<1e-9
  assert np.max(np.abs(np.array([d.mean()-half,d.mean()+half])-row['paired_t95']))<1e-9
