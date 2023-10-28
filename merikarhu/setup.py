import os, shutil, subprocess, datetime

# Resetoi dist ja luo tyhjät kansiot
try:
    shutil.rmtree("./dist")
except:
    pass
os.makedirs("./dist")
os.makedirs("./dist/merikarhu")

dist_dir = "./dist"
install_dir = "./dist/merikarhu"

os.makedirs(os.path.join(install_dir, "build"))
os.makedirs(os.path.join(install_dir, "input"))
os.makedirs(os.path.join(install_dir, "output"))

# Luodaan requirements
result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
packages = result.stdout.splitlines()
requirements_file_path = "./requirements.txt"
with open(requirements_file_path, "w") as requirements_file:
    for package in packages:
        requirements_file.write(package + "\n")


# Siirretään kansiot
shutil.copytree(
    r"./templates", os.path.join(install_dir, "templates"), dirs_exist_ok=True
)
shutil.copytree(r"./other", os.path.join(install_dir, "other"), dirs_exist_ok=True)

# Siirretään asenna.bat juureen
shutil.move(os.path.join(install_dir, "other", "asenna.bat"), dist_dir)

# Siirretään tiedostot
musta_lista = ["setup.py", ".gitignore", "loggaus.log", "sykli.png"]
for file in os.listdir("."):
    if file not in musta_lista and os.path.isfile(os.path.join(".", file)):
        shutil.copy2(os.path.join(".", file), os.path.join(install_dir, file))

# Paketoi tiedostot ZIP-muotoon
pvm = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
zip_file_path = shutil.make_archive(
    f"Merikarhu-{pvm}", "zip", root_dir=dist_dir, base_dir=""
)

# Kopioi paketti /dist ja siirrä arkistoon
shutil.copy(zip_file_path, dist_dir)
shutil.move(zip_file_path, "./archive")
