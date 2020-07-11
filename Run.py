import os

def run(runfile):
  with open(runfile,"r") as rnf:
    exec(rnf.read())

if os.path.exists('covid.sqlite'):
    print("Database already exist")
    c = input('Want to create new one? (Y/N)')
    if c == 'Y':
        os.remove('covid.sqlite')
        print('Old SQLite File Has Been Deleted..')
        #os.system('python state_city.py')
        print('Creating new db')
        run("state_city.py")
    else:
        print('Using old database')
else:
    print('creating new db...')
    run("state_city.py")
print('Running scrapper.py...')
c = input('Want to fetch updated data? (Y/N)')
if c == 'Y':
    run('scrapper.py')
    print('Data fetched successfully')

print('Visualizing data...')
run('selector.py')