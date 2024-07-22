# build_files.sh
cd service
. myvenv/Scripts/activate
cd ToDoList
pip install -r requirements.txt
python3.9.6 manage.py collectstatic --no-input --clear