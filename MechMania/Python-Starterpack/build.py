import zipapp
print("Writing to bot.pyz...")
zipapp.create_archive('.', main='main:main', target='C:/Users/patbo/MechMania/bot.pyz')
print("Done!")