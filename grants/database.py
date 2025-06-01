import oracledb

conn = oracledb.connect(
    user="admin",
    password="Bsn9QKNzaf64xdp",
    dsn="ctmhdefxnd2sbehk_high",
    config_dir=r"C:\Users\OK\Downloads\mydb",
    wallet_location=r"C:\Users\OK\Downloads\mydb",
    wallet_password="Directoria!12"
)

def search_grants(query):
    cur = conn.cursor()
    sql = """
    SELECT id, name, grantor FROM grants
    WHERE LOWER(name) LIKE :q OR LOWER(facts) LIKE :q
    """
    cur.execute(sql, {"q": f"%{query.lower()}%"})
    return cur.fetchall()

def get_grant_by_id(grant_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM grants WHERE id = :id", {"id": grant_id})
    return cur.fetchone()
