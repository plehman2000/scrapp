import re

def remove_verse_numbers(input_file, output_file=None):
    if not output_file:
        output_file = input_file.replace('.txt', '_cleaned.txt')
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    cleaned = re.sub(r'^\d+:\d+\s+', '', content, flags=re.MULTILINE)
    
    with open(output_file, 'w') as f:
        f.write(cleaned)
    
    return output_file

remove_verse_numbers('bible.txt')