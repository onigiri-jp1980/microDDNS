from app.models import ApiKeys,Users,Hosts,Domains

def purge_tables():
    tables = [ApiKeys,Users,Hosts,Domains]
    for table in tables:
        table.delete_table()
        print(f"Deleted table {table.__name__}")

if __name__ == "__main__":
    purge_tables()