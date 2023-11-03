import weasyprint
from PIL import Image
from pdf2image import convert_from_bytes


# Sample data
current_time = "14:30"
tasks = [
    {"task": "Buy groceries", "due_date": "2023-11-10"},
    {"task": "Complete project", "due_date": "2023-11-15"},
]
temperature = "22°C"
conditions = "Sunny"

# Create an HTML template with placeholders
html_template = """
<html>
<head>
    <style>
        /* Your CSS styles here */
    </style>
</head>
<body>
    <h1>Fancy Dashboard</h1>
    <p>Current Time: {current_time}</p>
    <ul>
        {task_list}
    </ul>
    <p>Weather: {temperature}, {conditions}</p>
</body>
</html>
"""

# Create a string with the task list
task_list = ""
for task in tasks:
    task_list += f"<li>{task['task']} - Due Date: {task['due_date']}</li>"

# Replace placeholders in the HTML template with actual values
html_content = html_template.format(
    current_time=current_time,
    task_list=task_list,
    temperature=temperature,
    conditions=conditions
)

# Convert HTML to PDF using WeasyPrint
pdf = weasyprint.HTML(string=html_content).write_pdf()

# Convert PDF to image using pdf2image
images = convert_from_bytes(pdf)

# Save the first page as an image
image = images[0]

image.save("dashboard.png")

# Display the image on your E-ink display
# Add code for your specific hardware display library
