import sys, os, subprocess

now_dir = os.getcwd()
absolute_to_workspace = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)

os.chdir(absolute_to_workspace)

subprocess.call(["cmd.exe", "/c", '.\\update_altium.bat'])
subprocess.call(["cmd.exe", "/c", '.\\_tools\\run_python.bat', '.\\_tools\\export_csv.py'])

process = subprocess.Popen(["svn", "status"], stdout=subprocess.PIPE)
out, err = process.communicate()

os.chdir(now_dir)

if len(out) > 0:
    print("Changes occured during access startup! Check database!")
    print(out.decode('ascii'))

    process = subprocess.Popen(["svn", "diff"], stdout=subprocess.PIPE)
    out, err = process.communicate()
    print(out.decode('ascii'))
    sys.exit(1)
