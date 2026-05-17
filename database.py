from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY


print(repr(SUPABASE_URL))
print(repr(SUPABASE_KEY))

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)