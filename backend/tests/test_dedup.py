from app.utils.ingest import compute_dedup_key

def test_dedup_key():
    k1 = compute_dedup_key('idea', 'icp')
    k2 = compute_dedup_key('Idea', 'ICP')
    assert k1 == k2
