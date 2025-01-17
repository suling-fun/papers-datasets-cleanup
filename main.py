import subprocess

def run_script(script_name):
    try:
        result = subprocess.run(["python", script_name], check=True)
        print(f"{script_name} executed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")
        return False

if __name__ == "__main__":
    # 先执行 pdf_to_md.py
    if run_script("pdf_to_md.py"):
        # 如果 pdf_to_md.py 执行成功，再执行 text_extractor.py
        run_script("text_extractor.py")