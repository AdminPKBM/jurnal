import os
import markdown
from jinja2 import Template

def build_blog():
    # Konfigurasi Folder
    POSTS_DIR = 'posts'
    TEMPLATE_DIR = 'templates'
    # Output ke root agar langsung dibaca oleh GitHub Pages
    OUTPUT_DIR = '.' 

    # Pastikan folder posts ada, jika tidak, buat foldernya
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)
        print(f"Folder '{POSTS_DIR}' dibuat. Silakan isi dengan file .md")

    posts_metadata = []

    # 1. PROSES SEMUA FILE MARKDOWN
    for filename in sorted(os.listdir(POSTS_DIR), reverse=True):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                
                # Mengubah Markdown menjadi HTML
                html_content = markdown.markdown(text, extensions=['extra', 'codehilite'])
                
                # Membuat judul dari nama file (misal: 'halo-dunia.md' jadi 'Halo Dunia')
                title = filename.replace('.md', '').replace('-', ' ').title()
                
                # Merakit dengan file templates/layout.html
                try:
                    with open(f'{TEMPLATE_DIR}/layout.html', 'r', encoding='utf-8') as t:
                        template = Template(t.read())
                        output_html = template.render(title=title, content=html_content)
                    
                    # Nama file output (misal: halo-dunia.html)
                    output_filename = filename.replace('.md', '.html')
                    
                    with open(os.path.join(OUTPUT_DIR, output_filename), 'w', encoding='utf-8') as out:
                        out.write(output_html)
                    
                    # Simpan data untuk daftar isi di index.html
                    posts_metadata.append({'title': title, 'url': output_filename})
                    print(f"✓ Berhasil memproses: {filename}")
                except Exception as e:
                    print(f"✗ Gagal memproses {filename}: {e}")

    # 2. BUAT HALAMAN UTAMA (index.html)
    try:
        with open(f'{TEMPLATE_DIR}/index_template.html', 'r', encoding='utf-8') as t:
            template = Template(t.read())
            index_html = template.render(posts=posts_metadata)
        
        with open('index.html', 'w', encoding='utf-8') as out:
            out.write(index_html)
        print("✓ Halaman index.html berhasil diperbarui!")
    except Exception as e:
        print(f"✗ Gagal membuat index.html: {e}")

if __name__ == "__main__":
    build_blog()
