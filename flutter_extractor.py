import os
import re
from datetime import datetime

def extract_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except UnicodeDecodeError:
        print(f"Skipping file due to encoding issues: {file_path}")
        return ""

def get_file_metadata(file_path):
    stats = os.stat(file_path)
    return {
        "size": stats.st_size,
        "last_modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
        "line_count": sum(1 for _ in open(file_path, 'rb'))
    }

def extract_imports(content):
    return re.findall(r'^import .*$', content, re.MULTILINE)

def extract_classes_and_functions(content):
    class_pattern = r'class (\w+)'
    function_pattern = r'(?:void|Future|String|int|double|bool|List|Map|dynamic) (\w+)\('
    classes = re.findall(class_pattern, content)
    functions = re.findall(function_pattern, content)
    return classes, [f[1] for f in functions]

def process_file(file_path, project_path):
    content = extract_text_from_file(file_path)
    if not content:
        return None

    relative_path = os.path.relpath(file_path, project_path)
    metadata = get_file_metadata(file_path)
    imports = extract_imports(content)
    classes, functions = extract_classes_and_functions(content)

    return {
        "file_path": relative_path,
        "metadata": metadata,
        "imports": imports,
        "classes": classes,
        "functions": functions,
        "content": content
    }

def extract_text_from_project(project_path):
    dart_files = []
    yaml_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.dart'):
                dart_files.append(os.path.join(root, file))
            elif file.endswith('.yaml'):
                yaml_files.append(os.path.join(root, file))
    
    all_files_data = []
    
    for file_list in [dart_files, yaml_files]:
        for file_path in file_list:
            file_data = process_file(file_path, project_path)
            if file_data:
                all_files_data.append(file_data)
    
    return all_files_data

def format_output(all_files_data):
    output = []
    for file_data in all_files_data:
        output.append(f"FILE: {file_data['file_path']}")
        output.append(f"METADATA: {file_data['metadata']}")
        output.append("IMPORTS:")
        output.extend(file_data['imports'])
        output.append("CLASSES:")
        output.extend(file_data['classes'])
        output.append("FUNCTIONS:")
        output.extend(file_data['functions'])
        output.append("CONTENT:")
        output.append(file_data['content'])
        output.append("="*50)
    return '\n'.join(output)

def create_output_directories():
    """Create necessary output directories if they don't exist."""
    base_dir = 'extracted_content'
    framework_dir = os.path.join(base_dir, 'flutter')
    os.makedirs(framework_dir, exist_ok=True)
    return framework_dir

def main():
    project_paths = [
        '/Users/somto/AndroidStudioProjects/CusorCart'
    ]

    framework_dir = create_output_directories()
    print(f"Total paths to process: {len(project_paths)}")

    for index, project_path in enumerate(project_paths, 1):
        print(f"\nProcessing path {index}/{len(project_paths)}: {project_path}")
        
        if not os.path.exists(project_path):
            print(f"Warning: Path does not exist: {project_path}")
            continue
        
        extracted_data = extract_text_from_project(project_path)
        
        if not extracted_data:
            print(f"No .dart or .yaml files found in: {project_path}")
            continue
        
        formatted_output = format_output(extracted_data)
        
        output_file_name = f"{os.path.basename(project_path)}_flutter_structured.txt"
        output_path = os.path.join(framework_dir, output_file_name)
        
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(formatted_output)
        
        print(f"Enhanced Flutter text extraction complete for {project_path}")
        print(f"Saved to '{output_path}'")
        print(f"Processed {len(extracted_data)} files")
        print("-" * 50)

    print("All project paths processed.")

if __name__ == "__main__":
    main()


    # Usage: python3 flutter_extractor.py