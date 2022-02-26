import logging
import string
import configparser
import argparse
from collections import Counter

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-i", "--input", help = "Input file")
parser.add_argument("-o", "--output", help = "Output file")
parser.add_argument("-c", "--config", help = "Config file")

# Read arguments from command line
args = parser.parse_args()
args_dict = vars(args)

'''
Class TextSanitizer
to sanitize raw text

@param raw_text:string
'''
class TextSanitizer:

    def lower(self, raw_text: string):
        text_lower = raw_text.lower()
        print(f"lower case:\n================\n{text_lower}\n")
        return text_lower

    def replace(self, raw_text: string, _from: string, _to: string):
        replaced_text = raw_text.replace(_from, _to)
        print(f"replaced text from {_from} to {_to}:\n================\n{replaced_text}\n")
        return replaced_text

    '''
    name: sanitized_by
    decription: to call function dynamically
    @param: function name, function's parameters
    '''
    def sanitized_by(self, _func: string, *args, **kwargs):
        if hasattr(self, _func) and callable(func := getattr(self, _func)):
            return func(*args, **kwargs)

    '''
    count number of occurrence of each alphabet.
    '''
    def print_char_count(self, raw_text: string):
        counter = Counter(raw_text)
        text = "count letters\n================\nletter : count"
        for letter, count in sorted(counter.items()):
            if letter == '\n': letter = letter.replace('\n', 'newline')
            text = text + f"{letter:7}: {count}\n"

        print(text)
        return text

if __name__ == "__main__":
    input_file = None
    output_file = None

    # read config file
    if args_dict['config']:
        config_file = args_dict['config']
        config = configparser.ConfigParser()
        config.read(config_file)
        input_file = config['TEXTSANIZITER']['input_filename']
        output_file = config['TEXTSANIZITER']['output_filename']

    # read input argument
    if args_dict['input']:
        input_file = args_dict['input']
    
    # read output argument
    if args_dict['output']:
        output_file = args_dict['output']

    if input_file:
        f = open(input_file, "r")
        if output_file:
            logging.basicConfig(filename=output_file, filemode='w', format='[%(asctime)s] %(message)s', level=logging.INFO)
        else:
            logging.basicConfig(filename='output.log', filemode='w', format='[%(asctime)s] %(message)s', level=logging.INFO)
        
        text = f.read()
        print(f"raw text:\n{text}\n")

        sanitizer = TextSanitizer()
        logging.info(f"raw text:\n{text}")

        text = sanitizer.sanitized_by("lower", text)
        logging.info(f"lower:\n{text}")

        text = sanitizer.sanitized_by("replace", text, '\t', '____')
        logging.info(f"replace from \t to ____:\n{text}")

        char_count = sanitizer.print_char_count(text)
        logging.info(f"print character's count\n{char_count}")