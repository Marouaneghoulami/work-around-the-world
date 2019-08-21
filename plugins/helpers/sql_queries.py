class SqlQueries:
    songplay_table_insert = ("""
        SELECT
                md5(events.sessionid || events.start_time) songplay_id,
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id, 
                songs.artist_id, 
                events.sessionid, 
                events.location, 
                events.useragent
                FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
    """)

    user_table_insert = ("""
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """)

    song_table_insert = ("""
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
    """)

    artist_table_insert = ("""
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
        SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
               extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
        FROM songplays
    """)

    recreate_staging_dice_com_jobs_table = ("""
        DROP TABLE IF EXISTS staging_dice_com_jobs;
        CREATE TABLE staging_dice_com_jobs (
            country_code VARCHAR(500),
            date_added DATE SORTKEY,
            job_board VARCHAR(500),
            job_description VARCHAR(65535),
            job_title VARCHAR(500),
            job_type VARCHAR(200),
            location VARCHAR(500),
            organization VARCHAR(500),
            page_url VARCHAR(1000),
            phone_number VARCHAR(500),
            salary VARCHAR(100),
            sector VARCHAR(5000)
        ) DISTSTYLE EVEN;
    """)

    select_companies_from_dice_jobs_staging_table = ("""
        select distinct  
            REPLACE(TRIM(regexp_replace(translate(
                LOWER(organization),
                'áàâãäåāăąèééêëēĕėęěìíîïìĩīĭḩóôõöōŏőùúûüũūŭůäàáâãåæçćĉčöòóôõøüùúûßéèêëýñîìíïş',
                'aaaaaaaaaeeeeeeeeeeiiiiiiiihooooooouuuuuuuuaaaaaaeccccoooooouuuuseeeeyniiiis'
            ), '[^a-z0-9\-]+', ' ')),' ', '-') as id,
            organization as name,
            NULL as remote_url
        from 
            staging_dice_com_jobs
        where 1 not in (select id from companies);
    """)