import pulp

M = 20
J = 2
K = 2
R_1 = 2
R_2 = 2
lambda_0 = 1.5
C_th = 20

V = pulp.LpVariable.dicts('y', (range(M), range(J), range(K), range(R_1), range(R_2)))
#V = pulp.LpVariable.dicts('y', (range(J), range(K)))
prob = pulp.LpProblem("MyProblem", pulp.LpMinimize)
prob += pulp.lpSum([i * V[i][j][k][r][b] for i in range(M) for j in range(J) for k in range(K) for r in range(R_1) for b in range(R_2)])

prob += pulp.lpSum([V[i][j][k][r][b] for i in range(M) for j in range(J) for k in range(K) for r in range(R_1) for b in range(R_2)]) == 1

for i in range(M):
    for j in range(J):
        for k in range(K):
            for r in range(R_1):
                for b in range(R_2):
                    prob += V[i][j][k][r][b] >= 0
                    prob += V[i][j][k][r][b] * (r + 10 * b) <= C_th
                    

prob.solve()
print("Status:", pulp.LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
