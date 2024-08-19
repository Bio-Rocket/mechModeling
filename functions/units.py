def convertToSI(value, unit, dim):

    if dim == "volume":
        if unit == "L":
            return value * 1e-3

        elif unit == "m^3":
            return value

        else:
            raise ValueError("Unsupported volume unit type.")

    elif dim == "mass":
        if unit == "kg":
            return value

        else:
            raise ValueError("Unsupported mass unit type.")

    elif dim == "time":
        if unit == "s":
            return value
        
        else:
            raise ValueError("Unsupported time unit type.")

    else:
        raise ValueError("Unsupported dimension type.")

    return value