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

def remove_imports(content):
    return re.sub(r'^import .*$\n?', '', content, flags=re.MULTILINE)

def is_test_file(file_path, content):
    test_indicators = [
        'Test.kt',
        '@RunWith',
        '@Test',
        'InstrumentationRegistry',
        'AndroidJUnit4'
    ]
    return any(indicator in file_path or indicator in content for indicator in test_indicators)

def process_file(file_path, project_path):
    content = extract_text_from_file(file_path)
    if not content or is_test_file(file_path, content):
        return None

    relative_path = os.path.relpath(file_path, project_path)
    content_without_imports = remove_imports(content)

    return {
        "file_path": relative_path,
        "content": content_without_imports
    }

def extract_text_from_project(project_path):
    kotlin_files = []
    gradle_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.kt'):
                kotlin_files.append(os.path.join(root, file))
            elif file.endswith('.gradle.kts'):
                gradle_files.append(os.path.join(root, file))
    
    all_files_data = []
    
    for file_list in [kotlin_files, gradle_files]:
        for file_path in file_list:
            file_data = process_file(file_path, project_path)
            if file_data:
                all_files_data.append(file_data)
    
    return all_files_data

def format_output(all_files_data):
    output = []
    for file_data in all_files_data:
        output.append(f"FILE: {file_data['file_path']}")
        output.append("CONTENT:")
        output.append(file_data['content'])
        output.append("="*50)
    return '\n'.join(output)

def create_output_directories():
    """Create necessary output directories if they don't exist."""
    base_dir = 'extracted_content'
    framework_dir = os.path.join(base_dir, 'android')
    os.makedirs(framework_dir, exist_ok=True)
    return framework_dir

def main():
    # List of project paths
    project_paths = [
        '/Users/somto/AndroidStudioProjects/NounHub',
        '/Users/somto/AndroidStudioProjects/NounHub/shared',
        '/Users/somto/AndroidStudioProjects/NounHub/authManagement',
        '/Users/somto/AndroidStudioProjects/NounHub/post',
        '/Users/somto/AndroidStudioProjects/NounHub/common',
        '/Users/somto/AndroidStudioProjects/NounHub/androidAppAdmin',
        '/Users/somto/AndroidStudioProjects/NounHub/androidAppUser',
        '/Users/somto/AndroidStudioProjects/NounHub/chat',
        '/Users/somto/AndroidStudioProjects/NounHub/admob',
        '/Users/somto/Downloads/Pdf-Viewer-master'
    ]

    # Create output directories
    framework_dir = create_output_directories()

    print(f"Total paths to process: {len(project_paths)}")

    for index, project_path in enumerate(project_paths, 1):
        print(f"\nProcessing path {index}/{len(project_paths)}: {project_path}")
        
        if not os.path.exists(project_path):
            print(f"Warning: Path does not exist: {project_path}")
            continue
        
        extracted_data = extract_text_from_project(project_path)
        
        if not extracted_data:
            print(f"No valid .kt or .gradle.kts files found in: {project_path}")
            continue
        
        formatted_output = format_output(extracted_data)
        
        # Generate output file name and path
        output_file_name = f"{os.path.basename(project_path)}_kotlin_and_gradle_structured.txt"
        output_path = os.path.join(framework_dir, output_file_name)
        
        # Save the extracted text to a file
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(formatted_output)
        
        print(f"Enhanced Kotlin and Gradle KTS text extraction complete for {project_path}")
        print(f"Saved to '{output_path}'")
        print(f"Processed {len(extracted_data)} files")
        print("-" * 50)

    print("All project paths processed.")

if __name__ == "__main__":
    main()


    # Usage: python3 android_extractor.py