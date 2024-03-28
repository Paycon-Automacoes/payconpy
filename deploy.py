import sys
import os, shutil, sys
from dotenv import load_dotenv

load_dotenv()

pypi_username = os.getenv("PYPI_USERNAME")
pypi_password = os.getenv("PYPI_PASSWORD")

if not pypi_username or not pypi_password:
    print("Erro: As credenciais do PyPI não estão definidas no arquivo .env")
    sys.exit(1)

if os.path.exists('dist'):
    shutil.rmtree('dist')
    
if os.path.exists('payconpy.egg-info'):
    shutil.rmtree('payconpy.egg-info')

print("Criando a distribuição de origem...")
os.system("python setup.py sdist")

print("Fazendo o upload para o PyPI...")
os.system(f"twine upload -u {pypi_username} -p {pypi_password} dist/*")

print("Concluído!")