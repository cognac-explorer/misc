# Uses python3

def edit_distance(s, t):
    n = len(s)
    m = len(t)
    d_matrix = [[0 for _ in range(m+1)] for _ in range(n+1)]

    for i in range(n+1):
        d_matrix[i][0] = i
    
    for j in range(m+1):
        d_matrix[0][j] = j
    
    for i in range(1, n+1):
        for j in range(1, m+1):
            insert_e = d_matrix[i-1][j] + 1
            delete_e = d_matrix[i][j-1] + 1
            match_e = d_matrix[i-1][j-1]
            mismatch_e = d_matrix[i-1][j-1] + 1

            if s[i-1] == t[j-1]:
                d_matrix[i][j] = min(insert_e, delete_e, match_e)
            else:
                d_matrix[i][j] = min(insert_e, delete_e, mismatch_e)

    return d_matrix[i][j]


if __name__ == "__main__":
    print(edit_distance(input(), input()))
