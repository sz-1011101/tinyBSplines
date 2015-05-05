
class B_Spline:
    """
    This class can be used to evaluate and calculate B-Splines
    """
    SAMPLE_RATE = 50.0  # used to determine how fine plots will be

    def __init__(self, knotlist, coefficients, interp_points):
	"""
	:param knot_list: knotlist/vector to construct b-splines form
	:param coefficients: coefficients to multiply on the b-splines
	:param interp_points: points to create a interpolating spline from
	"""
        self.parameters = {"knotlist": knotlist, "coefficients": coefficients, "interp_points": interp_points}

    def set_parameter(self, key, data):
        """
        use to set the parameters of this Spline obj.
        :param key: knotlist, interp_points, coefficients
        :param data: 
        """
        if (key == "knotlist"):
            for i in range(1, len(data)):
                if data[i-1] > data[i]:
                    raise self.ParameterWrongForm("new knotlist not monotonous rising")
        elif (key == "interp_points"):
            for i in range(1, len(data)):
                if data[i-1][0] > data[i][0]:
                    raise self.ParameterWrongForm("interp_points x-values not monotonous rising")

        self.parameters[key] = data

    def gamma(self, n, k, x):
        """
        The Gamma from the recursive B_spline definition
        :param n: degree of the b-spline
        :param k: the b-spline's k'
        :param x: evaluation at x
        :return: gamma value corresponding to kth b-spline of degree n
        """

        # Preconditions:
        self.check_preconditions(False, True, False)

        if self.parameters["knotlist"][k + n] == self.parameters["knotlist"][k]:
            return 0.0
        return (x - self.parameters["knotlist"][k]) / float(
            self.parameters["knotlist"][k + n] - self.parameters["knotlist"][k])


    def b_spline(self, n, k, x):
	"""
	Calculates the value of the kth b-spline of degree n at x
	:param n: degree of b
	:param k: k of b
	:param x: evaluation at x
	:return: value of kth b-spline of degree n at x 
	"""
        # Preconditions:
        self.check_preconditions(False, True, False)

        if n == 0:
            if self.parameters["knotlist"][k] <= x and x < self.parameters["knotlist"][k + 1]:
                return 1.0
            else:
                return 0.0

        return (self.gamma(n, k, x) * self.b_spline(n - 1, k, x)) + (
            (1 - self.gamma(n, k + 1, x)) * self.b_spline(n - 1,
                                                          k + 1,
                                                          x))

    def alpha(self, n, k, x):
	"""
	Calculates the alpha of the derivative of the kth b-spline of degree n at x
	:param n: degree of b-spline
	:param k: k of b
	:param x: evaluate at x
	"""
        # Preconditions:
        self.check_preconditions(False, True, False)

        if self.parameters["knotlist"][k + n] == self.parameters["knotlist"][k]:
            return 0.0
        return n / float(self.parameters["knotlist"][k + n] - self.parameters["knotlist"][k])

    def b_spline_derivative(self, n, k, i_th, x):
	"""
	Calculates (b^n_k)^(ith), aka the ith-derivative of b^n_k
	:param n: degree of the b-spline to derivate
	:param k: the k of b
	:param ith: how often 
	:return ith deriv value of kth b-spline of degree n
	"""
        # Preconditions:
        self.check_preconditions(False, True, False)

        if i_th == 0:
            return self.b_spline(n, k, x)
        elif i_th == 1:
            return self.alpha(n, k, x) * self.b_spline(n - 1, k, x) - self.alpha(n, k + 1, x) * self.b_spline(n - 1,
                                                                                                              k + 1, x)
        else:
            return self.alpha(n, k, x) * self.b_spline_derivative(n - 1, k, i_th - 1, x) - self.alpha(n, k + 1,
                                                                                                      x) * self.b_spline_derivative(
                n - 1, k + 1, i_th - 1, x)


    def determine_multiplicity_interp_points(self):
	"""
	Returns the muliplicity of the interpolation points, e.g for 1,2,2,2,3,4,4: 0,0,1,2,0,0,1
	:return: the mulitplicity of self.parameters["interp_points"]
	"""
        # Preconditions:
        self.check_preconditions(True, False, False)

        multiplicities = []

        # TODO: This could be done way better
        for j in range(len(self.parameters["interp_points"])):
            multiplicities.append(0)
            for i in range(1, j + 1):
                if self.parameters["interp_points"][j - i][0] == self.parameters["interp_points"][j][0]:
                    multiplicities[j] += 1

        return multiplicities


    def check_preconditions(self, interp_available, knotlist_available, coeefficients_available):
        """
        Check for flagged preconditions
        :param interp_available: Check if interpolation points are available
        :param knotlist_available: Check if knotlist available
        :param coeefficients_available: Check if coefficients available
        """

        if interp_available and (self.parameters["interp_points"] is None or len(self.parameters["interp_points"]) == 0):
            raise self.PreConditionsNotSatisfied("interp_points empty?")
        if knotlist_available and (self.parameters["knotlist"] is None or len(self.parameters["knotlist"]) == 0):
            raise self.PreConditionsNotSatisfied("knotlist empty?")
        if coeefficients_available and (self.parameters["coefficients"] is None or len(self.parameters["coefficients"]) == 0):
            raise self.PreConditionsNotSatisfied("coefficients empty?")

    class PreConditionsNotSatisfied(Exception):
        def __init__(self, message):
            self.message = message


    class SchoenbergWhitneyNotSatisfied(Exception):
        def __init__(self, message):
            self.message = message


    class ParameterWrongForm(Exception):
        def __init__(self, message):
            self.message = message
