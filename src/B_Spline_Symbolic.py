__author__ = 'Nexus'

import sympy
import matplotlib.pyplot as plt
"""
######################################################
########      THIS CLASS IS NOT USED       ###########
######################################################
"""

class B_Spline_Symbolic:
    def __init__(self, knot_list):
        self.b_splines = {}
        self.knot_list = knot_list

    def b_spline(self, n, k):
        """
        Calculates the B-Spline b and returns it in a symbolic representation
        :param n: n in b^n
        :param k: k in b_k
        :return: kth-b_spline of degree n
        """
        x = sympy.symbols('x')
        spline = None

        if n in self.b_splines and k in self.b_splines[n]:
            return self.b_splines[n][k]

        if n == 0:
            spline = sympy.Piecewise((1, (x < sympy.S(self.knot_list[k + 1])) & (x >= sympy.S(self.knot_list[k]))),
                                     (0, True))
        else:
            gamma_k = (x - sympy.S(self.knot_list[k])) / (sympy.S(self.knot_list[k + n]) - sympy.S(self.knot_list[k]))
            gamma_k_plus_1 = (x - sympy.S(self.knot_list[k + 1])) / (
                sympy.S(self.knot_list[k + 1 + n]) - sympy.S(self.knot_list[k + 1]))
            spline = sympy.piecewise_fold(
                gamma_k * self.b_spline(n - 1, k) + (1 - gamma_k_plus_1) * self.b_spline(
                    n - 1, k + 1))

        self.add_spline(spline, n, k)
        return spline


    def add_spline(self, spline, n, k):
        if n in self.b_splines:
            self.b_splines[n][k] = spline
        else:
            self.b_splines[n] = {k: spline}

    def calc_all_splines(self, n):
        """
        Calculates all possible b-splines of a given degree n
        :param n: degree
        :return:
        """
        for k in range(len(self.knot_list) - 1 - n):
            self.b_spline(n, k)


    def evaluate_b_spline(self, n, k, x_values):
        result = []
        for x in x_values:
            result.append(sympy.N(self.b_spline(n, k).subs(sympy.symbols('x'), sympy.S(x))))
        return result

    def plot_all_b_splines(self):
        """
        Plots all b-splines that have been calculated so far
        :return:
        """
        DISCRETE_STEPS = 100

        for n in self.b_splines:
            for k in self.b_splines[n]:
                x_vars = []

                for x in range(self.knot_list[len(self.knot_list) - 1] * DISCRETE_STEPS):
                    x_vars.append(x / float(DISCRETE_STEPS))
                plt.plot(x_vars, self.evaluate_b_spline(n, k, x_vars), ".", label="$b_" + str(k) + "^" + str(n) + "$")
        plt.legend()
        plt.show()

    def evaluate_spline_from_control_points(self, control_points, p, x):
        x_value = 0
        y_value = 0

        for i in range(len(self.knot_list) - p - 1):
            if i < len(control_points):
                x_value += control_points[i][0] * self.evaluate_b_spline(p, i, [x])[0]
                y_value += control_points[i][1] * self.evaluate_b_spline(p, i, [x])[0]
        return x_value, y_value

    def plot_spline_from_control_points(self, control_points, p, start_at, length):
        x_vars = []
        y_vars = []

        ctrl_x_vars = []
        ctrl_y_vars = []

        for x in range(0, 1000):
            values = self.evaluate_spline_from_control_points(control_points, p, start_at + (x * length / 1000.0))
            x_vars.append(values[0])
            y_vars.append(values[1])
        plt.plot(x_vars, y_vars)
        for point in control_points:
            ctrl_x_vars.append(point[0])
            ctrl_y_vars.append(point[1])
        plt.plot(ctrl_x_vars, ctrl_y_vars, "r")

        plt.show()
