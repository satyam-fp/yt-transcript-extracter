from openai import OpenAI
from dotenv import load_dotenv  
import os
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

system_prompt = '''
You are an expert-level Blender Python script writer. You have the ability to create any 3D scene, models, texutre materials, animations just using Python scripting. As per the user's prompt or images or the description of all the components given in the thread, generate a Blender Python script to perform the requsted task. If image input was provided make sure you are as accurate as possible to the provided image and fits into the description. 
Also, add materials. Name the components properly and position them so they look like the input image.  Make sure that the components of the model does not have any unnecessary gaps. Smooth edges and add bevel wherever needed. 

 Your purpose is to help users modify 3D meshes using natural language commands. Follow these guidelines:

1. Response Format:
   - Always respond with Python code wrapped in triple backticks (```).
   - Do not include any explanatory texts at all.

2. Code Style and Best Practices:
   - Import entire modules instead of individual components.
   - Use descriptive variable names and add comments for clarity.
   - Follow PEP 8 style guidelines for Python code.

3. Blender-specific Instructions:
   - Avoid destructive operations on meshes.
   - Do not use `cap_ends` function.
   - Don't perform actions beyond what is explicitly requested (e.g., setting up render settings, adding cameras).
   - Use keyframe animation for all animation tasks.
   - When applying colors, always use RGBA format with alpha channel (e.g., (1, 0, 0, 1) for red).
   - Check if a material exists before applying color. If not, create a new material.
   - For textures, use image nodes in the shader editor. Avoid using random texture enums not available in Blender.

4. Error Handling and Safety:
   - Include error handling in your code where appropriate.
   - Provide safeguards against potential issues (e.g., check for existing objects before creating new ones).

5. Efficiency and Performance:
   - Optimize code for performance, especially when dealing with large numbers of objects or complex operations.
   - Use Blender's built-in functions and APIs whenever possible for better performance.

6. Adaptability:
   - Be prepared to modify or extend existing objects and materials.
   - If a user request is ambiguous, interpret it in the most likely and useful way for Blender operations.

7. Advanced Features:
   - Be ready to utilize Blender's advanced features like modifiers, particle systems, and physics simulations when appropriate.
   - Implement proper scene management techniques for complex scenes.

'''
system_prompt = open("C:\Work\Mixar\yt-transcript-extracter\.idea\system_instruction.txt", "r").read()
prompt = open("C:\Work\Mixar\yt-transcript-extracter\.idea\prompt.txt", "r").read()
# prompt = "create a 3d model of a sofa"
completion = client.chat.completions.create(
    model="gpt-4o",

    store=True,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

)

result_text = completion.choices[0].message.content.strip()
# print(result_text)

# Remove markdown formatting from the returned Blender Python code
python_code = result_text.replace("```python", "").replace("```", "")

# === New Code Below: Save the generated Blender script into script.py ===
with open("script.py", "w") as f:
    f.write(python_code)

# Instead of executing the code via exec, run Blender with the saved script in a loop until successful
import subprocess

blender_exe = r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"

count = 5
while count > 0:
    try:
        # Execute Blender in background mode with the generated script
        result = subprocess.run(
            [blender_exe, "-b", "--python", "script.py"],
            # [blender_exe, "--python", "script.py"],
            capture_output=True,
            text=True,
            check=True
        )

        if result.stderr.strip() == "":
            print("########################################################")
            print(result.stderr)
            print("########################################################")
            print("Blender script executed successfully")
            break  # if successful, exit the loop
        else:
            error_msg = result.stderr
            print("Blender script failed with error:")
            print(error_msg)
            # Prepare a prompt with the error and the current script content to get a corrected version from GPT
            fix_prompt = (
                "The Blender Python script 'script.py' failed with the following error:\n\n"
                f"{error_msg}\n\n"
                "The current script content is:\n\n"
                f"{python_code}\n\n"
                "Please fix the code and return the entire corrected Python code without any explanation."
            )
            
            fix_completion = client.chat.completions.create(
                model="gpt-4o",
                store=True,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": fix_prompt}
                ]
            )
            
            corrected_code = fix_completion.choices[0].message.content.strip()
            # Remove markdown formatting if present
            corrected_code_clean = corrected_code.replace("```python", "").replace("```", "")
            # print("Corrected Code:")
            # print(corrected_code_clean)
            
            # Update script.py with the corrected code and update python_code for the next loop iteration
            with open("script.py", "w") as f:
                f.write(corrected_code_clean)
            python_code = corrected_code_clean
            print(f"######################################################## count: {count}")
            count -= 1

    except subprocess.CalledProcessError as err:
        error_msg = err.stderr
        print("Blender script failed with error:")
        print(error_msg)
        break
        
