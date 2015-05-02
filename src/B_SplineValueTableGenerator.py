
import ValueTable as vt
import B_Spline_Tools as bst

def linear_combination_value_table(bspline_obj, start, end, n):
    """
    Plots a spline with corresponding coefficients
    :param coefficients:
    :param start:
    :param end:
    :param n:
    :param supports:
    :return:
    """

    # Preconditions:
    bspline_obj.check_preconditions(False, True, True)


    x_vars = []
    y_vars = []

    # sampling constant for plotting
    SAMPLES = (end - start) * bspline_obj.SAMPLE_RATE

    for i in range(0, int(SAMPLES)):
        current = start + (i / SAMPLES) * (end - start)
        x_vars.append(current)
        y_vars.append(bst.evaluate(bspline_obj, n, current))

    return vt.ValueTable("linear_combination", x_vars, y_vars, "blue")

def linear_combination_naive_value_table(bspline_obj, n):
    """
    Plots a spline with corresponding coefficients
    :param coefficients:
    :param start:
    :param end:
    :param n:
    :param supports:
    :return:
    """

    # Preconditions:
    bspline_obj.check_preconditions(False, True, True)


    x_vars = []
    y_vars = []

    start = bspline_obj.parameters["knotlist"][0]
    end = bspline_obj.parameters["knotlist"][-1]

    # sampling constant for plotting
    SAMPLES = (end - start) * bspline_obj.SAMPLE_RATE

    for i in range(0, int(SAMPLES)):
        current = start + (i / SAMPLES) * (end - start)
        x_vars.append(current)
        y_vars.append(bst.evaluate_naive(bspline_obj, n, current))

    return vt.ValueTable("linear_combination", x_vars, y_vars, "blue")

def b_spline_value_table(bspline_obj, n, k):
    """
    Plots a single b_spline in it's interval where it's not 0
    :param n:
    :param k:
    :param coefficients:
    :return:
    """
    # Preconditions:
    bspline_obj.check_preconditions(False, True, False)

    SAMPLES = (bspline_obj.parameters["knotlist"][k + n + 1] - bspline_obj.parameters["knotlist"][k]) * bspline_obj.SAMPLE_RATE

    x_vars = []
    y_vars = []

    for i in range(0, int(SAMPLES)):  # plot values in range [xi_k, xi_(k+n+1) )
        current = bspline_obj.parameters["knotlist"][k] + (i / SAMPLES) * (
        bspline_obj.parameters["knotlist"][k + n + 1] - bspline_obj.parameters["knotlist"][k])
        x_vars.append(current)
        if bspline_obj.parameters["coefficients"] is not None:
            y_vars.append(bspline_obj.parameters["coefficients"][k] * bspline_obj.b_spline(n, k, current))
        else:
            y_vars.append(bspline_obj.b_spline(n, k, current))

    return vt.ValueTable("basis_spline", x_vars, y_vars, "gray")

def b_spline_derivative_value_table(bspline_obj, n, k, ith):

    # Preconditions:
    bspline_obj.check_preconditions(False, True, False)


    SAMPLES = (bspline_obj.parameters["knotlist"][k + n + 1] - bspline_obj.parameters["knotlist"][k]) * bspline_obj.SAMPLE_RATE

    x_vars = []
    y_vars = []

    for i in range(0, int(SAMPLES)):
        current = bspline_obj.parameters["knotlist"][k] + (i / SAMPLES) * (
        bspline_obj.parameters["knotlist"][k + n + 1] - bspline_obj.parameters["knotlist"][k])
        x_vars.append(current)
        y_vars.append(bspline_obj.b_spline_derivative(n, k, ith, current))

    return vt.ValueTable("basis_spline_derivative", x_vars, y_vars, "orange")

def gamma_value_table(bspline_obj, n, k):

    # Preconditions:
    bspline_obj.check_preconditions(False, True, False)


    result = []

    # gamma k
    samples = (bspline_obj.parameters["knotlist"][k + n] - bspline_obj.parameters["knotlist"][k]) * bspline_obj.SAMPLE_RATE
    x_vars = []
    y_vars = []

    for i in range(0, int(samples)):
        current = bspline_obj.parameters["knotlist"][k] + (i / samples) * (
        bspline_obj.parameters["knotlist"][k + n] - bspline_obj.parameters["knotlist"][k])
        x_vars.append(current)
        y_vars.append(bspline_obj.gamma(n, k, current))

    result.append(vt.ValueTable("gamma", x_vars, y_vars, "orange"))

    # gamma k+1
    samples = (bspline_obj.parameters["knotlist"][k + 1 + n] - bspline_obj.parameters["knotlist"][k + 1]) * bspline_obj.SAMPLE_RATE
    x_vars = []
    y_vars = []


    for i in range(0, int(samples)):
        current = bspline_obj.parameters["knotlist"][k + 1] + (i / samples) * (
        bspline_obj.parameters["knotlist"][k + 1 + n] - bspline_obj.parameters["knotlist"][k + 1])
        x_vars.append(current)
        y_vars.append(1 - bspline_obj.gamma(n, k + 1, current))

    result.append(vt.ValueTable("gamma", x_vars, y_vars, "orange"))

    return result

def corresponding_b_splines_value_tables(bspline_obj, n):
    """
    Plots all b-Splines with coefficients for the corresponding knotlist on D_n
    :param coefficients:
    :param n:
    :return:
    """

    # Preconditions:
    bspline_obj.check_preconditions(False, True, False)

    m = len(bspline_obj.parameters["knotlist"]) - 1 - n
    value_tables = []

    for k in range(0, m):  # For every b_spline of degree n...
        value_tables.append(b_spline_value_table(bspline_obj, n, k))

    return value_tables


def corresponding_gamma_value_table(bspline_obj, n):
    """
    Plots the corresponding two gamma functions of b_spline^n_k
    :param n:
    :param k:
    :return:
    """
    # Preconditions:
    bspline_obj.check_preconditions(False, True, False)

    m = len(bspline_obj.parameters["knotlist"]) - 1 - n
    value_tables = []

    for k in range(0, m):
        value_tables += gamma_value_table(bspline_obj, n, k)

    return value_tables


def corresponding_b_splines_derivatives_value_tables(bspline_obj, n, ith):
    """
    Plots all b-Splines derivatives with coefficients for the corresponding knotlist on D_n
    :param coefficients:
    :param n:
    :return:
    """

    # Preconditions:
    bspline_obj.check_preconditions(False, True, False)

    m = len(bspline_obj.parameters["knotlist"]) - 1 - n
    value_tables = []

    for k in range(0, m):  # For every b_spline of degree n...
        x_vars = []
        y_vars = []

        value_tables.append(b_spline_derivative_value_table(bspline_obj, n, k, ith))

    return value_tables

def knotlist_value_table(bspline_obj):

    # Preconditions:
    bspline_obj.check_preconditions(False, True, False)

    return vt.ValueTable("knots", bspline_obj.parameters["knotlist"], [0 for knot in bspline_obj.parameters["knotlist"]], "green", "knots")

def interp_points_value_table(bspline_obj):
    # Preconditions:
    bspline_obj.check_preconditions(True, False, False)

    mult = bspline_obj.determine_multiplicity_interp_points()
    x_vars = []
    y_vars = []

    for k in range(len(bspline_obj.parameters["interp_points"])):
        if mult[k] == 0:
            x_vars.append(bspline_obj.parameters["interp_points"][k][0])
            y_vars.append(bspline_obj.parameters["interp_points"][k][1])

    return vt.ValueTable("interp_points", x_vars, y_vars, "red", "points")