import re

def parse_text_file(file_path, flag_file_path):
    with open(flag_file_path, 'r') as flag_file:
        flag = flag_file.read().strip()

    with open(file_path, 'r') as file:
        lines = file.readlines()

    parsed_lines = []
    sources_section = False

    for line in lines:
        # Check if the line contains the "Sources" section
        if "Sources" in line:
            sources_section = True
            break

        # Remove [x] patterns
        parsed_line = ''.join(part.split(']')[1] if ']' in part else part for part in line.split('['))

        if flag == "google":
            # Remove formatting like **, ##, and replace bullet points with " - "
            # Also remove all # and spaces around them
            parsed_line = parsed_line.replace('**', '').replace('*', '').replace('•', ' - ')
            parsed_line = parsed_line.replace('#', '').strip()

            # Remove enumerated components like 1., 2., etc.
            parsed_line = re.sub(r'^\d+\.\s*', '', parsed_line)

        # Ensure each line ends with a single newline character
        parsed_lines.append(parsed_line.rstrip() + '\n')

    # Write the parsed content back to the original file
    with open(file_path, 'w') as file:
        file.writelines(parsed_lines)

# Call the function with the path to your text file and flag file
parse_text_file('text.txt', 'flag.txt')