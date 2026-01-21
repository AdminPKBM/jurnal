import os
import markdown
from jinja2 import Template

def build_blog():
    POSTS_DIR = 'posts'
    PAGES_DIR = 'pages'
    TEMPLATE_DIR = 'templates'
    OUTPUT_DIR = '.' 

    # Buat folder jika belum ada
    for folder in [POSTS_DIR, PAGES_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    posts_metadata = []

    # --- BAGIAN 1: PROSES ARTIKEL (POSTS) ---
    # File di sini akan muncul di halaman depan (index.html)
    files_posts = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md')]
    for filename in sorted(files_posts, reverse=True):
        with open(os.path.join(POSTS_DIR, filename), 'r', encoding='utf-8') as f:
            content_html = markdown.markdown(f.read(), extensions=['extra', 'codehilite'])
            title = filename.replace('.md', '').replace('-', ' ').title()
            
            with open(f'{TEMPLATE_DIR}/layout.html', 'r', encoding='utf-8') as t:
                output_html = Template(t.read()).render(title=title, content=content_html)
            
            output_name = filename.replace('.md', '.html')
            with open(os.path.join(OUTPUT_DIR, output_name), 'w', encoding='utf-8') as out:
                out.write(output_html)
            
            # Tambahkan ke daftar artikel untuk index
            posts_metadata.append({'title': title, 'url': output_name})

    # --- BAGIAN 2: PROSES HALAMAN (PAGES) ---
    # File di sini HANYA dibuat HTML-nya, tidak masuk ke daftar index
    files_pages = [f for f in os.listdir(PAGES_DIR) if f.endswith('.md')]
    for filename in files_pages:
        with open(os.path.join(PAGES_DIR, filename), 'r', encoding='utf-8') as f:
            content_html = markdown.markdown(f.read(), extensions=['extra'])
            title = filename.replace('.md', '').replace('-', ' ').title()
            
            with open(f'{TEMPLATE_DIR}/layout.html', 'r', encoding='utf-8') as t:
                output_html = Template(t.read()).render(title=title, content=content_html)
            
            output_name = filename.replace('.md', '.html')
            with open(os.path.join(OUTPUT_DIR, output_name), 'w', encoding='utf-8') as out:
                out.write(output_html)

    # --- BAGIAN 3: GENERATE BERANDA (INDEX) ---
    # Hanya menggunakan posts_metadata (dari folder posts)
    with open(f'{TEMPLATE_DIR}/index_template.html', 'r', encoding='utf-8') as t:
        index_html = Template(t.read()).render(posts=posts_metadata)
    
    with open('index.html', 'w', encoding='utf-8') as out:
        out.write(index_html)
    
    print("✓ Sukses: Artikel dan Halaman Statis berhasil dipisahkan!")

if __name__ == "__main__":
    build_blog()
