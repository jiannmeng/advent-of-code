def is_valid(password):
    password = str(password)

    has_adjacent_same = [
        password[i] == password[i + 1] for i in range(len(password) - 1)
    ]
    print(has_adjacent_same)

    is_not_decreasing = [
        int(password[i]) >= int(password[i + 1]) for i in range(len(password) - 1)
    ]
    print(is_not_decreasing)
    return None
