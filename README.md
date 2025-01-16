# Code Extractor Hub

A collection of code extractors for different frameworks that help analyze and extract structured content from various project codebases. The extracted content is specifically formatted to be used as context for AI models, allowing them to understand your codebase structure and provide more accurate responses to your development queries.

## Key Benefits

- Provides structured context for AI model interactions
- Enables AI to understand your codebase architecture
- Facilitates more accurate AI responses to development questions
- Helps AI provide relevant code suggestions and improvements

## Features

- Framework-specific code extraction
- Organized output structure
- Configurable project paths
- Import analysis
- Class and function detection
- Test file filtering

## Supported Frameworks

- Android (Kotlin)
- Flutter (Dart)
- React/Next.js
- [More frameworks to be added]

## Usage

1. Place your extractor script in the `extractors/` directory
2. Configure project paths in the script
3. Run the extractor:
```bash
python extractors/[framework]_extractor.py
```

Output will be generated in `extracted_content/[framework]/`

## Adding New Frameworks

1. Create new extractor following naming pattern: `[framework]_extractor.py`
2. Create corresponding output directory in `extracted_content/[framework]/`
3. Update README with new framework support

## Structure

Each extractor provides:
- File metadata
- Code structure analysis
- Content extraction
- Framework-specific parsing

## Contributing

Feel free to add extractors for new frameworks following the established patterns and structure.