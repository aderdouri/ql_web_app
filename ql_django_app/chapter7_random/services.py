
import QuantLib as ql

def generate_random_sequence(generator_type: str, num_points: int, seed: int, dimensionality: int):
    """
    Generates a sequence of N-dimensional points using a selected random number generator.
    This service replicates the core concepts from the 'random_numbers.ipynb' notebook.

    Args:
        generator_type (str): The type of generator to use ('pseudorandom' or 'quasirandom').
        num_points (int): The number of points to generate in the sequence.
        seed (int): The seed for the random number generator for reproducibility.
        dimensionality (int): The number of dimensions for each point in the sequence.

    Returns:
        list: A list of points. For 2D, it's a list of dictionaries [{'x':..., 'y':...}].
              For other dimensions, it's a list of lists [[d1, d2, ...], ...].
    """
    
    points = []
    
    if generator_type == 'pseudorandom':
        # This corresponds to the Mersenne Twister example in the notebook.
        # It's a high-quality pseudo-random generator.
        # Since it's a 1D generator, we need to call it 'dimensionality' times for each point.
        rng = ql.MersenneTwisterUniformRng(seed)
        for _ in range(num_points):
            point = [rng.next().value() for _ in range(dimensionality)]
            points.append(point)
            
    elif generator_type == 'quasirandom':
        # This corresponds to the Sobol sequence example in the notebook.
        # It's a low-discrepancy (quasi-random) sequence generator.
        # It must be initialized with the desired dimensionality.
        rng = ql.SobolRsg(dimensionality, seed)
        for _ in range(num_points):
            # nextSequence() returns a list of values with the correct dimensionality.
            point_values = rng.nextSequence().value()
            points.append(point_values)
            
    else:
        raise ValueError(f"Unknown generator type: {generator_type}")
        
    # --- Data Formatting for the Chart ---
    # The scatter plot in Chart.js expects a list of objects with 'x' and 'y' keys.
    # We only format the data this way if the user requested a 2D plot.
    if dimensionality == 2:
        return [{'x': p[0], 'y': p[1]} for p in points]
    else:
        # For other dimensions, we just return the raw list of points.
        # The template will display a message that it cannot be plotted.
        return points