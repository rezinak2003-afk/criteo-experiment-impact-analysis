import duckdb

def test_consistency_rule_catches_bad_rows():
    con = duckdb.connect()
    con.execute("CREATE TABLE events AS SELECT * FROM (VALUES (1,1,1),(1,0,1),(0,1,0)) t(treatment, visit, conversion)")
    bad = con.execute("SELECT COUNT(*) FROM events WHERE conversion=1 AND visit=0").fetchone()[0]
    assert bad == 1
