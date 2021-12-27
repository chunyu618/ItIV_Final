import pulp
import numpy as np
import json

Q = 21 # Queue length 20
M = 4 # packet arrival rate 0, 1, 2, 3
J = 2 # Encountering RSU in current time slot, yes or no
K = 3 # Will encounter RSU in next time slot, yes, no , or unkown
R_1 = 6 # RSU download rate at most 5
R_2 = 3 # cellular download rate at most 2
lambda_0 = 1.5
C_th = 20
p_m = 1 / M
p_s = 0.3
p_v = 0.5
C_r = 1 # cost for use RSU
C_b = 10 # cost for use cellular

V = pulp.LpVariable.dicts('y', (range(Q), range(J), range(K), range(R_1), range(R_2)))
#V = pulp.LpVariable.dicts('y', (range(J), range(K)))
prob = pulp.LpProblem("MyProblem", pulp.LpMinimize)
prob +=  pulp.lpSum([i * V[i][j][k][r][b] for i in range(M) for j in range(J) for k in range(K) for r in range(R_1) for b in range(R_2)])

prob += pulp.lpSum([V[i][j][k][r][b] for i in range(Q) for j in range(J) for k in range(K) for r in range(R_1) for b in range(R_2)]) == 1


lambda_2 = np.zeros((Q, J, K, J, K))
for i in range(Q):
    for j in range(J):
        for k in range(K):
            if k != 2:
                lambda_2[i][j][k][k][0] = p_v * (1 - p_s)
                lambda_2[i][j][k][k][1] = p_v * p_s
                lambda_2[i][j][k][k][2] = (1 - p_v)
            elif k == 2:
                lambda_2[i][j][k][0][0] = p_v * (1 - p_s) * (1 - p_s)
                lambda_2[i][j][k][0][1] = p_v * p_s * (1 - p_s)
                lambda_2[i][j][k][0][2] = (1 - p_v) * p_s
                lambda_2[i][j][k][1][0] = p_v * p_s * (1 - p_s)
                lambda_2[i][j][k][1][1] = p_v * p_s * p_s
                lambda_2[i][j][k][1][2] = (1 - p_v) * (1 - p_s)






for i in range(Q):
    for j in range(J):
        for k in range(K):
            # y >= 0
            # y(c_r + c_b) <= C_th
            for r in range(R_1):
                for b in range(R_2):
                    prob += V[i][j][k][r][b] >= 0
                    prob += V[i][j][k][r][b] * (C_r * r + C_b * b) <= C_th
            
            # Transition matrix lambda_1 * lambda_2
            # Transit to state (i, j, k)
            prob += pulp.lpSum(lambda_2[_i][_j][_k][j][k] * pulp.lpSum([int(_i + m - _j * _r - _b == i) * p_m * V[_i][_j][_k][_r][_b] for m in range(M) for _r in range(R_1) for _b in range(R_2)]) for _i in range(Q) for _j in range(J) for _k in range(K)) - pulp.lpSum(V[i][j][k][r][b] for r in range(R_1) for b in range(R_2)) <= 0.001
            prob += pulp.lpSum(lambda_2[_i][_j][_k][j][k] * pulp.lpSum([int(_i + m - _j * _r - _b == i) * p_m * V[_i][_j][_k][_r][_b] for m in range(M) for _r in range(R_1) for _b in range(R_2)]) for _i in range(Q) for _j in range(J) for _k in range(K)) - pulp.lpSum(V[i][j][k][r][b] for r in range(R_1) for b in range(R_2)) >= -0.001
            #prob += pulp.lpSum([V[i][j][k][r][b] for r in range(R_1) for b in range(R_2)]) == pulp.lpSum([V[i][j][k][r][b] for r in range(R_1) for b in range(R_2)])

prob.solve()
pi = np.zeros((Q, J, K))
F = np.zeros((Q, J, K, R_1, R_2))
for i in range(Q):
    for j in range(J):
        for k in range(K):
            for r in range(R_1):
                for b in range(R_2):
                    pi[i][j][k] += V[i][j][k][r][b].varValue
            print(i, j, k, pi[i][j][k])
        
            for r in range(R_1):
                for b in range(R_2):
                    if pi[i][j][k] != 0:
                        F[i][j][k][r][b] = V[i][j][k][r][b].varValue / pi[i][j][k]
                    else:
                        F[i][j][k] = 1 / (R_1 * R_2)
            print(F[i][j][k])
            print(np.sum(F[i][j][k]))


#print("Sum over pi is ", np.sum(pi))
print("Status:", pulp.LpStatus[prob.status])

with open("strategy2.json", "w") as outfile:
    json.dump(F.tolist(), outfile, indent=4)
