class Matrix:
    def __init__(self, n):
        self.n = n
        self.rows = [dict() for _ in range(n)]

    def get(self, i, j):
        return self.rows[i].get(j, 0.0)

    def set(self, i, j, val):
        if val:
            self.rows[i][j] = val
        else:
            if j in self.rows[i]:
                del self.rows[i][j]

    def add(self, i, j, val):
        self.set(i, j, self.get(i, j) + val)

    def clone(self):
        m = Matrix(self.n)
        m.rows = [dict(row) for row in self.rows]
        return m

    def __add__(self, other):
        if self.n != other.n:
            raise Exception()
        result = self.clone()
        for i, row in enumerate(other.rows):
            for j, val in row.items():
                result.add(i, j, val)
        return result
        

    def __mul__(self, other):
        if self.n != other.n:
            raise Exception()
        result = Matrix(self.n)
        for i in range(self.n):
            for j in range(self.n):
                sum = 0.0
                for k in range(self.n):
                    sum += self.get(i, k) * other.get(k, j)
                result.set(i, j, sum)
        return result

    def __str__(self):
        out = ""
        for i in range(len(self.rows)):
            for j in range(len(self.rows)):
                out += str(self.get(i, j)) + "\t"
            out += "\n"
        return out
    

m1 = Matrix(3)
m1.set(0,0,1)
m1.set(1,1,1)
m1.set(2,2,1)
m2 = Matrix(3)
m2.set(0,1,5)
m2.set(2,2,20)
print(m2 * m1)