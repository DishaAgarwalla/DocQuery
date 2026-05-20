from reportlab.pdfgen import canvas

c = canvas.Canvas('data/real_python.pdf')
y = 750

lines = [
    'Python is a high-level programming language created by Guido van Rossum in 1991.',
    'Python is used for web development, data science, artificial intelligence, and automation.',
    'Python has built-in data structures like lists, tuples, dictionaries, and sets.',
    'A list in Python is created using square brackets: my_list = [1, 2, 3].',
    'Lists are mutable and can hold different data types.',
    'Python is known for its simple, readable syntax and is widely used in industry and academia.'
]

for line in lines:
    c.drawString(50, y, line)
    y -= 20

c.save()
print('✅ real_python.pdf created successfully!')
