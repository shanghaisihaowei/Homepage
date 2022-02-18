import snowflake.client
def get_snowflake_uuid():
    guid = snowflake.client.get_guid()
    return guid