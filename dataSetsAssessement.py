from pprint import pprint
import pandas as pd

objetsTrouvesGares = pd.read_csv('objets-trouves-gares.csv', delimiter = ';')
objetsTrouvesRestitution = pd.read_csv('objets-trouves-restitution.csv', delimiter = ';')

# Count values != NaN
objetsTrouvesGaresCount = objetsTrouvesGares.count()
objetsTrouvesRestitutionCount = objetsTrouvesRestitution.count()

print('\nResultats pour "objets-trouves-gares":\n')
pprint(objetsTrouvesGaresCount)

print('\nResultats pour "objets-trouves-restitution";\n')
pprint(objetsTrouvesRestitutionCount)