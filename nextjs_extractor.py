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
    import_patterns = [
        r'^import .*$',
        r'require\(["\'].*["\']\)',
        r'from ["\'].*["\']\simport'
    ]
    imports = []
    for pattern in import_patterns:
        imports.extend(re.findall(pattern, content, re.MULTILINE))
    return imports

def extract_components_and_functions(content):
    component_patterns = [
        r'(?:export default |export )?(?:function|const) (\w+)(?:\s*:\s*React\.FC)?\s*(?:\([^)]*\))?\s*(?:=>|\{)',
        r'class (\w+) extends React\.Component',
        r'class (\w+) extends Component'
    ]
    hook_pattern = r'(?:export )?const use(\w+)\s*='
    
    components = []
    for pattern in component_patterns:
        components.extend(re.findall(pattern, content))
    hooks = re.findall(hook_pattern, content)
    
    return components, hooks

def process_file(file_path, project_path):
    content = extract_text_from_file(file_path)
    if not content:
        return None

    relative_path = os.path.relpath(file_path, project_path)
    metadata = get_file_metadata(file_path)
    imports = extract_imports(content)
    components, hooks = extract_components_and_functions(content)

    return {
        "file_path": relative_path,
        "metadata": metadata,
        "imports": imports,
        "components": components,
        "hooks": hooks,
        "content": content
    }

def extract_text_from_project(project_path):
    react_files = []
    config_files = []
    excluded_dirs = {'node_modules', '.next', 'build', 'dist', '.git'}
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        for file in files:
            if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                react_files.append(os.path.join(root, file))
            elif file in ['package.json', 'tsconfig.json', 'next.config.js']:
                config_files.append(os.path.join(root, file))
    
    all_files_data = []
    for file_list in [react_files, config_files]:
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
        output.append("COMPONENTS:")
        output.extend(file_data['components'])
        output.append("HOOKS:")
        output.extend(file_data['hooks'])
        output.append("CONTENT:")
        output.append(file_data['content'])
        output.append("="*50)
    return '\n'.join(output)

def create_output_directories():
    """Create necessary output directories if they don't exist."""
    base_dir = 'extracted_content'
    framework_dir = os.path.join(base_dir, 'react')
    os.makedirs(framework_dir, exist_ok=True)
    return framework_dir

def main():
    project_paths = [
        # Add your Next.js project paths here
        '/Users/somto/VsCodeProjects/auth-test'
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
            print(f"No React/Next.js files found in: {project_path}")
            continue
        
        formatted_output = format_output(extracted_data)
        
        output_file_name = f"{os.path.basename(project_path)}_react_structured.txt"
        output_path = os.path.join(framework_dir, output_file_name)
        
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(formatted_output)
        
        print(f"Enhanced React/Next.js text extraction complete for {project_path}")
        print(f"Saved to '{output_path}'")
        print(f"Processed {len(extracted_data)} files")
        print("-" * 50)

    print("All project paths processed.")

if __name__ == "__main__":
    main()


    # Usage: python3 nextjs_extractor.py