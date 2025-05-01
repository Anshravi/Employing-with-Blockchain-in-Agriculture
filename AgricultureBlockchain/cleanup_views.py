import re

def clean_views_file():
    with open('AgricultureApp/views.py', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find all function definitions
    functions = re.findall(r'def\s+(\w+)\s*\([^)]*\):', content)
    
    # Keep only the first occurrence of each function
    seen = set()
    cleaned_content = []
    current_function = None
    
    for line in content.split('\n'):
        match = re.match(r'def\s+(\w+)\s*\([^)]*\):', line)
        if match:
            func_name = match.group(1)
            if func_name in seen:
                current_function = func_name
                continue
            seen.add(func_name)
            current_function = None
        
        if current_function is None:
            cleaned_content.append(line)
    
    # Write cleaned content back to file
    with open('AgricultureApp/views.py', 'w', encoding='utf-8') as file:
        file.write('\n'.join(cleaned_content))

if __name__ == '__main__':
    clean_views_file() 