SElECT
    t.relname AS table_name,
    i.relname AS index_name,
    array_to_string(array_agg(a.attname), ', ') AS column_names
FROM
    pg_class t,
    pg_class i,
    pg_index ix,
    pg_attribute a
WHERE
    t.oid = ix.indrelid
    AND i.oid = ix.indexrelid
    AND a.attrelid = t.oid
    AND a.attnum = ANY(ix.indkey)
    AND t.relkind = 'r'
    AND t.relname IN ('mentor_candidates', 'schools')
    AND i.relname NOT IN ('schools_pk')
GROUP BY
    t.relname,
    i.relname
ORDER BY
    t.relname,
    i.relname;
