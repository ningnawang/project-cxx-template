import numpy as np

def noisy_udf_wrapper(clean_udf, noise_level):
    """Add Gaussian noise to UDF values.

    Supports both clean_udf styles used in this repo:
    - returns only distances, e.g. lambda x: unsigned_distance(...)[0]
    - returns the full unsigned_distance tuple: (distances, indices, lambdas)
    """
    def noisy_udf(pt):
        pt = np.asarray(pt)
        udf_value = clean_udf(pt)

        if isinstance(udf_value, tuple):
            distances = np.asarray(udf_value[0], dtype=np.float64)
            if noise_level > 0.0:
                distances = distances + np.random.normal(
                    0.0, noise_level, size=distances.shape
                )
            return (distances, *udf_value[1:])

        distances = np.asarray(udf_value, dtype=np.float64)
        if noise_level > 0.0:
            distances = distances + np.random.normal(
                0.0, noise_level, size=distances.shape
            )
        return distances
    return noisy_udf
