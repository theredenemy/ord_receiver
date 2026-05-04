def count_steps(value, steps):
    value_i = value
    for i in range(steps):
        value_i += value
    return value_i - value