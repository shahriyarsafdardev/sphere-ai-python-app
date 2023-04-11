import re
import openai
import psycopg2
import environ
from user.models.postgres_reference import PostgresReference

env = environ.Env()
environ.Env.read_env()
openai.api_key = env('OPENAI_API_KEY')


def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.5
    )['choices'][0]['message']['content'].strip()
    return response


def parsed_table_names(tables_prompt):
    raw_table_names = ask_gpt(tables_prompt)
    raw_table_names = re.findall(r'::\w+', raw_table_names)
    raw_table_names = [table[2:] for table in raw_table_names]
    raw_table_names = [f"'{table}'" for table in raw_table_names]
    return raw_table_names


def execute_query(postgres_reference_id, sql_query):
    postgres_reference = PostgresReference.objects.get(
        pk=postgres_reference_id)
    connection = psycopg2.connect(
        host=postgres_reference.host,
        port=postgres_reference.port,
        user=postgres_reference.db_user_name,
        password=postgres_reference.password,
        database=postgres_reference.db_name
    )
    cursor = connection.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    connection.close()
    return results


def fetch_tables_schema(postgres_reference_id, table_names):
    sql = f"SELECT tc.table_name AS table, tc.column_name AS column FROM information_schema.columns AS tc LEFT JOIN information_schema.key_column_usage AS kcu ON tc.table_name = kcu.table_name AND tc.column_name = kcu.column_name LEFT JOIN information_schema.constraint_column_usage AS ccu ON kcu.constraint_name = ccu.constraint_name WHERE tc.table_name IN ({', '.join(map(str, table_names))}) ORDER BY tc.table_name, tc.ordinal_position;"
    result = execute_query(postgres_reference_id, sql)
    return str([row for row in result]).replace("', '", ": ").replace("('", "").replace("')", "")


def fetch_table_names(postgres_reference_id):
    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    result = execute_query(postgres_reference_id, sql)
    return [row[0] for row in result]
