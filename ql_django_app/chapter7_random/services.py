# Fichier : ql_web_app/chapter7_random/services.py
import QuantLib as ql

def generate_random_points(generator_type: str, num_points: int, seed: int):
    """
    Génère un nombre spécifié de points 2D en utilisant un générateur de nombres aléatoires sélectionné.
    """
    points = []
    
    if generator_type == 'pseudorandom':
        # Mersenne Twister : un générateur pseudo-aléatoire de haute qualité
        rng = ql.MersenneTwisterUniformRng(seed)
        for i in range(num_points * 2): # On a besoin de 2x plus de nombres pour des paires
            x = rng.next().value()
            y = rng.next().value()
            points.append({'x': x, 'y': y})
            
    elif generator_type == 'quasirandom':
        # Sobol : une séquence à faible disparité (quasi-aléatoire)
        # Il nécessite la dimensionnalité à la création (2D dans notre cas)
        rng = ql.SobolRsg(2, seed)
        for i in range(num_points):
            # nextSequence() renvoie une liste de valeurs [x, y]
            point_values = rng.nextSequence().value()
            points.append({'x': point_values[0], 'y': point_values[1]})
            
    else:
        raise ValueError("Type de générateur inconnu")
        
    return points