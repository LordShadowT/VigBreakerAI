import random

print('Program started')
with open('wordlist_clean.txt', 'r', encoding='Windows-1252') as f:
    with open('training_data.txt', 'w', encoding='Windows-1252') as output:
        print('Files loaded')
        lines = f.readlines()
        total_lines = len(lines)
        for i in range(100):
            for j in range(500):
                words = []
                line = ' '
                for j in range(random.randint(30, 120)):
                    random_line = lines[random.randint(0, total_lines - 1)]
                    words.append(random_line.replace('\n', ''))
                line = line.join(words)
                line += '\n'
                output.write(line)
            print('Generated ' + str(i) + '%')
        print('Finished')
