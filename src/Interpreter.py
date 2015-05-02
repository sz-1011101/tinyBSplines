
import B_Spline as bs
import B_SplineValueTableGenerator as bsvg
import B_Spline_Tools as bst
import PlotGenerator as pg

class Interpreter:
    """
    Handles user input
    """
    def __init__(self):

        self.plot_gen = pg.PlotGenerator()
        self.spline_obj = bs.B_Spline(None, None, None)
        self.queue = []  # Queue of commands to be interpreted

        self.commands = {"set": self.command_set, "save": self.command_save, "interpolate": self.command_interpolate,
                         "tex": self.command_tex, "plot": self.command_plot, "clear": self.command_clear,
                         "exec": self.command_exec, "quit": self.command_quit, "evaluate": self.command_evaluate,
                         "evaluate_naive": self.command_evaluate_naive}

        self.data_interpretation = {"knotlist": self.string_list_to_float_list,
                                    "coefficients": self.string_list_to_float_list,
                                    "interp_points": self.string_list_to_float_tuples_list}

    def command_set(self, key, raw_data):
        if raw_data is not None and key in self.data_interpretation:
            try:
                data = self.data_interpretation[key](raw_data)
                self.spline_obj.set_parameter(key, data)
            except ValueError as exception:
                print("An ValueError occurred: " + exception.message)
        else:
            print("No data given or unknown key")
        return True

    def command_save(self, key, raw_data):
        try:
            if key == "basis":  # Saves the basis splines for the degree given by raw_data

                degree = int(raw_data)
                corr_splines_derivatives = bsvg.corresponding_b_splines_value_tables(self.spline_obj, degree)

                for value_table in corr_splines_derivatives:
                    self.plot_gen.pass_value_table(value_table)
                print("Basis saved")

            elif key == "derivatives":  # Saves the basis splines for the degree given by raw_data

                degree = int(raw_data)
                corr_splines_derivatives = bsvg.corresponding_b_splines_derivatives_value_tables(self.spline_obj, degree, 1)

                for value_table in corr_splines_derivatives:
                    self.plot_gen.pass_value_table(value_table)
                print("Derivatives saved")

            elif key == "linearcomb":  # Saves the linear combination spline curve of deg given by raw_data
                if raw_data is not None:
                    degree = int(raw_data)
                else:
                    raise ValueError("degree is None")

                start = self.spline_obj.parameters["knotlist"][degree]
                end = self.spline_obj.parameters["knotlist"][len(self.spline_obj.parameters["coefficients"])]
                lin_comb = bsvg.linear_combination_value_table(self.spline_obj, start, end, degree)
                self.plot_gen.pass_value_table(lin_comb)
                print("Linear combination saved")
            elif key == "linearcomb_complete":  # Saves the linear combination spline curve of deg given by raw_data on whole knotlist
                if raw_data is not None:
                    degree = int(raw_data)
                else:
                    raise ValueError("degree is None")
                # Here we want to plot over the entire knotlist
                lin_comb = bsvg.linear_combination_naive_value_table(self.spline_obj,degree)
                self.plot_gen.pass_value_table(lin_comb)
                print("Linear combination saved")

            elif key == "knotlist":  # Saves the knots Xi, useful for showing the knot intervals

                knots = bsvg.knotlist_value_table(self.spline_obj)
                self.plot_gen.pass_value_table(knots)
            elif key == "interp_points":
                interp_points = bsvg.interp_points_value_table(self.spline_obj)
                self.plot_gen.pass_value_table(interp_points)
            elif key == "gamma":
                if raw_data is not None:
                    degree = int(raw_data)
                else:
                    raise ValueError("degree is None")

                corr_gammas = bsvg.corresponding_gamma_value_table(self.spline_obj, degree)

                for value_table in corr_gammas:
                    self.plot_gen.pass_value_table(value_table)
                print("Gammas saved")
            else:
                print("unexpected keyword \"" + key + "\".")
        except ValueError as exception:
            print("An ValueError occurred." + exception.message)
        except self.spline_obj.PreConditionsNotSatisfied as exception:
            print(exception.message)
        except self.spline_obj.SchoenbergWhitneyNotSatisfied as exception:
            print(exception.message)

        return True

    def command_interpolate(self, key, raw_data):
        try:
            # interpret key as degree, raw_data as interpolation points
            degree = int(key)

            print("Determining coefficients")
            bst.determine_coefficients(self.spline_obj, degree)
        except IndexError as exception:
            print("An IndexError occurred: " + exception.message)
        except ValueError as exception:
            print("An ValueError occurred: " + exception.message)
        except self.spline_obj.PreConditionsNotSatisfied as exception:
            print(exception.message)
        except self.spline_obj.SchoenbergWhitneyNotSatisfied as exception:
            print(exception.message)

        return True

    def command_evaluate(self, key, raw_data):
        try:
            if key is not None and raw_data is not None:
                degree = int(key)
                at_x = float(raw_data)
                print("p("+str(at_x)+") = "+str(bst.evaluate(self.spline_obj, degree, at_x)))
            else:
                print ("Give n and x")
        except ValueError:
            print("An ValueError occurred.")

        return True

    def command_evaluate_naive(self, key, raw_data):
        try:
            if key is not None and raw_data is not None:
                degree = int(key)
                at_x = float(raw_data)
                print(bst.evaluate_naive(self.spline_obj, degree, at_x))
            else:
                print ("Give n and x")
        except ValueError:
            print("An ValueError occurred.")

        return True

    def command_tex(self, key, raw_data):
        try:
            name = str(key)

            if raw_data is not None:  # path given?
                path = raw_data  # TODO: Parse this?
                self.plot_gen.create_tex_plot_from_value_tables(name, path)  # name, outputpath
            else:
                self.plot_gen.create_tex_plot_from_value_tables(name, None)  # name only

        except IOError as exception:
            print("An IOError occurred: " + exception.message)

        return True

    def command_plot(self, key, raw_data):
        self.plot_gen.plot()
        return True

    def command_clear(self, key, raw_data):
        self.plot_gen.clear_value_tables()
        self.spline_obj.parameters["knotlist"] = None
        self.spline_obj.parameters["coefficients"] = None
        return True

    def command_quit(self, key, raw_data):
        return False

    def command_exec(self, key, raw_data):

        try:
            command_file = open(str(key))
            self.queue += [line.strip() for line in command_file]  # add all lines in the file to the queue
        except IOError as exception:
            print("An IOError occurred: " + exception.message)
        return True

    def interpret(self):
        # interpret from queue first
        if len(self.queue) > 0:
            console_input = self.queue.pop(0)
        else:  # otherwise read user input
            console_input = raw_input(">>")

        console_input_split = console_input.split(" ", 2)  # split in 3 elements: command, key and given data

        command, key, raw_data = None, None, None

        if len(console_input_split) >= 1:
            command = console_input_split[0]

        if len(console_input_split) >= 2:
            key = console_input_split[1]

        if len(console_input_split) == 3:
            raw_data = console_input_split[2]

        if command in self.commands:
            return self.commands[command](key, raw_data)
        else:
            print("Command not recognized")
            return True

    def string_list_to_float_list(self, string_list):
        # TODO catch unintended data
        string_list_raw = string_list.replace(" ", "")
        data_string_list = string_list_raw.split(",")
        result = []

        for value in data_string_list:
            result.append(float(value))

        return result

    def string_list_to_float_tuples_list(self, string_list):
        # TODO catch unintended data
        string_list_raw = string_list.replace(" ", "")
        data_string_list = string_list_raw.split("),(")
        result = []

        for value in data_string_list:
            data = value.replace("(", "").replace(")", "").split(",")  # remove parenthesis and split
            data = float(data[0]), float(data[1])
            result.append(tuple(data))

        return result

