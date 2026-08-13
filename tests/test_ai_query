from ai_query import clean_sql, is_safe_query


def test_clean_sql_strips_markdown_fence_with_language_tag():
    raw = "```sql\nSELECT * FROM events;\n```"
    assert clean_sql(raw) == "SELECT * FROM events;"


def test_clean_sql_strips_plain_fence():
    raw = "```\nSELECT * FROM events;\n```"
    assert clean_sql(raw) == "SELECT * FROM events;"


def test_clean_sql_passes_through_unfenced_query():
    raw = "SELECT * FROM events;"
    assert clean_sql(raw) == "SELECT * FROM events;"


def test_is_safe_query_allows_select():
    assert is_safe_query("SELECT COUNT(*) FROM events") is True


def test_is_safe_query_blocks_non_select():
    assert is_safe_query("DELETE FROM events") is False


def test_is_safe_query_blocks_select_with_embedded_mutation():
    # e.g. a query wrapped around a subquery containing DDL/DML
    assert is_safe_query("SELECT 1; DROP TABLE events;") is False


def test_is_safe_query_case_insensitive():
    assert is_safe_query("select * from events") is True
    assert is_safe_query("Delete From events") is False
