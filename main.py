import psycopg2


db = psycopg2.connect(
    host="",
    database="",
    user="",
    password=""
)

with db.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id SERIAL PRIMARY KEY,
            category_id INTEGER REFERENCES categories(id),
            title VARCHAR(200) NOT NULL UNIQUE,
            content TEXT NOT NULL,
            published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_published BOOLEAN DEFAULT FALSE
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            news_id INTEGER REFERENCES news(id),
            author TEXT,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    db.commit()

with db.cursor() as cur:
    cur.execute("""
        ALTER TABLE news
        ADD COLUMN IF NOT EXISTS views INTEGER DEFAULT 0;
    """)
    cur.execute("""
        ALTER TABLE comments
        ALTER COLUMN author TYPE TEXT;
    """)
    db.commit()

with db.cursor() as cur:
    cur.executemany("""
        INSERT INTO categories (name, description) VALUES (%s, %s)
    """, [
        ('Texnologiya', 'Eng soʻnggi texnologik yangiliklar'),
        ('Sport', 'Sport olamidagi eng soʻnggi voqealar'),
        ('Salomatlik', 'Sogʻlom hayot uchun tavsiyalar')
    ])
    cur.executemany("""
        INSERT INTO news (category_id, title, content) VALUES (%s, %s, %s)
    """, [
        (1, 'Sunʼiy intellektning yangi imkoniyatlari', 'Sunʼiy intellekt hayotni qanday o‘zgartirishi haqida maqola.'),
        (2, 'Futbol bo‘yicha Jahon chempionati', 'Jahon chempionatidagi eng soʻnggi yangiliklar.'),
        (3, 'Sogʻlom ovqatlanish bo‘yicha maslahatlar', 'Sogʻlom ovqatlanish uchun eng yaxshi tavsiyalar.')
    ])
    cur.executemany("""
        INSERT INTO comments (news_id, author, comment) VALUES (%s, %s, %s)
    """, [
        (1, 'Aziz', 'Bu juda qiziqarli yangilik!'),
        (2, 'Dilshod', 'Mazmunli maqola uchun rahmat.'),
        (3, 'Madina', 'Juda foydali maslahatlar!')
    ])
    db.commit()

with db.cursor() as cur:
    cur.execute("UPDATE news SET views = views + 1;")
    cur.execute("""
        UPDATE news
        SET is_published = TRUE
        WHERE published_at < CURRENT_TIMESTAMP - INTERVAL '1 day';
    """)
    db.commit()

with db.cursor() as cur:
    cur.execute("""
        DELETE FROM comments
        WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '1 year';
    """)
    db.commit()

with db.cursor() as cur:
    cur.execute("""
        SELECT n.id AS yangilik_id, n.title AS sarlavha, c.name AS kategoriya
        FROM news n
        JOIN categories c ON n.category_id = c.id;
    """)
    yangiliklar = cur.fetchall()

    cur.execute("""
        SELECT title, content FROM news
        JOIN categories ON news.category_id = categories.id
        WHERE categories.name = 'Texnologiya';
    """)
    texnologiya_yangiliklari = cur.fetchall()

    cur.execute("""
        SELECT id, title FROM news
        WHERE is_published = TRUE
        ORDER BY published_at DESC
        LIMIT 5;
    """)
    oxirgi_yangiliklar = cur.fetchall()

    cur.execute("""
        SELECT id, title FROM news
        WHERE views BETWEEN 10 AND 100;
    """)
    mashhur_yangiliklar = cur.fetchall()

    cur.execute("""
        SELECT id, author, comment FROM comments
        WHERE author LIKE 'A%';
    """)
    izohlar_a = cur.fetchall()

    cur.execute("""
        SELECT id, comment FROM comments
        WHERE author IS NULL;
    """)
    muallifsiz_izohlar = cur.fetchall()

    cur.execute("""
        SELECT c.name, COUNT(n.id) AS yangilik_soni
        FROM categories c
        LEFT JOIN news n ON c.id = n.category_id
        GROUP BY c.name;
    """)
    kategoriya_hisobi = cur.fetchall()

with db.cursor() as cur:
    cur.execute("""
        ALTER TABLE news
        ADD CONSTRAINT unique_title UNIQUE (title);
    """)
    db.commit()

db.close()
