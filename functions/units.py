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

    elif dim == "temperature":
        if unit == "C":
            return value + 273.15

        elif unit == "K":
            return value

        else:
            raise ValueError("Unsupported temperature unit type.")

    elif dim == "pressure":
        if unit == "psi":
            return value * 6894.7572932

        elif unit == "Pa":
            return value

        else:
            raise ValueError("Unsupported pressure unit type.")

    else:
        raise ValueError("Unsupported dimension type.")

    return value