
import os
import matplotlib.pyplot as plt

class PlotGenerator:
    def __init__(self):
        self.value_tables = []

    def pass_value_table(self, value_table):
        self.value_tables.append(value_table)

    def clear_value_tables(self):
        self.value_tables = []

    def create_tex_plot_from_value_tables(self, name, output_path):

        plot_string = ""  # will later contain all "\addplot" commands
        plot_counter = 1

        directory = None

        if output_path is not None:
            directory = output_path + "/" + name + "/plots/"
        else:
            directory = name + "/plots/"

        norm_directory = os.path.normpath(directory)
        if not os.path.exists(norm_directory):
            os.makedirs(norm_directory)

        # write the values into seperate files
        for value_table in self.value_tables:
            plot_path = directory + value_table.name + "_plot_" + str(plot_counter) + ".dat"  # use in tex src
            plot_path_norm = os.path.normpath(plot_path)  # use in dir
            print("opening " + plot_path + "...")
            plot_table_file = open(plot_path_norm, "w")

            # write all the value pairs with " " as delimiter
            for i in range(len(value_table.x_values)):
                plot_table_file.write(str(value_table.x_values[i]) + " " + str(value_table.y_values[i]) + "\n")

            plot_table_file.close()

            if value_table.style == "standard":  # Standard functions
                plot_string += "\\addplot[color=" + str(value_table.color) + "] table {\"" + plot_path + "\"};\n"
            if value_table.style == "points":
                plot_string += "\\addplot[color=" + str(value_table.color) + ",mark=x, only marks] table {\"" + plot_path + "\"};\n"
            elif value_table.style == "knots":
                plot_string += "\\addplot[color=" + str(
                    value_table.color) + ",only marks, mark=|] table {\"" + plot_path + "\"}\n"  # plot the knots
                plot_string += "node[pos=0.0,label=270:$\\xi_0$] {}\n node[pos=1.0,label=270:$\\xi_{" + str(
                    len(value_table.x_values) - 1) + "}$] {};\n"
            plot_counter += 1

        tex_src = open(os.path.normpath(directory + "/src.tex"), "w")  # the source code for the plots

        tex_src.write(
            "\\begin{tikzpicture}\n\\begin{axis}[title=" + name + ",xlabel={$x$},ylabel={$y$},extra x ticks={0,0},extra y ticks={0,0},extra tick style={grid=major}]\n" + plot_string + "\\end{axis}\n\\end{tikzpicture}")

        tex_src.close()

    def plot(self):
        """
        Plot with pyplot
        :return:
        """
        for vt in self.value_tables:
            if vt.style == "standard":
                plt.plot(vt.x_values, vt.y_values, color=vt.color)
            elif vt.style == "points":
                plt.plot(vt.x_values, vt.y_values, vt.color[0] + "x")
            elif vt.style == "knots":
                plt.plot(vt.x_values, vt.y_values, vt.color[0] + "|")
        plt.axhline(0, color="black")
        plt.show()