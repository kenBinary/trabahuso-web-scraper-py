import sqlite3


def main():
    connection = sqlite3.connect("../../db/job_record.db")
    cursor = connection.cursor()
    duplicates = cursor.execute(
        """SELECT job_title,
       count(job_title),
       location,
       count(location),
       salary,
       count(salary),
       job_level,
       count(job_level),
       date_scraped,
       count(date_scraped) 
  FROM job_data
 GROUP BY job_title,
          location,
          salary,
          job_level,
          date_scraped
HAVING count(job_title) > 1 AND 
       count(location) > 1 AND 
       count(salary) > 1 AND 
       count(job_level) > 1 AND 
       count(date_scraped) > 1;
"""
    ).fetchall()

    try:
        for duplicate in duplicates:
            job_title = duplicate[0]
            job_location = duplicate[2]
            job_salary = duplicate[4]
            job_level = duplicate[6]
            date_scraped = duplicate[8]

            job_id = cursor.execute(
                f"""
                SELECT job_data_id
                FROM job_data
                WHERE job_title = ? AND 
                    location = ? AND 
                    salary = ? AND 
                    job_level = ? AND 
                    date_scraped = ?
                    LIMIT 1;
            """,
                (
                    job_title,
                    job_location,
                    job_salary,
                    job_level,
                    date_scraped,
                ),
            ).fetchall()

            cursor.execute(
                """
            DELETE FROM tech_skill
                WHERE job_data_id = ?;
                """,
                (job_id[0][0],),
            )

            cursor.execute(
                """
            DELETE FROM job_data
                WHERE job_data_id = ?;
                """,
                (job_id[0][0],),
            )
    except Exception as e:
        print(e)
        print("failed to delete duplicates")
    finally:
        connection.commit()


if __name__ == "__main__":
    main()
