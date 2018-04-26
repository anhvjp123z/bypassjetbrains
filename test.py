import requests

simsimi = requests.get('http://simsimi.tubotocdo.design/api_sim.php?key=tubotocdo&tenbot=ahihi&text=dm')

print(simsimi.text)