import time


def calculate_time(func):
    def inner(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        print("our time: ", time.time() - begin)
        return result
    return inner


class GaloisNumber:
    def __init__(self, value, field_size):
        self.value = value
        self.field_size = field_size

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        first_number = self.value
        second_number = other.value
        if len(first_number) > len(second_number):
            size = len(first_number)
        else:
            size = len(second_number)
        result_bin = ''
        for i in range(size):
            temp = int(first_number[i]) + int(second_number[i])
            result_bin += str(temp % 2)

        return self.__class__(result_bin, self.field_size)

    @staticmethod
    def left_shift(number, shift):
        num_list = list(number)
        num_list = num_list[shift:] + num_list[:shift]
        result = ''
        for i in num_list:
            result += i
        return result

    @calculate_time
    def matrix_create(self):
        p = 2 * self.field_size + 1
        multiplicative_matrix = [[0]*self.field_size for _ in range(self.field_size)]
        for i in range(self.field_size):
            for j in range(self.field_size):
                if (2**i + 2**j) % p == 1:
                    multiplicative_matrix[i][j] = 1
                elif (2**i - 2**j) % p == 1:
                    multiplicative_matrix[i][j] = 1
                elif (-1 * 2**i + 2**j) % p == 1:
                    multiplicative_matrix[i][j] = 1
                elif (-1 * 2**i - 2**j) % p == 1:
                    multiplicative_matrix[i][j] = 1
                else:
                    multiplicative_matrix[i][j] = 0
        return multiplicative_matrix

    @calculate_time
    def __mul__(self, other):
        result = ''
        multiplicative_matrix = self.matrix_create()
        for z in range(self.field_size):
            result_1 = [0 for _ in range(self.field_size)]
            result_2 = 0
            pre_1 = self.left_shift(self.value, z)
            pre_2 = self.left_shift(other.value, z)

            for i in range(self.field_size):
                for j in range(self.field_size):
                    result_1[i] += int(pre_1[j]) * multiplicative_matrix[j][i]
                result_1[i] = result_1[i] % 2

            for i in range(self.field_size):
                result_2 += result_1[i] * int(pre_2[i])
            result_2 = result_2 % 2
            result += str(result_2)

        return self.__class__(result, self.field_size)

    @calculate_time
    def __pow__(self, power, modulo=None):
        result = self * self
        for i in range(int(power.value, 2) - 2):
            result = self * result
        return self.__class__(result, self.field_size)

    @calculate_time
    def double_pow(self):
        return bin(int(self.value, 2) >> 1)[2:]

    @calculate_time
    def tr(self):
        res = 0
        for i in range(len(self.value)):
            res += int(self.value[i])
        res = res % 2
        return res


first = GaloisNumber(input(), 179)
second = GaloisNumber(input(), 179)
degree = GaloisNumber(input(), 179)
print("-----Calculating!-----")
print("Addition: ", first + second)
print("Multiplication: ", first * second)
print("Square: ", first * first)
print("Degree: ", first ** degree)
print("Trace: ", degree.tr())

