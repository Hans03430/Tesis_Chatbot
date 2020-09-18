import re

text = '''


Hey there how



are you today?



'''
text_aux = re.sub(r'\b\n+\b', '\n', text)
print(text_aux)