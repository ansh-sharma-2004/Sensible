import os
import shutil
import re

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp', '.webp'}
IMAGES_FOLDER = 'images'

def is_image_file(filename):
    return os.path.splitext(filename.lower())[1] in IMAGE_EXTENSIONS

def move_images(base_path):
    images_path = os.path.join(base_path, IMAGES_FOLDER)
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    
    for file in os.listdir(base_path):
        if is_image_file(file):
            src = os.path.join(base_path, file)
            dest = os.path.join(images_path, file)
            
            # Avoid overwrite
            if os.path.exists(dest):
                base, ext = os.path.splitext(file)
                count = 1
                while True:
                    new_name = f"{base}_{count}{ext}"
                    new_dest = os.path.join(images_path, new_name)
                    if not os.path.exists(new_dest):
                        dest = new_dest
                        break
                    count += 1
            
            print(f"Moving {file} to {IMAGES_FOLDER}/")
            shutil.move(src, dest)

def update_html_files(base_path):
    src_pattern = re.compile(r'(src\s*=\s*["\'])([^"\']+)(["\'])', re.IGNORECASE)
    
    for file in os.listdir(base_path):
        if file.endswith('.html'):
            file_path = os.path.join(base_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            def replace_src(match):
                prefix, path, suffix = match.groups()
                ext = os.path.splitext(path)[1].lower()
                if ext in IMAGE_EXTENSIONS:
                    img_name = os.path.basename(path)
                    new_path = f"{IMAGES_FOLDER}/{img_name}"
                    print(f"Updating {file}: {path} -> {new_path}")
                    return prefix + new_path + suffix
                else:
                    return match.group(0)
            
            new_content = src_pattern.sub(replace_src, content)
            
            if new_content != content:
                print(f"Writing changes to {file}")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

def update_css_files(base_path):
    css_pattern = re.compile(r'(url\(["\']?)([^"\')]+)(["\']?\))', re.IGNORECASE)

    for file in os.listdir(base_path):
        if file.endswith('.css'):
            file_path = os.path.join(base_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            def replace_url(match):
                prefix, path, suffix = match.groups()
                ext = os.path.splitext(path)[1].lower()
                if ext in IMAGE_EXTENSIONS:
                    filename = os.path.basename(path)
                    new_path = f"{IMAGES_FOLDER}/{filename}"
                    print(f"Updating CSS {file}: {path} -> {new_path}")
                    return prefix + new_path + suffix
                return match.group(0)

            new_content = css_pattern.sub(replace_url, content)

            if new_content != content:
                print(f"Writing changes to {file}")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    print("Working in folder:", base_path)
    move_images(base_path)
    update_html_files(base_path)
    print("Done!")

if __name__ == "__main__":
    main()
