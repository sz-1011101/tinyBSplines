
import numpy as np

def evaluate(bspline_obj, n, x):
    """
    De Boor's algorithm for evaluating a linear combination of b_splines
    """

    # Preconditions:
    bspline_obj.check_preconditions(False, True, True)

    # find boundary l in knot_list (TODO: change)
    xi_counter = 0
    l = -1

    for i in range(len(bspline_obj.parameters["knotlist"])):
        if bspline_obj.parameters["knotlist"][i] <= x and x < bspline_obj.parameters["knotlist"][i + 1]:
            l = xi_counter
            break
        xi_counter += 1

    p = {0: {}}

    for k in range(l - n, l + 1):
        if len(bspline_obj.parameters["coefficients"])>k:
            p[0][k] = bspline_obj.parameters["coefficients"][k]

    for i in range(0, n):
        p[i + 1] = {}
        for k in range(l - n + i + 1, l + 1):
            gam = bspline_obj.gamma(n - i, k, x)
            p[i + 1][k] = (gam * float(p[i][k])) + ((1 - gam) * float(p[i][k - 1]))

    return p[n][l]

def evaluate_naive(bspline_obj, n, x):
    result = 0

    for i in range(0,len(bspline_obj.parameters["knotlist"])-n-1):
        result += bspline_obj.parameters["coefficients"][i] * bspline_obj.b_spline(n, i, x)

    return result

def determine_coefficients(bspline_obj, n):

    # Preconditions:
    bspline_obj.check_preconditions(True, True, False)

    check_schoenberg_whitney(bspline_obj, n)

    a = np.zeros(shape=(len(bspline_obj.parameters["interp_points"]), len(bspline_obj.parameters["interp_points"])))
    b = np.array([i[1] for i in bspline_obj.parameters["interp_points"]])
    multiplicities = bspline_obj.determine_multiplicity_interp_points()

    # fill matrix
    for j in range(len(bspline_obj.parameters["interp_points"])):
        for k in range(len(bspline_obj.parameters["interp_points"])):
            a[j, k] = bspline_obj.b_spline_derivative(n, k, multiplicities[j],
                                               bspline_obj.parameters["interp_points"][j][0])
    # print(a)
    bspline_obj.parameters["coefficients"] = np.linalg.solve(a, b).tolist()

def check_schoenberg_whitney(bspline_obj, n):

    # Preconditions:
    bspline_obj.check_preconditions(True, True, False)

    m = len(bspline_obj.parameters["knotlist"]) - n - 1

    if m != len(bspline_obj.parameters["interp_points"]):
        raise bspline_obj.PreConditionsNotSatisfied("Violation of Schoenberg-Whitney Conditions:\nYou must use interp_points t_0 <= ... <= t_"+str(m-1))

    for k in range(len(bspline_obj.parameters["interp_points"])):
        t_k = bspline_obj.parameters["interp_points"][k][0]
        xi_k = bspline_obj.parameters["knotlist"][k]
        xi_k_plus_n_plus_1 = bspline_obj.parameters["knotlist"][k+n+1]

        if not (xi_k  < t_k and t_k < xi_k_plus_n_plus_1):
            raise bspline_obj.SchoenbergWhitneyNotSatisfied("Violation of Schoenberg-Whitney Conditions:\nt_"+str(k)+" = "+str(t_k)+", xi_"+str(k)+" = "+str(xi_k)+" < t_"+str(k)+" < xi_"+str(k+n+1)+" = "+str(xi_k_plus_n_plus_1))

        if t_k < bspline_obj.parameters["knotlist"][n] or t_k > bspline_obj.parameters["knotlist"][m]:
            raise bspline_obj.SchoenbergWhitneyNotSatisfied("Violation of Schoenberg-Whitney Conditions:\nt_"+str(k)+" = "+str(t_k)+" is outside of [xi_"+str(n)+",xi_"+str(m)+"]")

    return True